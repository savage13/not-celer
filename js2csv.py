#!/usr/bin/env python3

import sys
import json

data = json.load(open(sys.argv[1],"r"))
keys = list(data[0].keys())
keys.remove("drop")
keys.remove("pos")
keys.extend(['x','y','z'])
print(",".join(keys))
for r in data:
    r['x'] = r['pos'][0]
    r['y'] = r['pos'][1]
    r['z'] = r['pos'][2]
    print(",".join( [str(r[key]) for key in keys] ))
        
