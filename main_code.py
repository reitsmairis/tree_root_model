#############################################################################
# Main code for executing the rootvolume models
#############################################################################

import pandas as pd
import numpy as np
import os
import json
from method_treegrowth import main_treegrowth
from method_treedict import main_treedict
from method_static import main_static
from interpolation import interpolate, intersect
from helpers import wgs_to_rd
from bgt_reader import get_properties, WMTS_calculator, bgt_classifier
from ahn_reader import get_groundlevel, backup_treeheight
from cityjson_converter import to_cityJSON


def get_treenumber(tree):

    # retrieve tree id
    tree_number = tree['Boomnummer']

    # use object number if tree number is unknown (=0)
    if tree_number == 0:
        tree_number = 'objNR_' + str(tree['OBJECTNUMMER'])
    
    return tree_number


def get_coordinates(tree):

    # TODO checken of t rd of latlong is 

    # read out tree location from gemeente data
    lng = tree['LNG']
    lat = tree['LAT']

    # convert location from WGS84 to Rijksdriehoek
    rd_x, rd_y = wgs_to_rd(lat, lng)

    return rd_x, rd_y


def get_soiltype(rd_x, rd_y):

    # determine wmts file coordinates 
    col, row, i, j = WMTS_calculator(rd_x, rd_y)

    # try requesting bgt class
    try:
        properties = get_properties(col, row, i, j)
        bgt_class = bgt_classifier(properties)
    except:
        bgt_class = None
    
    return bgt_class


def get_treeheight(tree, rd_x, rd_y):
    # TODO checken of t een range is of n getal

    # retrieve tree height
    height_string = tree['Boomhoogte']

    # if height not known use ahn
    if height_string == 'Onbekend':
        height = backup_treeheight(rd_x, rd_y)

    # read out height string from gemeente data and convert to average of the range
    else:
        height_range = []
        for word in height_string.split():
            if word.isdigit():
                height_range.append(int(word))
        height = np.mean(height_range) 
    
    return height


def get_crown(tree_number):
    # TODO ook crown van ander groot bestand kunnen meenemen
    
    # read out crown data from Cobra Groeninzicht
    cobra_df = pd.read_csv('data/cobra_data.csv')

    # read out Cobra Groeninzicht information
    index = cobra_df.index[cobra_df.uid_gemeente == tree_number]

    # check if tree is known by Cobra Groeninzicht
    if len(index) == 0:
        crown = None
    else:
        # check if Cobra Groeninzicht crown is known
        cobra_height = cobra_df.at[index[0], 'boomhoogte']
        if cobra_height == 3:
            crown = None
        else:
            crown = cobra_df.at[index[0], 'kroondiameter']

    return crown

	
