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
from timedependency import *

def main(year, cobra_df, mesh, age, name, tree_number, bgt_class, origin, type):
    '''for 1 tree'''
    # todo cobra df maybe van tevoren al splitten dat ik niet steeds heel df meegeef

    # if year of planting is not known it is not possible to determine rootvolume
    if origin == 0:
        print('year of planting was not known so rootvolume could not be determined')
        return [0, 0, 0], 0, 0, rd_x, rd_y, tree_number
    circulation = year - origin
    print('origin', origin)

    # determine if tree grows fast or regular
    group = name.split()
    genus = str(group[0])
    if genus in fast_growers:
        fast_growth = True
    else:
        fast_growth = False

    print('year', year)
    dbh = predict_value(age, name, 'age', 'dbh')
    print('dbh', dbh)

    # determine height and crown class
    height = predict_value(dbh, name, 'dbh', 'tree ht')
    height_class = height_classifier(height)
    crown_diameter = predict_value(dbh, name, 'dbh', 'crown dia')
    crown_class = crown_classifier(crown_diameter, height, type)
    print('height', height, 'crown', crown_diameter)

    # what if bgt value unknown
    if not bgt_class:
        rootvolume = bgt_unknown(height_class, crown_class, circulation, fast_growth)
        print('bgt was unknown')

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



def determine_base(tree, cobra_df, tree_number, name, rd_x, rd_y):

    # read out height string from gemeente data and convert to average of the range
    height_string = tree['Boomhoogte']
    # if height not known use ahn
    if height_string == 'Onbekend':
        height = get_treeheight(rd_x, rd_y)
    else:
        height_range = []
        for word in height_string.split():
            if word.isdigit():
                height_range.append(int(word))
        height = np.mean(height_range) # TODO iets anders dan average? of wat als avarage precies op classification boundary valt?
        print('gemeente height', height)

    # read out cobra information
    index = cobra_df.index[cobra_df.uid_gemeente == tree_number]

    if len(index) != 0:
        crown_diameter = cobra_df.at[index[0], 'kroondiameter']
        trunk_diameter = cobra_df.at[index[0], 'stamdiameter']
        cobra_height = cobra_df.at[index[0], 'boomhoogte']
        print('crown diameter', crown_diameter, 'trunk diameter', trunk_diameter, 'cobra_height', cobra_height)

    dbh = estimate_dbh(cobra_df, height, name, tree_number)
    print('mean dbh', dbh)
    age = predict_value(dbh, name, 'dbh', 'age')
    # dbh_2020 = predict_value(age, name, 'age', 'dbh')
    # print('dbh_2020', dbh_2020)
    print('age', age)

    return age

# voor eventuele main functie:
# boomhoogte, kroondiameter, aanplantjaar, x, y (stamdiameter, tree_number/name)



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

# create crown csv
# todo eigenlijk ook ff met select_trees voor goede coords doen
cobra_df = pd.read_csv('data/cobra_data.csv')

df = pd.read_csv('Wallen_trees.csv')

years = [2020, 2040, 2060] # years for which to calculate rootvolume


radius_list = [[] for i in range(len(years))]
groundlevel_list = [[] for i in range(len(years))]
groundwater_list = [[] for i in range(len(years))]
x_list = [[] for i in range(len(years))]
y_list = [[] for i in range(len(years))]
number_list = [[] for i in range(len(years))]

for index, tree in df.iterrows():
    print()
    if index > 5:
        continue

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

    # read out origin
    origin = tree['Plantjaar']

    # read out tree location from gemeente data
    lng = tree['LNG']
    lat = tree['LAT']

    # convert location from WGS84 to Rijksdriehoek
    # hoeft niet voor gisib, wel voor dingen van maps.amsteram, TODO maybe somehow coordinatensysteem checken?
    rd_x, rd_y = wgs_to_rd(lat, lng)

    # determine type of ground from bgt
    col, row, i, j = WMTS_calculator(rd_x, rd_y)
    properties = get_properties(col, row, i, j)
    bgt_class = bgt_classifier(properties)
    print('bgt class:', bgt_class)

    # determine age in year of data aquisition
    age_0 = determine_base(tree, cobra_df, tree_number, name, rd_x, rd_y)

    # TODO wat als leeftijd niet bepaald kon worden -> backup, dus hier al een soort check van als de soort niet in amerikaans paper staat
    # for future
    if age_0 == None:
        continue

    for n, y in enumerate(years):

        # calculate new age
        additional_years = y - data_year
        age = age_0 + additional_years

        radius, ground_level, groundwater_level, rd_x, rd_y, tree_number = main(y, cobra_df, mesh, age, name, tree_number, bgt_class, origin, type)
        radius_list[n].append(radius)
        groundlevel_list[n].append(ground_level)
        groundwater_list[n].append(groundwater_level)
        x_list[n].append(rd_x)
        y_list[n].append(rd_y)
        number_list[n].append(tree_number)

vertices = 30 # must be even number of at least 8, defines vertices of cylinder
for n, y in enumerate(years):
    radius_T = np.array(radius_list[n]).T.tolist()

    city_json_opt = to_cityJSON(radius_T[0], groundlevel_list[n], groundwater_list[n], x_list[n], y_list[n], number_list[n], vertices, 'optimal')
    json_string_opt = json.dumps(city_json_opt)
    with open('output/json_opt_{}.city.json'.format(y), 'w') as outfile:
        outfile.write(json_string_opt)

    city_json_res = to_cityJSON(radius_T[1], groundlevel_list[n], groundwater_list[n], x_list[n], y_list[n], number_list[n], vertices, 'reasonable')
    json_string_res = json.dumps(city_json_res)
    with open('output/json_res_{}.city.json'.format(y), 'w') as outfile:
        outfile.write(json_string_res)

    city_json_mar = to_cityJSON(radius_T[2], groundlevel_list[n], groundwater_list[n], x_list[n], y_list[n], number_list[n], vertices, 'marginal')
    json_string_mar = json.dumps(city_json_mar)
    with open('output/json_mar_{}.city.json'.format(y), 'w') as outfile:
        outfile.write(json_string_mar)
