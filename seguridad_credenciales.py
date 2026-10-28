# © 2025-2026 Oscar Salvador Fernandez. Derechos reservados. Ver LICENSE y LEGAL.md.
"""Credenciales locales: hashes lentos, compatibilidad histórica y entrada sin eco."""
import getpass
import hashlib
import hmac
import secrets
import re

ITERACIONES = 600_000
# Solo para reconocer y migrar datos antiguos; no se utiliza para hashes nuevos.
_SALT_LEGACY = b"don_oscar_salt_secreto"
_DEFAULT_DIGEST = "ce5ca673d13b36118d54a7cf13aeb0ca012383bf771e713421b4d1fd841f539a"

def es_password_fabrica(password):
    return hmac.compare_digest(hashlib.sha256(password.encode('utf-8')).hexdigest(), _DEFAULT_DIGEST)

def hash_password(password):
    if not isinstance(password,str) or not password or len(password)>1024:
        raise ValueError('Contraseña vacía o demasiado larga.')
    salt=secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,ITERACIONES)
    return 'pbkdf2_sha256$'+str(ITERACIONES)+'$'+salt.hex()+'$'+digest.hex()

def verificar_password(password,stored):
    if not isinstance(password,str) or len(password)>1024 or not isinstance(stored,str):return False
    if stored.startswith('pbkdf2_sha256$'):
        try:
            _,rounds,salt,digest=stored.split('$');rounds=int(rounds)
            if not 100_000<=rounds<=2_000_000 or not re.fullmatch('[0-9a-f]{32}',salt) or not re.fullmatch('[0-9a-f]{64}',digest):return False
            actual=hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),bytes.fromhex(salt),rounds).hex()
            return hmac.compare_digest(actual,digest)
        except (ValueError,TypeError):return False
    if re.fullmatch('[0-9a-f]{64}',stored):
        actual=hashlib.sha256(_SALT_LEGACY+password.encode('utf-8')).hexdigest()
        return hmac.compare_digest(actual,stored)
    # Compatibilidad exclusivamente con el administrador inicial histórico en texto.
    return es_password_fabrica(stored) and hmac.compare_digest(password,stored)

def leer_secreto(prompt):
    # getpass puede caer en entrada con eco: se cancela en ese caso.
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('error',getpass.GetPassWarning)
        return getpass.getpass(prompt)

def pedir_password():
    while True:
        password=leer_secreto('Nueva contraseña (12 a 1024 caracteres): ')
        if len(password)<12 or len(password)>1024 or es_password_fabrica(password):
            print('Elegí una contraseña propia de al menos 12 caracteres.');continue
        if not hmac.compare_digest(password,leer_secreto('Repetir contraseña: ')):
            print('Las contraseñas no coinciden.');continue
        return password

def pedir_pin():
    while True:
        pin=leer_secreto('Nuevo PIN de cancelación (6 a 12 dígitos): ')
        if not re.fullmatch(r'[0-9]{6,12}',pin) or len(set(pin))==1:
            print('Elegí de 6 a 12 dígitos, sin repetir siempre el mismo.');continue
        if not hmac.compare_digest(pin,leer_secreto('Repetir PIN: ')):
            print('Los PIN no coinciden.');continue
        return pin

def pedir_alta_inicial():
    print('Configuración inicial: no hay contraseña ni PIN de fábrica.')
    while True:
        username=input('Nombre de usuario administrador: ').strip()
        if username and len(username)<=80:break
        print('Ingresá un nombre de usuario de hasta 80 caracteres.')
    return username,hash_password(pedir_password()),pedir_pin()
