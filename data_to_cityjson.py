import numpy as np
import json
from cityjson_converter import to_cityJSON
import os

#################################### main ############################################

years = [2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060] #np.arange(2010, 2061, 1) # choose years
vertices = 30 # choose number of vertices for cylinder, must be even number of at least 8
model = 'treedict' # choose model
subareas = ['Amsterdam_0', 'Amsterdam_1', 'Amsterdam_2', 'Amsterdam_3'] # choose area
main_area = 'Amsterdam'

#######################################################################################


# create directories for years if not existing
for l in ['marginal', 'reasonable', 'optimal']:
    for y in years:
        dirName = 'output/{}/{}/{}/{}'.format(main_area, model, l, y)
        binaryName = 'output_bin/{}/{}/{}/{}'.format(main_area, model, l, y)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        if not os.path.exists(binaryName):
            os.makedirs(binaryName)

for area in subareas: 
    # load data
    radius_list = np.load('output/numpy_files/{}_{}_radius.npy'.format(area, model))
    groundlevel_list = np.load('output/numpy_files/{}_{}_groundlevel.npy'.format(area, model))
    groundwater_list = np.load('output/numpy_files/{}_{}_groundwater.npy'.format(area, model))
    x_list = np.load('output/numpy_files/{}_{}_rdx.npy'.format(area, model))
    y_list = np.load('output/numpy_files/{}_{}_rdy.npy'.format(area, model))
    number_list = np.load('output/numpy_files/{}_{}_number.npy'.format(area, model))
    volume_list = np.load('output/numpy_files/{}_{}_volume.npy'.format(area, model))

    # convert output to CityJSON cylinders for the three ambition levels
    for n, y in enumerate(years):
        print(y)
        radius_T = np.array(radius_list[n]).T.tolist()
        to_cityJSON(radius_T[0], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'optimal', area, model, y, main_area)
        to_cityJSON(radius_T[1], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'reasonable', area, model, y, main_area)
        to_cityJSON(radius_T[2], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'marginal', area, model, y, main_area)
