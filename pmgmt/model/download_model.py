#!/usr/bin/env python
import requests
import codecs
import pkg_resources
import os
import pmgmt
base_url = 'https://docs.google.com/spreadsheet/pub?key=0AttCeOvLP6XMdG82NHZfSEJJOGdQTkgzb05aRjkzMEE'
categories = {
    'ParameterDefs.csv'           : '%s&single=true&gid=57&output=csv'% base_url,
    'ParameterDictionary.csv'     : '%s&single=true&gid=58&output=csv'% base_url,
}

def get(cat):
    fpath = os.path.join(pkg_resources.resource_filename(pmgmt.__name__,'resources'),cat)
    print 'Getting ', fpath
    with codecs.open(fpath,'w', 'utf-8') as f:
        r = requests.get(categories[cat])
        f.write(r.text)
def main():
    import sys
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg in categories:
                get(arg)

    else:
        for k in categories.iterkeys():
            get(k)


if __name__ == '__main__':
    main()




