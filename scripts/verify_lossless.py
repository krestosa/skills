#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]/'shared'
idx=json.loads((ROOT/'manifests/source-index.json').read_text())
errors=[]
for item in idx['sources']:
 raw=(ROOT/item['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=item['sha256']: errors.append('source manifest '+item['path'])
 src=json.loads(raw); data=(ROOT/src['path']).read_bytes(); cursor=0; chunks=[]
 if len(data)!=src['bytes'] or hashlib.sha256(data).hexdigest()!=src['sha256']: errors.append('source '+src['path'])
 for sec in src['sections']:
  if sec['startByte']!=cursor: errors.append('coverage '+src['path']+' '+sec['id'])
  chunk=data[sec['startByte']:sec['endByte']]; chunks.append(chunk); cursor=sec['endByte']
  if len(chunk)!=sec['bytes'] or hashlib.sha256(chunk).hexdigest()!=sec['sha256']: errors.append('section '+sec['id'])
 if cursor!=len(data) or b''.join(chunks)!=data: errors.append('rebuild '+src['path'])
if errors:
 print('LOSSLESS: FAIL'); [print('-',x) for x in errors]; sys.exit(1)
print('LOSSLESS: PASS'); print('sources:',len(idx['sources'])); print('text_mutations: 0')
