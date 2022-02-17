import pandas as pd
import numpy as np
import os
import json
import datetime
from bgt_reader import get_properties, WMTS_calculator, bgt_classifier
from helpers import wgs_to_rd
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from ahn_reader import get_height, get_treeheight
from interpolation import interpolate, intersect
from cityjson_converter import to_cityJSON
from exceptions import crown_unknown, bgt_unknown
from treedict import tree_properties

def main(tree, year, mesh):
    '''for 1 tree'''

    # retrieve tree id
    tree_number = tree['Boomnummer']
    # use object number if tree number is unknown (=0)
    if tree_number == 0:
        tree_number = 'objNR_' + str(tree['OBJECTNUMMER'])
    print('tree_number', tree_number)

    # read out name and type
    name = tree['Soortnaam_WTS']
    type = tree['Boomtype']
    print('name', name, 'type', type)

    # determine if tree grows fast or regular
    group = name.split()
    genus = str(group[0])
    if genus in fast_growers:
        fast_growth = True
    else:
        fast_growth = False

    # read out tree location from gemeente data
    lng = tree['LNG']
    lat = tree['LAT']

    # convert location from WGS84 to Rijksdriehoek
    # hoeft niet voor gisib, wel voor dingen van maps.amsteram, TODO maybe somehow coordinatensysteem checken?
    rd_x, rd_y = wgs_to_rd(lat, lng)

    # check boommonitor dict
    if name in tree_properties:
        attributes = tree_properties[name]
        print(name, attributes)
        height_class = attributes['height_class']
        crown_class = attributes['crown_class']
    else:
        height_class = None
        crown_class = None
        print('this tree species is not yet classified:', name)
    print('height class', height_class, 'crown class', crown_class)
    if not height_class:
        print('height class was not known so rootvolume could not be determined')
        return [0, 0, 0], 0, 0, rd_x, rd_y, tree_number

    # read out year of planting (origin) from gemeente data
    origin = tree['Plantjaar']
    if origin == 0:
        print('year of planting was not known so rootvolume could not be determined')
        return [0, 0, 0], 0, 0, rd_x, rd_y, tree_number
    circulation = year - origin
    print('origin', origin)

    # determine type of ground from bgt
    col, row, i, j = WMTS_calculator(rd_x, rd_y)
    properties = get_properties(col, row, i, j)
    bgt_class = bgt_classifier(properties)
    print('bgt class:', bgt_class)

    # if crown size & bgt value unknown
    if not crown_class and not bgt_class:
        print('both crownsize and bgt value unknown, rootvolume cannot be determined for tree', tree_number)
        return [0, 0, 0], 0, 0, rd_x, rd_y, tree_number

    # what if bgt value unknown
    elif crown_class and not bgt_class:
        rootvolume = bgt_unknown(height_class, crown_class, circulation, fast_growth)
        print('bgt was unknown')

    # what if tree is not Cobra dataset (thus crown not known)
    elif not crown_class and bgt_class:
        rootvolume = crown_unknown(height_class, bgt_class, circulation, fast_growth)
        print('crownsize was unknown')

    else:
        print('no unknowns')
        # determine necessery root volume (TODO hier forloopje overheen voor grootte over tijd?)
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)
        print('rootvolume', rootvolume)

    # determine ahn height
    ground_level = get_height(rd_x, rd_y)
    print('ground level', ground_level)

    # determine groundwater level (interpolated)
    intersect_coord = intersect(mesh, rd_x, rd_y)
    groundwater_level = intersect_coord[2]
    print('groundwater level', groundwater_level)

    # determine relative depth
    relative_depth = ground_level - groundwater_level

    #  determine cylinder radius
    radius = np.sqrt(rootvolume / (np.pi * relative_depth))
    print('radius', radius)



    return radius, ground_level, groundwater_level, rd_x, rd_y, tree_number




# determine current year
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
current_year = date.year

data_year = 2020 # from what year is the data (tree crown/height especially)

# do Delaunay interpolation for groundwater groundwater levels
# todo: #probleem: einddataframe heeft bepaalde rijen niet meer die plek 1 of 2 waren -> probleem als < 3 punten in hydrolisch jaar
# todo alleen recentste jaren meenemen? maybe neit want bomen staan er gwn lang
points = np.load('GHG_values.npy')
mesh = interpolate(points)
df = pd.read_csv('Wallen_trees.csv')

years = [2020, 2040, 2060] # years for which to calculate rootvolume
for y in years:
    radius_list = []
    groundlevel_list = []
    groundwater_list = []
    x_list = []
    y_list = []
    number_list = []
    for index, row in df.iterrows():
        print()

        if index > 5:
            continue
        print(row)
        print('index', index)
        radius, ground_level, groundwater_level, rd_x, rd_y, tree_number = main(row, y, mesh)
        radius_list.append(radius)
        groundlevel_list.append(ground_level)
        groundwater_list.append(groundwater_level)
        x_list.append(rd_x)
        y_list.append(rd_y)
        number_list.append(tree_number)

    vertices = 30 # must be even number of at least 8, defines vertices of cylinder
    radius_T = np.array(radius_list).T.tolist()

    city_json_opt = to_cityJSON(radius_T[0], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'optimal')
    json_string_opt = json.dumps(city_json_opt)
    with open('output/json_opt_{}.city.json'.format(y), 'w') as outfile:
        outfile.write(json_string_opt)

    city_json_res = to_cityJSON(radius_T[1], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'reasonable')
    json_string_res = json.dumps(city_json_res)
    with open('output/json_res_{}.city.json'.format(y), 'w') as outfile:
        outfile.write(json_string_res)

    city_json_mar = to_cityJSON(radius_T[2], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'marginal')
    json_string_mar = json.dumps(city_json_mar)
    with open('output/json_mar_{}.city.json'.format(y), 'w') as outfile:
        outfile.write(json_string_mar)
