import sys
import json

donors = dict()
donors['year'] = sys.argv[1]
donors['donors'] = []

lines = sys.stdin.readlines()
for i in range(0, len(lines), 4):
    d = dict()
    d['name'] = lines[i]
    d['address'] = ''.join(lines[i+1:i+3])
    donors['donors'].append(d)

json.dump(donors, sys.stdout, indent=4, ensure_ascii=False)
