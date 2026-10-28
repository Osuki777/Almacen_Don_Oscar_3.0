"""Pruebas aisladas con SQLite en memoria; no contienen datos reales."""
import unittest,sqlite3,sys,types,hashlib,importlib.util
from pathlib import Path
from unittest.mock import patch
import seguridad_credenciales as sc
ROOT=Path(__file__).parent
class SecurityTests(unittest.TestCase):
 def setUp(self):
  fake=types.ModuleType('modulos.ui');fake.Colores=types.SimpleNamespace(INPUT='')
  for n in ['limpiar_pantalla','imprimir_titulo','imprimir_advertencia','imprimir_error','imprimir_exito','presione_enter']:setattr(fake,n,lambda *a:None)
  sys.modules['modulos.ui']=fake
  if 'modulos' not in sys.modules:
   mod=types.ModuleType('modulos');mod.__path__=[str(ROOT/'modulos')];sys.modules['modulos']=mod
  setattr(sys.modules['modulos'],'ui',fake)
  spec=importlib.util.spec_from_file_location('test_auth_actual',ROOT/'modulos/auth.py');self.auth=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.auth)
  self.c=sqlite3.connect(':memory:');self.c.executescript("CREATE TABLE usuarios(id INTEGER PRIMARY KEY,username TEXT,password_hash TEXT,nombre_completo TEXT,rol TEXT,is_activo INTEGER);CREATE TABLE configuracion(clave TEXT PRIMARY KEY,valor TEXT);CREATE TABLE ventas(id INTEGER PRIMARY KEY,total REAL);INSERT INTO ventas VALUES(11,123.45);")
 def tearDown(self):self.c.close()
 def add(self,h,active=1,pin='654321'):
  self.c.execute('INSERT INTO usuarios VALUES(1,?,?,?,?,?)',('operador',h,'Persona ficticia','admin',active));self.c.execute('INSERT INTO configuracion VALUES(?,?)',('clave_cancelacion',pin));self.c.commit()
 def login(self,password):
  with patch('builtins.input',return_value='operador'),patch.object(self.auth,'leer_secreto',return_value=password):return self.auth.login(self.c)
 def test_salts_and_verification(self):
  a=sc.hash_password('frase ficticia de pruebas');b=sc.hash_password('frase ficticia de pruebas');self.assertNotEqual(a,b);self.assertTrue(sc.verificar_password('frase ficticia de pruebas',a));self.assertFalse(sc.verificar_password('incorrecta',a));self.assertFalse(sc.verificar_password('x','pbkdf2_sha256$999999999$00$00'))
 def test_legacy_upgrades_only_after_correct_login(self):
  pwd='frase anterior ficticia';old=hashlib.sha256(b'don_oscar_salt_secreto'+pwd.encode()).hexdigest();self.add(old);self.assertIsNone(self.login('incorrecta'));self.assertEqual(self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0],old);self.assertIsNotNone(self.login(pwd));new=self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0];self.assertTrue(new.startswith('pbkdf2_sha256$'));self.assertTrue(sc.verificar_password(pwd,new));self.assertEqual(self.c.execute('SELECT total FROM ventas').fetchone()[0],123.45)
 def test_plain_factory_requires_replacement_and_pin(self):
  old='toor';self.add(old,pin='1234')
  with patch.object(self.auth,'pedir_password',return_value='nueva frase ficticia'),patch.object(self.auth,'pedir_pin',return_value='987654'):self.assertIsNotNone(self.login(old))
  h=self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0];self.assertFalse(sc.verificar_password(old,h));self.assertTrue(sc.verificar_password('nueva frase ficticia',h));self.assertEqual(self.c.execute('SELECT valor FROM configuracion').fetchone()[0],'987654')
 def test_hashed_factory_also_requires_replacement(self):
  old=hashlib.sha256(b'don_oscar_salt_secreto'+b'toor').hexdigest();self.add(old)
  with patch.object(self.auth,'pedir_password',return_value='otra frase ficticia'):
   self.assertIsNotNone(self.login('toor'))
  h=self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0];self.assertFalse(sc.verificar_password('toor',h));self.assertTrue(sc.verificar_password('otra frase ficticia',h))
 def test_cancel_migration_is_atomic(self):
  self.add('toor',pin='1234')
  with patch.object(self.auth,'pedir_password',return_value='nueva frase ficticia'),patch.object(self.auth,'pedir_pin',side_effect=KeyboardInterrupt):self.assertIsNone(self.login('toor'))
  self.assertEqual(self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0],'toor');self.assertEqual(self.c.execute('SELECT valor FROM configuracion').fetchone()[0],'1234')
 def test_disabled_user_cannot_migrate(self):
  self.add('toor',active=0);self.assertIsNone(self.login('toor'));self.assertEqual(self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0],'toor')
 def test_new_database_has_no_factory_secrets(self):
  spec=importlib.util.spec_from_file_location('test_database_actual',ROOT/'modulos/database.py');db=importlib.util.module_from_spec(spec);spec.loader.exec_module(db);c=sqlite3.connect(':memory:');h=sc.hash_password('alta ficticia de pruebas')
  with patch.object(sc,'pedir_alta_inicial',return_value=('dueño',h,'876543')):db.crear_schema(c)
  self.assertEqual(c.execute('SELECT username,password_hash FROM usuarios').fetchone(),('dueño',h));self.assertEqual(c.execute("SELECT valor FROM configuracion WHERE clave='clave_cancelacion'").fetchone()[0],'876543');c.close()
 def test_cancel_setup_writes_no_schema(self):
  spec=importlib.util.spec_from_file_location('test_database_cancel',ROOT/'modulos/database.py');db=importlib.util.module_from_spec(spec);spec.loader.exec_module(db);c=sqlite3.connect(':memory:')
  with patch.object(sc,'pedir_alta_inicial',side_effect=KeyboardInterrupt),self.assertRaises(KeyboardInterrupt):db.crear_schema(c)
  self.assertEqual(c.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0],0);c.close()
 def test_existing_pbkdf2_login_remains_valid(self):
  h=sc.hash_password('frase ficticia vigente');self.add(h);self.assertIsNotNone(self.login('frase ficticia vigente'));self.assertEqual(self.c.execute('SELECT password_hash FROM usuarios').fetchone()[0],h)
if __name__=='__main__':unittest.main()
