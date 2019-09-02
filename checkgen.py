#convert FlightGear checklist.xml files to easy to read .txt
#Author: Rudolf

#usage:
#python3 path/to/checkgen.py path/to/checklist.xml > outputfile.txt

import xml.etree.ElementTree as ET
import sys

e = ET.parse(str(sys.argv[1]))
root = e.getroot()

for cl in root:
    print(cl.find('title').text)
    for l in cl.findall('item'):
        try:
            print('\t' + l.find('name').text + '\t -- \t' +
              l.find('value').text)
        except:
            pass

