#!/usr/bin/env python

import json
import copy
import requests


data = json.load(open("raw_korok2.json","r"))

out = {}

for v in data:
    url = f"http://localhost:3008/obj/{v['objid']}"
    x = requests.get(url).json()
    url = f"http://localhost:3008/obj/MainField/{x['map_name']}/{x['hash_id']}/gen_group"
    gg = requests.get(url).json()
    end = None
    for g in gg:
        if g['name'] == 'KorokCarry_Destination':
            #print(g['hash_id'], g['name'])
            end = g
            break
    korok_id = v['korok_id']
    v['DisplayName'] = korok_id
    out[korok_id] = copy.deepcopy(v)
    v['DisplayName'] = f"{korok_id} Start"
    out[korok_id]['Start'] = copy.deepcopy(v)
    end['DisplayName'] = f"{korok_id} End"
    end['korok_type'] = v['korok_type']
    out[korok_id]['End'] = end

json.dump(out, open("raw_korok3.json", "w"), indent=2)
