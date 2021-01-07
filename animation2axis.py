import math

with open('/home/domokos/AircraftWIP/A-6E/Models/A-6E-model.xml') as ipf:
    inputFile = ipf.readlines()
of = open('./A-6E-model-axis.xml', 'w+')
ac = open('./A-6E-axis.ac', 'w+')


def dataExtract(line, tags):
    for tag in tags:
        if tag in line:
            num = ''
            isNum = False
            for c in line:
                if c == '<':
                    isNum = False
                elif isNum:
                    num += c
                if c == '>':
                    isNum = True
            return (tag, float(num))


class axis:
    def __init__(self, name, x1, y1, z1, x2, y2, z2):
        self.name = name
        self.x1 = float(x1)
        self.y1 = float(- y1)
        self.z1 = float(z1)
        self.x2 = float(x2)
        self.y2 = float(- y2)
        self.z2 = float(z2)

    def __str__(self):
        final = 'OBJECT poly\n'
        final += 'name "' + self.name + '"\n'
        final += 'data 4\ncrease 40.0\nnumvert 2\n'
        final += str(self.x1) + ' ' + str(self.z1) + ' ' + str(self.y1) + '\n'
        final += str(self.x2) + ' ' + str(self.z2) + ' ' + str(self.y2) + '\n'
        final += 'numsurf 1\n'
        final += 'SURF 0x01\n'
        final += 'mat 0\n'
        final += 'refs 2 \n'
        final += '0 0 0\n'
        final += '1 0 0\n'
        final += 'kids 0\n'
        return final

    def printRaw(self):
        print(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)


axisList = []

searchType = None
entries = dict()
current_center = {'x': 0, 'y': 0, 'z': 0}
for line in inputFile:
    if searchType is None:
        outputLine = line

    if (('</center>' in line or '</axis>' in line or '</offsets>' in line) and
            searchType is not None):
        if searchType == 'center':
            current_center['x'] = entries['<x-m>']
            current_center['y'] = entries['<y-m>']
            current_center['z'] = entries['<z-m>']
        if searchType == 'offsets':
            coords = rotate(entries['<x-m>'], entries['<z-m>'], alpha, zoffset)
            of.write('<x-m>' + str(- coords['x']) + '</x-m>\n')
            of.write('<y-m>' + str(entries['<y-m>']) + '</y-m>\n')
            of.write('<z-m>' + str(- coords['z']) + '</z-m>\n')
            if '<pitch-deg>' in entries:
                of.write('<pitch-deg>' + str(entries['<pitch-deg>'] + alpha) + '</pitch-deg>\n')
            if '<roll-deg>' in entries:
                of.write('<roll-deg>' + str(entries['<roll-deg>'] + alpha) + '</roll-deg>\n')
            if '<yaw-deg>' in entries:
                of.write('<yaw-deg>' + str(entries['<yaw-deg>'] + alpha) + '</yaw-deg>\n')
        if searchType == 'axis':
            if '<x>' in entries:
                axisList.append(axis('axis' + str(len(axisList)),
                                     current_center['x'] + entries['<x>'],
                                     current_center['y'] + entries['<y>'],
                                     current_center['z'] + entries['<z>'],
                                     current_center['x'],
                                     current_center['y'],
                                     current_center['z']))
                axisList[len(axisList) - 1].printRaw()
                print(current_center)
                print(entries['<x>'], entries['<y>'], entries['<z>'])
                current_center = {'x': 0, 'y': 0, 'z': 0}
                of.write('<object-name>axis' +
                         str(len(axisList) - 1) +
                         '</object-name>\n')
            else:
                axisList.append(axis('axis' + str(len(axisList)),
                                     entries['<x1-m>'], entries['<y1-m>'],
                                     entries['<z1-m>'], entries['<x2-m>'],
                                     entries['<y2-m>'], entries['<z2-m>']))
                of.write('<object-name>axis' +
                         str(len(axisList) - 1) +
                         '</object-name>\n')
        entries = dict()
        if searchType != 'center':
            outputLine = line
        searchType = None
    else:
        if searchType == 'center':
            data = dataExtract(line, ['<x-m>', '<y-m>', '<z-m>'])
            # print(line, data)
            entries[data[0]] = data[1]
        elif searchType == 'axis':
            data = dataExtract(line, ['<x>', '<y>', '<z>',
                                      '<x1-m>', '<y1-m>', '<z1-m>',
                                      '<x2-m>', '<y2-m>', '<z2-m>'])
            # print(line, data)
            entries[data[0]] = data[1]
        elif searchType == 'offsets':
            data = dataExtract(line, ['<x-m>', '<y-m>', '<z-m>',
                                      '<pitch-deg>', '<roll-deg>',
                                      '<yaw-deg>'])
            # print(line, data)
            entries[data[0]] = data[1]
    if '<center>' in line:
        searchType = 'center'
        outputLine = ''
    elif '<axis>' in line:
        searchType = 'axis'
    elif '<offsets>' in line:
        # searchType = 'offsets'
        pass

    of.write(outputLine)
    outputLine = ''


ac.write('AC3Db\n')
ac.write('MATERIAL "ac3dmat1" rgb 1 1 1  amb 1 1 1  emis 0 0 0  spec 0 0 0  shi 10  trans 0\n')
ac.write('OBJECT world\n')
ac.write('name "A-6E-axis.ac"\n')
ac.write('kids ' + str(len(axisList)) + '\n')
for a in axisList:
    ac.write(str(a))
ac.close()
of.close()
