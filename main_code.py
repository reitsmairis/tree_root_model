#############################################################################
# Main code for executing the rootvolume models
#############################################################################

import pandas as pd
import numpy as np
import math
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
from vedo import *

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
        try:
            height = backup_treeheight(rd_x, rd_y)
        except:
            height = None

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
    groundlevel_list = []
    groundwater_list = []
    x_list = []
    y_list = []
    number_list = []
    volume_list = [[] for i in range(len(years))]

    # create directories for years if not existing
    for l in ['marginal', 'reasonable', 'optimal']:
        for y in years:
            dirName = 'output/{}/{}/{}/{}'.format(area, model, l, y)
            binaryName = 'output_bin/{}/{}/{}/{}'.format(area, model, l, y)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            if not os.path.exists(binaryName):
                os.makedirs(binaryName)

    # create columns for bgt class, ground level and groundwater level if missing 
    if 'BGT_class' not in df.columns:
        df['BGT_class'] = None 
    if 'maaiveld' not in df.columns:
        df['maaiveld'] = None 
    if 'GHG' not in df.columns:
        df['GHG'] = None 

    # retrieve tree properties and rootvolume
    for index, tree in df.iterrows():

        # retrieve tree id
        tree_number = get_treenumber(tree) 

        # read out name and type
        name = tree['Soortnaam_WTS']
        tree_type = tree['Boomtype'] 

        # read out origin, if not known it is not possible to determine rootvolume
        origin = tree['Plantjaar']
        if origin == 0:
            continue

        # retrieve tree position in RD coordinates
        if 'RD_X' not in tree.keys():
            rd_x, rd_y = get_coordinates(tree)
        else:
            rd_x, rd_y = tree['RD_X'], tree['RD_Y']

        # retrieve tree height
        height = get_treeheight(tree, rd_x, rd_y)

        # retrieve tree crown
        crown = get_crown(tree_number)
       
        # retrieve soil type at location of tree
        bgt_class = tree['BGT_class']
        if not bgt_class: 
            bgt_class = get_soiltype(rd_x, rd_y)
            df.at[index, 'BGT_class'] = bgt_class
            
        # retrieve ahn height
        ground_level = tree['maaiveld']
        if not ground_level: 
            try:
                ground_level = get_groundlevel(rd_x, rd_y)
                if math.isnan(ground_level):
                    continue
                df.at[index, 'maaiveld'] = ground_level
            except:
                continue

        # retrieve groundwater level (interpolated)
        groundwater_level = tree['GHG']
        if not groundwater_level:
            try:
                intersect_coord = intersect(mesh, rd_x, rd_y)
                groundwater_level = intersect_coord[2]
                df.at[index, 'GHG'] = groundwater_level
            except:
                continue

        # determine relative depth
        relative_depth = ground_level - groundwater_level
        
        # boundary for minimal root depth is 1.25 m
        if relative_depth < 0.25:
            relative_depth = 0.25
            groundwater_level = ground_level - relative_depth

        # boundary for maximal root depth is 1.25 m
        if relative_depth > 1.25:
            relative_depth = 1.25
            groundwater_level = ground_level - relative_depth

        # calculate root volume for every year using the chosen model
        for n, y in enumerate(years):

            if model == 'static':
                if height == None:
                    continue
                rootvolume = main_static(y, name, bgt_class, origin, tree_type, height, crown)

            if model == 'treedict':
                rootvolume = main_treedict(y, name, bgt_class, origin, tree_type)

            if model == 'treegrowth':
                data_df = pd.read_csv('data/grow_data.csv')
                rootvolume = main_treegrowth(y, name, bgt_class, origin, tree_type, data_df)

            # determine cylinder radius
            radius = np.sqrt(rootvolume / (np.pi * relative_depth))

            #print(y, rd_x, rd_y, origin, rootvolume, radius, relative_depth, ground_level, groundwater_level)

            # continue if rootvolume could not be determined
            if rootvolume[0] == 0 or math.isnan(rootvolume[0]):
                continue

            # store static output in last run
            if y == years[-1]:
                groundlevel_list.append(ground_level)
                groundwater_list.append(groundwater_level)
                x_list.append(rd_x)
                y_list.append(rd_y)
                number_list.append(tree_number)

            # store nonstatic output neccesary for cylinders
            radius_list[n].append(radius)
            volume_list[n].append(rootvolume)

        # save progress once every 100 trees
        if index % 100 == 0:
            print(index)
            np.save('output/numpy_files/{}_{}_radius'.format(area, model), np.array(radius_list))
            np.save('output/numpy_files/{}_{}_groundlevel'.format(area, model), np.array(groundlevel_list))
            np.save('output/numpy_files/{}_{}_groundwater'.format(area, model), np.array(groundwater_list))
            np.save('output/numpy_files/{}_{}_rdx'.format(area, model), np.array(x_list))
            np.save('output/numpy_files/{}_{}_rdy'.format(area, model), np.array(y_list))
            np.save('output/numpy_files/{}_{}_number'.format(area, model), np.array(number_list))
            np.save('output/numpy_files/{}_{}_volume'.format(area, model), np.array(volume_list))

    # save in the end
    np.save('output/numpy_files/{}_{}_radius'.format(area, model), np.array(radius_list))
    np.save('output/numpy_files/{}_{}_groundlevel'.format(area, model), np.array(groundlevel_list))
    np.save('output/numpy_files/{}_{}_groundwater'.format(area, model), np.array(groundwater_list))
    np.save('output/numpy_files/{}_{}_rdx'.format(area, model), np.array(x_list))
    np.save('output/numpy_files/{}_{}_rdy'.format(area, model), np.array(y_list))
    np.save('output/numpy_files/{}_{}_number'.format(area, model), np.array(number_list))
    np.save('output/numpy_files/{}_{}_volume'.format(area, model), np.array(volume_list))

    # safe dataframes with new information
    df.to_csv('data/trees_{}_filled.csv'.format(area))

    ## convert output to CityJSON cylinders
    #for n, y in enumerate(years):
     #   radius_T = np.array(radius_list[n]).T.tolist()

    #    city_json_opt = to_cityJSON(radius_T[0], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'optimal')
     #   json_string_opt = json.dumps(city_json_opt)
     #   with open('output/{}/{}/optimal/{}/json_opt.city.json'.format(area, model, y), 'w') as outfile:
     #       outfile.write(json_string_opt)

      #  city_json_res = to_cityJSON(radius_T[1], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'reasonable')
    #    json_string_res = json.dumps(city_json_res)
     #   with open('output/{}/{}/reasonable/{}/json_res.city.json'.format(area, model, y), 'w') as outfile:
      #      outfile.write(json_string_res)

      #  city_json_mar = to_cityJSON(radius_T[2], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'marginal')
     #   json_string_mar = json.dumps(city_json_mar)
      #  with open('output/{}/{}/marginal/{}/json_mar.city.json'.format(area, model, y), 'w') as outfile:
      #      outfile.write(json_string_mar)


