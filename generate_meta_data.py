#!/usr/bin/env python3

import json
import copy

names = json.load(open("names.json", "r"))
locations = json.load(open("LocationMarker.json","r"))
towers = {}
shrines = {}
koroks = {}
frogs = {}
addisons = {}
lightroot = {}
caves = {}
wells = {}
data = json.load(open("raw_towers.json", "r"))
for r in data:
    if r['Location'] == "DeepHole_B-6_Tower":
        continue
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

for file in ["raw_korok_with_trails.json"]:
    data = json.load(open(file, "r"))
    for k,v in data.items():
        v['DisplayName'] = v['korok_id']
        koroks[k] = v

for k,v in json.load(open("raw_korok3.json", "r")).items():
    v['DisplayName'] = v['korok_id']
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
    if name == "Komo Shoreline Cave":
        continue
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
def goddess_t(r, k, state):
    name = "Goddess Statue"
    key = f"{k:02d}"
    if names.get(r['name']):
        name = names.get(r['name'])
    return [name, key, state]
def chest_t(r, k, state):
    name = names[ r['drop']['value'][0] ]
    key = name.replace(" ", "").replace("'","").replace("-","")
    #print(key)
    return [name, key, state]
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
goddess = transform('raw_goddess_statue.json', goddess_t)
chests = transform('chest_armor.json', chest_t)
for value in chasms.values():
    value['Depths'] = copy.deepcopy(value)
    value['Depths']['pos'][1] = -512
    value['Depths']['DisplayName'] = f"{value['DisplayName']} Depths"

npcs = transform('raw_npcs.json', npcs_t)

extra = json.load(open("raw_npcs_extra.json", "r"))
for key, value in extra.items():
    if key in npcs:
        raise ValueError('key already exists in npcs', key)
    npcs[key] = value

oldmaps = transform("raw_old_map.json", frog_t)
sageswill = transform("raw_sage_will.json", frog_t)

def yiga_t(r, k, state):
    name = names[r['drop']['value'][0]]
    key = name.replace("-","").replace(" ","")
    return [name, key, state]

yiga = transform("raw_yiga_schematics.json", yiga_t)
stones = transform("raw_schema_stones.json", frog_t)

mappct = json.load(open('map_pct2.json', 'r'))

G,S,D = 0,0,0
dispenser = {}
for item in mappct['recycle box']:
    t = None
    if type(item['Trans'][0]) is dict:
        t = item['Trans'][0]['Trans']
    elif type(item['Trans'][0]) is list:
        t = item['Trans'][0]
    else:
        raise ValueError('getting position')
    name = ''
    if t[1] < 0:
        name = f'D{D:02d}'
        D += 1
    elif t[1] > 500:
        name = f'S{S:02d}'
        S += 1
    else:
        name = f'G{G:02d}'
        G += 1
    #print(name, t)
    dispenser[name] = {
        'pos': t, 
        'hash_id': item['hash_id'],
        'DisplayName': 'Device Dispenser',
        'flag': item['flag']
    }
tablets = {}
S = 0
for item in mappct['ancient stone tablets']:
    tablets[f'S{S:02d}'] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": "Ancient Tablet",
        'flag': item['flag']
    }
    S += 1
tears = {}
S = 0
for item in mappct['tears']:
    tears[f'G{S:02d}'] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": "Dragon Tears",
        'flag': item['flag']
    }
    S += 1
places = {}
for item in mappct['places']:
    key0 = item['ui_name'].replace(" ", "").replace("'","")
    n = 1
    key = key0
    while key in places:
        key = f"{key0}{n:02d}"
        n += 1

    places[key] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": item['ui_name'],
        'flag': item['flag']
    }

shops = {}
for item in mappct['important shops']:
    key0 = item['ui_name'].replace(" ", "").replace("-", "")
    n = 1
    key = key0
    while key in shops:
        key = f"{key0}{n:02d}"
        n += 1

    shops[key] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": item['ui_name'],
        'flag': item['flag']
    }
for item in mappct['shops']:
    key0 = item['ui_name'].replace(" ", "").replace("-","")
    n = 1
    key = key0
    while key in shops:
        key = f"{key0}{n:02d}"
        n += 1

    shops[key] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": item['ui_name'],
        'flag': item['flag']
    }

fairy = {}
for item in mappct['fairy']:
    key0 = item['ui_name'].replace(" ", "")
    n = 1
    key = key0
    while key in fairy:
        key = f"{key0}{n:02d}"
        n += 1

    fairy[key] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": item['name'],
        'flag': item['flag']
    }
special = {}
for item in mappct['warps']:
    name = item['ui_name']
    if name == "DgnObj_WarpPoint_Zonau_A_06":
        name = "CentralMineWarpPoint"
    special[name] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        'DisplayName': name,
        'flag': item['flag']
    }

xlocations = {}
for item in mappct['spots']:
    name0 = item['ui_name'].replace(" ", "").replace("'","").replace("-", "")
    name = name0
    n = 1
    while name in xlocations:
        name = f"{name0}{n:02d}"
        n += 1
    #print(item['hash_id'], name)
    if name in xlocations:
        raise ValueError('aargh')
    xlocations[name] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        "DisplayName": item['ui_name'],
        'flag': item['flag'],
    }
xlocations['EmergencyShelter'] = {
    "hash_id": "0xd02e649ed5deb358",
    "pos": [-254.00, 112.95, -98.00],
    "DisplaName": "Emergency Shelter",
    "Location": "BaseCamp_Shelter"
}

