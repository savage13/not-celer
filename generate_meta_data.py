#!/usr/bin/env python3

import json

names = json.load(open("names.json", "r"))
locations = json.load(open("LocationMarker.json","r"))
data = json.load(open("raw_towers.json", "r"))
towers = {}
shrines = {}
koroks = {}
frogs = {}
addisons = {}
lightroot = {}
caves = {}
wells = {}
for r in data:
    name = locations[r["Location"]]
    key = name.replace(" ", "").replace("SkyviewTower", "")
    towers[key] = {
        "pos": r['pos'], "Location": r["Location"],
        "DisplayName": name, "hash_id": r["hash_id"],
    }
tmp = json.load(open("raw_crystals.json", "r"))
crystals = {x['DungeonNum']: x for x in tmp}
data = json.load(open("raw_shrines.json", "r"))
for r in data:
    name = locations[r["Location"]]
    key = name.replace(" ", "").replace("Shrine", "")
    if not r['Location'].startswith('Dungeon'):  # Skip Shrine Island and Shrine of Ressurection
        print(r['Location'])
        continue
    shrines[key] = {
        "pos": r['pos'], "Location": r["Location"],
        "DisplayName": name, "hash_id": r["hash_id"],
    }
    if r['Location'] in crystals:
        shrines[key]['Start'] = crystals[r['Location']]

for file in ["raw_korok.json"]:
    data = json.load(open(file, "r"))
    for r in data:
        name = r['korok_id']
        koroks[name] = {
            "pos": r['pos'], "korok_type": r['korok_type'],
            "DisplayName": name, "hash_id": r["hash_id"],
        }
for k,v in json.load(open("raw_korok3.json", "r")).items():
    koroks[k] = v

data = json.load(open("raw_addison.json", "r"))
k = 0
for r in data:
    name = f"A{k:02d}"
    addisons[name] = { "pos": r['pos'], "DisplayName": name, "hash_id": r["hash_id"], }
    k += 1
data = json.load(open("raw_lightroot.json", "r"))
for r in data:
    name = locations[r["Location"]]
    key = name.replace(" ", "").replace("Lightroot", "")
    lightroot[key] = { "pos": r['pos'], "DisplayName": name, "hash_id": r["hash_id"], }
data = json.load(open("raw_caves.json", "r"))
keys = {}
for r in data:
    name = locations[r["Location"]]
    key = name.replace(" ", "").replace("Cave", "")
    if not key in keys:
        keys[key] = 0
    key0 = key + f"{keys[key]:02d}"
    keys[key] += 1
    if key0 in caves:
        print("multiple caves", key0)
    caves[key0] = { "pos": r['pos'], "DisplayName": name, "hash_id": r["hash_id"] }
data = json.load(open("raw_wells.json", "r"))
for r in data:
    name = locations[r["Location"]]
    if name.endswith("Shrine"):
        continue
    key = name.replace(" ", "").replace("Well", "")
    if key in wells:
        print("multiple wells", key)

    wells[key] = { "pos": r['pos'], "DisplayName": name, "hash_id": r["hash_id"], }

def transform(file, func):
    data = json.load(open(file, "r"))
    out = {}
    state = {}
    for i, r in enumerate(data):
        [name, key, state] = func(r, i, state)
        if key in out:
            keys = [k for k in out.keys() if k.startswith(key)]
            key = f'{key}_{len(keys):02d}'
            if key in out:
                raise ValueError('duplicate key detected', key)
        out[key] = { "pos": r['pos'], "DisplayName": name, "hash_id": r["hash_id"], }
        if r.get('Location'):
            out[key]['Location'] = r.get('Location')
    return out

def frox_t(r, k, state):
    name = f"{k:02d}"
    return [name, name, state]
def frog_t(r, k, state):
    name = names[r['name']]
    if r.get('Id'):
        key = r.get('Id')
    else:
        key = r['Location'].replace(" ", "")
    return [name, key, state]
def npcs_t(r, k, state):
    special = {
        'Npc_Zelda_Black_Event': {
            'name': 'Npc_Zelda_Black_Event'
        },
        'Npc_BaseCamp_Rito012_Simplify': {
            'name': 'Npc_BaseCamp_Rito012_Simplify',
        },
        'Npc_BaseCamp_Rito010_Simplify': {
            'name': 'Npc_BaseCamp_Rito010_Simplify',
        },
        'Npc_Ichikara_Gerudo_Demo': {
            'name': 'Npc_Ichikara_Gerudo_Demo',
        },
        'Npc_Zelda_Black_Chase': {
            'name': 'Npc_Zelda_Black_Chase',
        },
    }
    name = names.get(r['name'])
    if name is None:
        name = special[r['name']]['name']
    key = name
    if r['name'] in special:
        key = special[r['name']].get(r['hash_id'])
        if key is None:
            key = name
    return [name, key, state]
def chasm_t(r, k, state):
    print(r['Location'])
    name = locations[r['Location']]
    key = name
    key = key.replace(" ", "").replace("Chasm", "")
    key = key.replace("'", "")
    return [name, key, state]

frox = transform('raw_frox_locations.json', frog_t)
hinox = transform('raw_hinox_locations.json', frog_t)

talus = transform('raw_talus_location.json', frog_t)
gleeoks = transform('raw_gleeoks_location.json', frog_t)
flux = transform('raw_flux_location.json', frog_t)
frogs = transform("raw_bubbulfrog_cave.json", frog_t)
molduga = transform('raw_molduga_location.json', frog_t)
chasms = transform('raw_chasm.json', chasm_t)
npcs = transform('raw_npcs.json', npcs_t)

