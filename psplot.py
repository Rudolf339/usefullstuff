#!/usr/bin/env python3

# plot out orthos is a scenery direcectory
# Usage:
# cd into your scenery direcectory (outside Orthophotos/)
# run index_scraper.sh to generate namelist.txt
# run psplot.py

from matplotlib import pyplot
import math


def width(lat):
    lat = abs(lat)
    if lat >= 89:
        return 12
    if lat >= 86:
        return 4
    if lat >= 83:
        return 2
    if lat >= 71:
        return 1
    if lat >= 62:
        return 0.5
    if lat >= 22:
        return 0.25
    return 0.125


def coord2index(lat, lon):
    tile_width = width(lat)
    base_y = math.floor(lat)
    y = math.trunc((lat - base_y) * 8)
    base_x = math.floor(math.floor(lon / tile_width) * tile_width)
    x = math.floor((lon - base_x) / tile_width)
    print(tile_width, base_y, y, base_x, x)
    return ((lon + 180) << 14) + ((lat + 90) << 6) + (y << 3) + x


def index2coord(index):
    i = bin(index)
    x = int(i[-3:], 2)
    y = int(i[-6:-3], 2)
    lat = int(i[-14:-6], 2) - 90 + y * 0.125
    lon = int(i[2:-14], 2) - 180 + x * width(int(i[-14:-6], 2) - 90)
    return lat, lon


lat = []
lon = []
points = []
with open('./namelist.txt') as namelist:
    for i in namelist.readlines():
        i = int(i)
        coord = index2coord(i)
        points.append(coord)
        lat.append(coord[0])
        lon.append(coord[1])

legend = 'total number of tiles: ' + str(len(list(dict.fromkeys(points))))
pyplot.plot(lon, lat, 'bo', label=legend)
pyplot.xlabel('lon')
pyplot.xlim([-180, 180])
pyplot.ylabel('lat')
pyplot.ylim([-90, 90])
pyplot.legend()
pyplot.show()
