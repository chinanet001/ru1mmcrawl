from json import loads as jloads

ids = []
with open('items.json') as fp:
    desc = jloads(fp.read())
    for item in desc:
        ids.append(int(item['urlid']))

print ids.sort()
print ids