####################### adjust model parameters #####################################

model = 'treedict' # choose which model to use, options: 'static', 'treedict', 'treegrowth'

area = ['Amsterdam_0', 'Amsterdam_1', 'Amsterdam_2', 'Amsterdam_3']  # choose the area, used for naming output

#df = pd.read_csv('data/trees_test_filled.csv') # choose the file containing the tree data
#df = df.replace({np.nan: None})
# read out dataframes containing the gemeente trees
df0 = pd.read_csv('data/BOMEN_0.csv', sep=';')
df0 = df0.replace({np.nan: None})
df1 = pd.read_csv('data/BOMEN_1.csv', sep=';')
df1 = df1.replace({np.nan: None})
df2 = pd.read_csv('data/BOMEN_2.csv', sep=';')
df2 = df2.replace({np.nan: None})
df3 = pd.read_csv('data/BOMEN_3.csv', sep=';')
df3 = df3.replace({np.nan: None})
df_list = [df0, df1, df2, df3]
# concatinate dataframes
#df_tot = pd.concat([df0, df1, df2, df3], ignore_index = True)

#points = np.load('grondwater/GHG_values_wallengebied.npy') # choose the file containing the GHG data
#mesh = interpolate(points)
#mesh = load('Filled_amsterdam_mesh.vtk')

years = [2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060] # np.arange(2010, 2061, 1) # choose years for which to calculate rootvolume

vertices = 30 # choose number of vertices for cylinder, must be even number of at least 8

#for model in ['static', 'treedict', 'treegrowth']:
for count, a in area: 
    __main__(model, a, df_list[count], mesh, years, vertices)

######################################################################################