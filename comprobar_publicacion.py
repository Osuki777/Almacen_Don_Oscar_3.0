#!/usr/bin/env python3
"""Local pattern check; no networking or secret-value output. Not a security audit."""
import argparse, io, json, re, subprocess, sys, zipfile
from pathlib import Path

RULES = {
 'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----'),
 'github_token': re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
 'aws_access_key': re.compile(rb'AKIA[0-9A-Z]{16}'),
 'google_api_key': re.compile(rb'AIza[0-9A-Za-z_-]{35}'),
 'slack_token': re.compile(rb'xox[baprs]-[A-Za-z0-9-]{20,}'),
 'stripe_live_key': re.compile(rb'sk_live_[A-Za-z0-9]{20,}'),
}
SENSITIVE = {'.keystore','.jks','.p12','.pfx','.pgbackup','.pgenc','.backup','.db','.sqlite','.sqlite3'}
SKIP = {'.git','node_modules','.gradle','build','__pycache__'}
MAX_FILE = 32*1024*1024
MAX_TOTAL = 256*1024*1024

class Scanner:
 def __init__(self): self.findings=[];self.count=0;self.total=0
 def report(self,path,kind): self.findings.append({'path':path,'type':kind})
 def scan(self,name,data,depth=0):
  self.count+=1;self.total+=len(data)
  if len(data)>MAX_FILE or self.total>MAX_TOTAL:
   self.report(name,'limite_de_lectura_requiere_revision');return
  leaf=Path(name.split('!')[-1]).name.lower()
  if Path(leaf).suffix in SENSITIVE or leaf in ['.env','key.properties','keystore.properties'] or leaf.startswith('.env.') and not leaf.endswith(('.example','.sample','.template')): self.report(name,'archivo_potencialmente_privado')
  for kind,rule in RULES.items():
   if rule.search(data):self.report(name,kind)
  if data[:4]==b'PK\x03\x04':
   if depth>=5:self.report(name,'archivo_anidado_requiere_revision');return
   try:
    with zipfile.ZipFile(io.BytesIO(data)) as z:
     for item in z.infolist():
      if item.is_dir():continue
      if item.file_size>MAX_FILE or self.total+item.file_size>MAX_TOTAL:self.report(name+'!'+item.filename,'limite_de_lectura_requiere_revision');continue
      if item.flag_bits&1:self.report(name+'!'+item.filename,'archivo_cifrado_no_inspeccionado');continue
      self.scan(name+'!'+item.filename,z.read(item),depth+1)
   except (zipfile.BadZipFile,RuntimeError,NotImplementedError,ValueError):self.report(name,'archivo_no_inspeccionado')
  if leaf.endswith(('.bundle','.7z','.rar','.tar','.gz')):self.report(name,'contenedor_requiere_revision_especifica')
 def tree(self,root):
  for f in sorted(root.rglob('*')):
   if not f.is_file() or any(p in SKIP for p in f.relative_to(root).parts):continue
   if f.is_symlink():self.report(str(f.relative_to(root)),'enlace_requiere_revision');continue
   if f.stat().st_size>MAX_FILE:self.report(str(f.relative_to(root)),'limite_de_lectura_requiere_revision');continue
   self.scan(str(f.relative_to(root)),f.read_bytes())
 def history(self,root):
  entries=subprocess.check_output(['git','-C',str(root),'rev-list','--objects','--all'],stderr=subprocess.DEVNULL).splitlines()
  for line in entries:
   parts=line.split(b' ',1)
   if len(parts)!=2:continue
   oid,path=parts
   kind=subprocess.check_output(['git','-C',str(root),'cat-file','-t',oid.decode()],stderr=subprocess.DEVNULL).strip()
   if kind!=b'blob':continue
   size=int(subprocess.check_output(['git','-C',str(root),'cat-file','-s',oid.decode()],stderr=subprocess.DEVNULL))
   name='git:'+oid.decode()[:12]+':'+path.decode(errors='replace')
   if size>MAX_FILE:self.report(name,'limite_de_lectura_requiere_revision');continue
   self.scan(name,subprocess.check_output(['git','-C',str(root),'cat-file','blob',oid.decode()],stderr=subprocess.DEVNULL))

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',nargs='?',default='.');parser.add_argument('--history',action='store_true',help='Revisar objetos alcanzables por todas las referencias locales de Git');args=parser.parse_args()
 s=Scanner();root=Path(args.directory).resolve();s.tree(root)
 if args.history:
  try:s.history(root)
  except (subprocess.CalledProcessError,FileNotFoundError):s.report('git','historial_no_inspeccionado')
 print(json.dumps({'files_inspected':s.count,'history_requested':args.history,'findings':s.findings,'scope':'Patrones y nombres de archivo; no detecta todos los secretos, datos personales, imágenes ni defectos de seguridad.'},ensure_ascii=False,indent=2))
 return 1 if s.findings else 0
if __name__=='__main__':sys.exit(main())