temps = {'0xeced362e8dbb109e': 'Lightning Temple',
         '0x7f43e8cce8e2bb29': 'Water Temple',
         '0xee51919128fd1da6': 'Wind Temple',
         '0xc34f654ff388119d': 'Fire Temple',
         '0x86a857fa8c9361a1': 'Spirit Temple',
         }

temples = {}
for item in mappct['temples']:
    name = temps[ item['hash_id'][0] ].replace(" Temple", "")
    temples[name] = {
        "hash_id": item['hash_id'][0],
        "pos": item['Trans'][0],
        'DisplayName': temps[ item['hash_id'][0] ],
        "AltDisplayName": item['ui_name'],
        'flag': item['flag'],
    }

quests = json.load(open("pancakes_list.json","r"))

side_adv = {}
i = 0
for item in quests['Side Adventures']:
    name = item['name']
    key = name.replace(" ", "").replace("!", "").replace("?", "").replace("-","").replace("'","").replace(":","").replace(",","")
    side_adv[key] = {
        "hash_id": f"0xSideAdv{i:02d}",
        "DisplayName": name,
        "notes": item['notes']
    }


    i += 1
main_quest = {}

for i, item in enumerate(quests["Main Quests"]):
    name = item['name']
    key = name.replace(" ", "").replace("!", "").replace("?", "").replace("-","").replace("'","").replace(":","").replace(",","")
    main_quest[key] = {
        "DisplayName": name,
        "hash_id": f"0xMainQuest{i:02d}",
    }

side_quest = {}
for i, item in enumerate(quests["Side Quests"]):
    name = item['name']
    key = name.replace(" ", "").replace("!", "").replace("?", "").replace("-","").replace("'","").replace(":","").replace(",","")
    if name.startswith("The Ancient City Gorondia"):
        key = name.replace(" ", "").replace("-","").replace("'","").replace(":","").replace(",","")
    side_quest[key] = {
        "DisplayName": name,
        "hash_id": f"0xSideQuest{i:03d}",
    }

    
key_items = {}
for i, item in enumerate(quests["Key Items"]):
    name = item['name']
    key = name.replace(" ", "").replace("!", "").replace("?", "").replace("-","").replace("'","").replace(":","").replace(",","").replace(")","").replace("(","")
    key_items[key] = {
        "DisplayName": name,
        "hash_id": f"0xKeyItem{i:02d}",
    }

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
    "SideAdv": side_adv,
    "MainQuest": main_quest,
    "SideQuest": side_quest,
    "KeyItem": key_items,
    "GoddessStatue": goddess,
    "Enemy": {
        "Frox": frox,
        "Hinox": hinox,
        "FluxConstruct": flux,
        "Gleeok": gleeoks,
        "Molduga": molduga,
        "Talus": talus
    },
    "Location": xlocations,
    "Fairy": fairy,
    "Shop": shops,
    "Place": places,
    "Special": special,
    "Tear": tears,

    "Temple": temples,
    "Tablet": tablets,
    "OldMap": oldmaps,
    "SagesWill": sageswill,
    "YigaSchema": yiga,
    "SchemaStone": stones,

    "Chest": chests,
    "Equipment": {
        "Weapon": {},
        "Bow": {},
        "Shield": {},
    },
    "Dispenser": dispenser,
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
        "OldMap": {
            "iconUrl": "oldmap.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "YigaSchema": {
            "iconUrl": "yigaschema.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "SchemaStone": {
            "iconUrl": "schemastone.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "SagesWill": {
            "iconUrl": "sageswill.png",
            "iconSize": [24,24],
            "iconAnchor": [12,12],
            "routeSize": [24,24],
        },
        "Tablet": {
            "iconUrl": "tablet.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
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
        "MainQuest": {
            "iconUrl": "MainQuest.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "SideAdv": {
            "iconUrl": "SideAdv.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "SideQuest": {
            "iconUrl": "SideQuest.png",
            "iconSize": [32,32],
            "iconAnchor": [16,16],
            "routeSize": [32,32],
        },
        "KeyItem": {
            "iconUrl": "star.png",
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
                "iconUrl": "frox.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Hinox": {
                "iconUrl": "hinox.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "FluxConstruct": {
                "iconUrl": "flux.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Gleeok": {
                "iconUrl": "gleeok.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Molduga": {
                "iconUrl": "molduga.png",
                "iconSize": [32,32],
                "iconAnchor": [16,16],
                "routeSize": [32,32],
                "displayString": "${txt} ${key}",
            },
            "Talus": {
                "iconUrl": "talus.png",
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
            },
            "1": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            },
            "2": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            },
            "3": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            },
            "4": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            },
            "5": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            }
            "6": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            }
            "7": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            }
            "8": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            }
            "9": {
                "iconUrl": "leaf.png",
                "iconSize": [28,28],
                "iconAnchor": [14, 14],
                "routeSize": [26,26],
            }
            "10": {
                "iconUrl": "leaf.png",
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
        "Special": {
            "iconUrl": "special.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "GoddessStatue": {
            "iconUrl": "stamina04.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
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
        },
        "Place": {
            "iconUrl": "location.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "Shop": {
            "iconUrl": "mapicon_shop_yorozu.svg",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "Fairy": {
            "iconUrl": "fairy.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "Tear": {
            "iconUrl": "tear.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
        "Temple": {
            "iconUrl": "temple.png",
            "iconSize": [32, 32],
            "iconAnchor": [16, 16],
            "routeSize": [32,32],
        },
    }
}
with open("celer_totk_metadata.json", "w") as f:
    json.dump(out, f, indent = 2)
