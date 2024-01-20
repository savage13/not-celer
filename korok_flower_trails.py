#!/usr/bin/env python

import json
import requests
from json import JSONEncoder

def gen_group(obj):
    map_type = obj['map_type']
    map_name = obj['map_name']
    hash_id = obj['hash_id']
    objs = requests.get(f'http://localhost:3008/obj/{map_type}/{map_name}/{hash_id}/gen_group').json()
    return objs
def ai_group(obj):
    map_type = obj['map_type']
    map_name = obj['map_name']
    hash_id = obj['hash_id']
    url = f'http://localhost:3008/obj/{map_type}/{map_name}/{hash_id}/ai_groups'
    return requests.get(url).json()

koroks = json.load(open("raw_korok.json", "r"))

ft5 = ['29a0_37f6', '196a_cb2f', '196a_c822', '196a_9cde', '53b7_0732']
ft10 = ['29a0_d827', '196a_3435', '196a_994b', '196a_95b8', '196a_7ed8',
        '196a_5af9', '196a_a1d9', '196a_68c7', '196a_d26c', '53b7_e9c4']

out = {}

for k in koroks:
    #print(_k)
    kid = k['korok_id']
    
    if k['korok_type'] != 'Flower Trail':
        out[kid] = k
        continue
    aig = ai_group(k)[0]
    ai = [r for r in aig['data']['References']]
    is5 = 'TrackingFlower_05' in aig['data']['Logic'] 
    gg = gen_group(k)
    ft = ft5
    if not is5 :
        ft = ft10
    refs2 = []
    for ift in ft:
        p = next(r for r in ai if r['Id'] == 'AiGroup' and r['InstanceName'].endswith(ift))
        path = p['Path'].split("/")[0]
        r = next(r for r in ai if r['Id'].startswith('Obj_Plant_Korok') and r['Path'].startswith(path))
        hash_id = f"0x{int(r['Reference']):016x}"
        g = next(g for g in gg if g['hash_id'] == hash_id)
        refs2.append(g)
    for i,r in enumerate(refs2):
        print(f"_Korok::{kid}::{i+1}", r['pos'])
        r['DisplayName'] = f"{kid} {i+1}"
        r['korok_type'] = 'Flower Trail'
        id = i + 1
        k[id] = r
    out[kid] = k

json.dump(out, open("raw_korok_with_trails.json", "w"))
