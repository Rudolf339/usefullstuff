#convert FlightGear checklist.xml files to easy to read .txt
#Author: Rudolf

#usage:
#python3 path/to/checkgen.py path/to/checklist.xml > outputfile.txt

import xml.etree.ElementTree as ET
import sys

e = ET.parse(str(sys.argv[1]))
root = e.getroot()

def items(pg, il):    
    for l in pg.findall('item'):
        #to avoid error due to empty tags
        try:
            print('\t' * il + l.find('name').text + '\t -- \t' +
            l.find('value').text)
        except:
           pass
    print()

def pages(cl, il):
    for p in cl.findall('page'):
        items(p, il + 1)

for cl in root:
    if False:
        #cl.find('group') is None:
        print(cl.find('title').text, '\n')
        if cl.find('page') is None:    
            items(cl, 1)
        else:
            pages(cl, 1)
    else:
        for c in cl.findall('checklist'): 
            if c.find('page') is None:
                print('\t', c.find('title').text)
                items(c, 2)
            else:
                print('\t', c.find('title').text)
                pages(c, 1)
