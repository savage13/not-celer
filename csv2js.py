#!/usr/bin/env python3

import sys
import json
import csv

data = []
with open(sys.argv[1],"r") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        row['pos'] = [float(row[v]) for v in ['x','y','z']]
        del row['x']
        del row['y']
        del row['z']
        data.append(row)

print(json.dumps(data, indent=2))
