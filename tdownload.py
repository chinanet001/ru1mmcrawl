import sys
from json import loads as jloads
from os import makedirs, system
from os.path import dirname, abspath, exists as pathexists

CURDIR = abspath('.')

class ItemDownloader(object):
    def __init__(self, item):
        self.item = item

    def do(self):
        droot = '%s/downloads/%s' % (CURDIR, self.item['urlid'])
        print droot
        if self.item['dpath'].endswith('/plans'):
            self.log('omit %s\n' % self.item['urlid'])
            return True
        if not pathexists(droot):
            makedirs(droot)

        if 0 != system('wget -P %s %s' % (droot, self.item['cover'])):
            return False
        if 0 != system('axel -an5 -o %s %s' % (droot, self.item['dpath'])):
            return False
        return True

    def log(self, msg):
        sys.stderr.write(msg)

if __name__ == '__main__':
    with open('items.json') as fp:
        items = jloads(fp.read())

    errrecord = open('err.csv', 'wt')
    for item in items:
        der = ItemDownloader(item)
        if der.do():
            sys.stderr.write('success %s' % item['urlid'])
        else:
            errrecord.write(',%s' % item[urlid])
            errrecord.flush()

    errrecord.close()
    print('finished')