def __main__(model, area, df, mesh, years, vertices):

    # create lists for storing necessary output
    radius_list = [[] for i in range(len(years))]
    groundlevel_list = [[] for i in range(len(years))]
    groundwater_list = [[] for i in range(len(years))]
    x_list = [[] for i in range(len(years))]
    y_list = [[] for i in range(len(years))]
    number_list = [[] for i in range(len(years))]

    # create directories for years if not existing
    for l in ['marginal', 'reasonable', 'optimal']:
        for y in years:
            dirName = 'output/{}/{}/{}/{}'.format(area, model, l, y)
            binaryName = 'output_bin/{}/{}/{}/{}'.format(area, model, l, y)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            if not os.path.exists(binaryName):
                os.makedirs(binaryName)

    # retrieve tree properties and rootvolume
    for index, tree in df.iterrows():

        # retrieve tree id
        tree_number = get_treenumber(tree) 

        # read out name and type
        name = tree['Soortnaam_WTS']
        tree_type = tree['Boomtype'] 

        # read out origin
        origin = tree['Plantjaar']

        # retrieve tree position in RD coordinates
        if 'RD_X' not in tree.keys():
            rd_x, rd_y = get_coordinates(tree)
        else:
            rd_x, rd_y = tree['RD_X'], tree['RD_Y']

        # retrieve tree height
        print(rd_x, rd_y, tree_number)
        height = get_treeheight(tree, rd_x, rd_y)

        # retrieve tree crown
        #crown = get_crown(tree_number)
        crown = tree['Cobra_crown']
        # retrieve soil type at location of tree
        bgt_class = get_soiltype(rd_x, rd_y)

        # retrieve ahn height
        ground_level = get_groundlevel(rd_x, rd_y)

        # retrieve groundwater level (interpolated)
        try:
            intersect_coord = intersect(mesh, rd_x, rd_y)
            groundwater_level = intersect_coord[2]
        except:
            print('no intersection point')
            continue

        # determine relative depth
        relative_depth = ground_level - groundwater_level
        
        # continue if interpolated GHG is higher than ground level
        if relative_depth < 0:
            print('interpolation wrong for ', rd_x, rd_y)
            continue

        # calculate root volume for every year using the chosen model
        for n, y in enumerate(years):

            if model == 'static':
                rootvolume = main_static(y, mesh, name, tree_number, bgt_class, origin, tree_type, rd_x, rd_y, height, crown)

            if model == 'treedict':
                rootvolume = main_treedict(y, mesh, name, tree_number, bgt_class, origin, tree_type)

            if model == 'treegrowth':
                data_df = pd.read_csv('data/grow_data.csv')
                rootvolume = main_treegrowth(y, mesh, name, tree_number, bgt_class, origin, tree_type, data_df)

            # determine cylinder radius
            radius = np.sqrt(rootvolume / (np.pi * relative_depth))

            print(y, rd_x, rd_y, origin, rootvolume, radius, relative_depth, ground_level, groundwater_level)

            # continue if rootvolume could not be determined
            if rootvolume[0] == 0:
                continue

            # store output neccesary for cylinders
            radius_list[n].append(radius)
            groundlevel_list[n].append(ground_level)
            groundwater_list[n].append(groundwater_level)
            x_list[n].append(rd_x)
            y_list[n].append(rd_y)
            number_list[n].append(tree_number)

        # save progress once every 100 trees
        if index % 100 == 0:
            np.save('output/numpy_files/{}_{}_radius'.format(area, model), np.array(radius_list))
            np.save('output/numpy_files/{}_{}_groundlevel'.format(area, model), np.array(groundlevel_list))
            np.save('output/numpy_files/{}_{}_groundwater'.format(area, model), np.array(groundwater_list))
            np.save('output/numpy_files/{}_{}_rdx'.format(area, model), np.array(x_list))
            np.save('output/numpy_files/{}_{}_rdy'.format(area, model), np.array(y_list))
            np.save('output/numpy_files/{}_{}_number'.format(area, model), np.array(number_list))

    # save in the end
    np.save('output/numpy_files/{}_{}_radius'.format(area, model), np.array(radius_list))
    np.save('output/numpy_files/{}_{}_groundlevel'.format(area, model), np.array(groundlevel_list))
    np.save('output/numpy_files/{}_{}_groundwater'.format(area, model), np.array(groundwater_list))
    np.save('output/numpy_files/{}_{}_rdx'.format(area, model), np.array(x_list))
    np.save('output/numpy_files/{}_{}_rdy'.format(area, model), np.array(y_list))
    np.save('output/numpy_files/{}_{}_number'.format(area, model), np.array(number_list))

    # convert output to CityJSON cylinders
    for n, y in enumerate(years):
        radius_T = np.array(radius_list[n]).T.tolist()

        city_json_opt = to_cityJSON(radius_T[0], groundlevel_list[n], groundwater_list[n], x_list[n], y_list[n], number_list[n], vertices, 'optimal')
        json_string_opt = json.dumps(city_json_opt)
        with open('output/{}/{}/optimal/{}/json_opt.city.json'.format(area, model, y), 'w') as outfile:
            outfile.write(json_string_opt)

        city_json_res = to_cityJSON(radius_T[1], groundlevel_list[n], groundwater_list[n], x_list[n], y_list[n], number_list[n], vertices, 'reasonable')
        json_string_res = json.dumps(city_json_res)
        with open('output/{}/{}/reasonable/{}/json_res.city.json'.format(area, model, y), 'w') as outfile:
            outfile.write(json_string_res)

        city_json_mar = to_cityJSON(radius_T[2], groundlevel_list[n], groundwater_list[n], x_list[n], y_list[n], number_list[n], vertices, 'marginal')
        json_string_mar = json.dumps(city_json_mar)
        with open('output/{}/{}/marginal/{}/json_mar.city.json'.format(area, model, y), 'w') as outfile:
            outfile.write(json_string_mar)


####################### adjust model parameters #####################################

model = 'treegrowth' # choose which model to use, options: 'static', 'treedict', 'treegrowth'

area = 'Centraal' # choose the area, used for naming output

df = pd.read_excel('data/centraal_trees.xlsx') # choose the file containing the tree data

points = np.load('grondwater/GHG_values_Centraal.npy') # choose the file containing the GHG data
mesh = interpolate(points)

years = [2018] # choose years for which to calculate rootvolume

vertices = 30 # choose number of vertices for cylinder, must be even number of at least 8

__main__(model, area, df, mesh, years, vertices)

######################################################################################