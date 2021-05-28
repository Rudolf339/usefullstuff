#!/usr/bin/python3
# TronView to fgfp conversion tool
# Author:  Jüttner Domokos aka Rudolf
# License: GPLv2

# Requires OSM2CITY to be in your path
# import the exported .txt (actually json) file
# waypoints that are radio beacons must be named by the codename of the beacon
# waypoints with 'navaid' in the remarks will be identified as radio beacons
# departure/destination should be noted by naming waypoint as ICAO code and
# adding departure/destination to the remarks

# tronview2fgfp TronView_scenario.txt
# output:
# TronView_scenario_{n}.fgfp routes 1-5
# TronView_scenario_line_{name}.fgfp

import json
import argparse
import fgfp

try:
    from osm2city.utils.utilities import FGElev
    fg_elev = FGElev(None, 0)
    OSM = True
except ModuleNotFoundError:
    OSM = False
    

parser = argparse.ArgumentParser()
parser.add_argument('ipf')
args = parser.parse_args()

with open(args.ipf, 'r') as input_file:
    tron = json.load(input_file)


# Routes 1-5
routes = [{'wp': []}, {'wp': []}, {'wp': []},
          {'wp': []}, {'wp': []}, {'wp': []}]
routes_raw = tron['data']['scenario']['steerpoints']
for wp in routes_raw:
    point = fgfp.waypoint()
    ap = False
    if 'remarks' in wp:
        if 'navaid' in wp['remarks']:
            point.navaid(wp['title'], wp['position']['latitude'],
                         wp['position']['longitude'],
                         wp['elevation'])
        elif 'departure' in wp['remarks']:
            routes[wp['route']]['departure'] = wp['title']
            ap = True
        elif 'destination' in wp['remarks']:
            routes[wp['route']]['destination'] = wp['title']
            ap = True
        else:
            if OSM:
                alt = fg_elev.probe_elev((wp['position']['longitude'],
                                          wp['position']['latitude']), True)
                point.coord(wp['title'], wp['position']['latitude'],
                            wp['position']['longitude'], alt)
            else:
                point.coord(wp['title'], wp['position']['latitude'],
                            wp['position']['longitude'])
    else:
        if OSM:
            alt = fg_elev.probe_elev((wp['position']['longitude'],
                                      wp['position']['latitude']), True)
            point.coord(wp['title'], wp['position']['latitude'],
                        wp['position']['longitude'], alt)
        else:
            point.coord(wp['title'], wp['position']['latitude'],
                        wp['position']['longitude'])
    if not ap:
        routes[wp['route']]['wp'].append(point)

for r in range(1, len(routes)):
    route = routes[r]
    if route['wp'] != []:
        fp = fgfp.fgfp()
        if 'departure' in route:
            fp.departure['airport'] = route['departure']
        if 'destination' in route:
            fp.destination['airport'] = route['destination']
        fp.route = route['wp']
        with open(args.ipf[:-4] + '_' + str(r) + '.fgfp', 'w+') as opf:
            for line in fp.parse():
                opf.write(line)

# lines
lines_raw = tron['data']['scenario']['lines']
for line in lines_raw:
    cl = fgfp.fgfp()
    n = 1
    for point in line['points']:
        cl.route.append(fgfp.waypoint().coord(str(n),
                                              point['latitude'],
                                              point['longitude']))
    name = args.ipf[:-4] + '_line_' + str(line['title']) + '.fgfp'
    n += 1
    with open(name, 'w+') as opf:
        for i in cl.parse():
            opf.write(i)
