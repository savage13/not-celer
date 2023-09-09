#!/usr/bin/env python3

import json
import requests

data = json.load(open("raw_crystals.json", "r"))

for v in data:
    url = f"http://localhost:3008/obj/{v['objid']}"
    x = requests.get(url).json()
    num = x['data']['Dynamic']['DungeonIndexStr']
    print(v['name'], num)
    v['DungeonNum'] = num

json.dump(data, open("raw_crystals.json", "w"), indent=2)
