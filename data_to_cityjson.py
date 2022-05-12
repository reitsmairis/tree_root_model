import numpy as np
import json
from cityjson_converter2 import to_cityJSON

years = np.arange(2010, 2061, 1) # choose years
vertices = 30 # choose number of vertices for cylinder, must be even number of at least 8
model = 'treedict' # choose model
area = 'Amsterdam' # choose area


# save in the end
radius_list = np.load('output/numpy_files/{}_{}_radius.npy'.format(area, model))
groundlevel_list = np.load('output/numpy_files/{}_{}_groundlevel.npy'.format(area, model))
groundwater_list = np.load('output/numpy_files/{}_{}_groundwater.npy'.format(area, model))
x_list = np.load('output/numpy_files/{}_{}_rdx.npy'.format(area, model))
y_list = np.load('output/numpy_files/{}_{}_rdy.npy'.format(area, model))
number_list = np.load('output/numpy_files/{}_{}_number.npy'.format(area, model))
volume_list = np.load('output/numpy_files/{}_{}_volume.npy'.format(area, model))

# convert output to CityJSON cylinders
for n, y in enumerate(years):
    print(y)
    radius_T = np.array(radius_list[n]).T.tolist()

    to_cityJSON(radius_T[0], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'optimal', area, model, y)
    #json_string_opt = json.dumps(city_json_opt)
    #with open('output/{}/{}/optimal/{}/json_opt.city.json'.format(area, model, y), 'w') as outfile:
        #outfile.write(json_string_opt)
    #outfile.close()

    city_json_res = to_cityJSON(radius_T[1], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'reasonable', area, model, y)
    #json_string_res = json.dumps(city_json_res)
    #with open('output/{}/{}/reasonable/{}/json_res.city.json'.format(area, model, y), 'w') as outfile:
     #   outfile.write(json_string_res)
    #outfile.close()

    city_json_mar = to_cityJSON(radius_T[2], groundlevel_list, groundwater_list, x_list, y_list, number_list, vertices, 'marginal', area, model, y)
    #json_string_mar = json.dumps(city_json_mar)
    #with open('output/{}/{}/marginal/{}/json_mar.city.json'.format(area, model, y), 'w') as outfile:
    #    outfile.write(json_string_mar)
    #outfile.close()