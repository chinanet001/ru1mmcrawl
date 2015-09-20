from urlparse import urlparse
from os.path import basename
from json import loads as jloads

content = ''
ids = []
with open('items.json') as fp:
    desc = jloads(fp.read())
    for item in desc:
        if item['dpath'].endswith('/plans'): continue
        content += '\n<img src="%s" />' % item['cover']
        content += '\n<a href="%s">%s</a>' % ('http://www.ru1mm.com/album/view/%s' % item['urlid'], item['urlid'])
        content += '\n<a href="%s">%s</a>' % (item['dpath'], basename(urlparse(item['dpath']).path))
        ids.append(int(item['urlid']))

with open('items.html', 'wt') as fp:
    fp.write('''<html>
<head>
<title>ru1mm list</title>
</head>
<body>
%s
</body>
''' % content)