extra = json.load(open("raw_npcs_extra.json", "r"))
for key, value in extra.items():
    if key in npcs:
        raise ValueError('key already exists in npcs', key)
    npcs[key] = value

out = {
    "ROA": {
        "DisplayName": "Room of Awakening",
        "pos": [370, 2281, 1753],
        "hash_id": '0x15b3d2803fbb4659',
    },
    "SOR": {
        "DisplayName": "Shrine of Ressurections",
        "pos": [ -1061.88, 247.67, 1829.55],
        "hash_id": '0x89f2b2ddfdd48294',
    },
    "Tower": towers,
    "Shrine": shrines,
    "Korok": koroks,
    "Bubbulfrog": frogs,
    "Addison": addisons,
    "Lightroot": lightroot,
    "Cave": caves,
    "Chasm": chasms,
    "Well": wells,
    "Enemy": {
        "Frox": frox,
        "Hinox": hinox,
        "FluxConstruct": flux,
        "Gleeok": gleeoks,
        "Molduga": molduga,
        "Talus": talus
    },
    "Chest": {},
    "Equipment": {
        "Weapon": {},
        "Bow": {},
        "Shield": {},
    },
    "Dispenser": {},
    "Location": {},
    "Memory": {},
    "Material": {},
    "Item": {},
    "Npc": npcs,
    "TechLab": {
        "Hateno": {
            "pos": [3777.71, 335.31, 2127.36],
            "hash_id": "0x69e2b123da91ebdb",
            "DisplayName": "Hateno Ancient Tech Lab",
        }
    },
    "_icons": {
        "Npc": {
            "iconUrl": "npc.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "Item": {
            "iconUrl": "item.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
            "displayString": "${key} ${txt}",
        },
        "Dispenser": {
            "iconUrl": "dispenser.png",
            "iconSize": [24,24],
            "iconAnchor": [12,12],
            "routeSize": [24,24],
            "displayString": "${key}"
        },
        "Memory": {
            "iconUrl": "memory.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "Location": {
            "iconUrl": "location.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "Enemy": {
            "iconUrl": "bokoSit.png",
            "iconSize": [24,24],
            "iconAnchor": [12,12],
            "routeSize": [24,24],
            "Frox": {
                "iconUrl": "enemy.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Hinox": {
                "iconUrl": "enemy.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "FluxConstruct": {
                "iconUrl": "enemy.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Gleeok": {
                "iconUrl": "enemy.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Molduga": {
                "iconUrl": "enemy.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Talus": {
                "iconUrl": "enemy.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
        },
        "Korok": {
            "iconUrl": "mapicon_korok.png",
            "canvas": True,
            "iconSize": [19,20],
            "iconAnchor": [9, 10],
            "routeSize": [20,20],
            "displayString": "${txt} ${meta.korok_type}",
            "Start": {
                "iconUrl": "korok_backpack.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            }
        },
        "Shrine": {
            "iconUrl": "shrine.png",
            "iconSize": [32, 32],
            "iconAnchor": [18, 18],
            "routeSize": [32,32],
            "Start": {
                "iconUrl": "crystal.png",
                "iconSize": [32, 32],
                "iconAnchor": [18, 18],
                "routeSize": [26,26],
                "displayString": "Shrine Crystal",
            }
        },
        "Tower": {
            "iconUrl": "tower.png",
            "iconSize": [32, 32],
            "iconAnchor": [20, 20],
            "routeSize": [32,32],
        },
        "Lightroot": {
            "iconUrl": "lightroot.png",
            "iconSize": [32, 32],
            "iconAnchor": [20, 20],
            "routeSize": [32,32],
        },
        "Cave": {
            "iconUrl": "cave.png",
            "canvas": True,
            "iconSize": [25, 25],
            "iconAnchor": [12, 12],
            "routeSize": [24,24],
        },
        "Chasm": {
            "iconUrl": "chasm.png",
            "canvas": True,
            "iconSize": [25, 25],
            "iconAnchor": [12, 12],
            "routeSize": [24,24],
        },
        "Well": {
            "iconUrl": "well.svg",
            "iconSize": [25, 25],
            "iconAnchor": [12, 12],
            "routeSize": [24,24],
        },
        "Bubbulfrog": {
            "iconUrl": "frog.png",
            "iconSize": [25, 25],
            "iconAnchor": [12, 12],
            "routeSize": [24,24],
        },
        "Addison": {
            "iconUrl": "sign.png",
            "iconSize": [25, 25],
            "iconAnchor": [12, 12],
            "routeSize": [24,24],
            "displayString": "Addison ${txt}",
        },
        "Chest": {
            "iconUrl": "chest.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "Material": {
            "iconUrl": "material.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [24,24],
        },
        "Equipment": {
            "Bow": {
                "iconUrl": "bow.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 16],
                "routeSize": [32,32],
            },
            "Weapon": {
                "iconUrl": "equipment.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 16],
                "routeSize": [32,32],
            },
            "Shield": {
                "iconUrl": "shield.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 16],
                "routeSize": [32,32],
            },
        },
        "Warp": {
            "iconUrl": "warp.png",
            "iconSize": [28, 28],
            "iconAnchor": [16, 16],
            "routeSize": [24,24],
        },
        "SOR": {
            "iconUrl": "special.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "ROA": {
            "iconUrl": "special.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "TechLab": {
            "iconUrl": "mapicon_labo.svg",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        }
    }
}
with open("celer_totk_metadata.json", "w") as f:
    json.dump(out, f, indent = 2)
#for v in sorted(shrines.keys()):
#    print(v)
