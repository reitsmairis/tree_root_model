###############
# This code creates config files corresponding to the different years and ambition levels,
# together with the TileBakeTool it is then possible to create binary formats from the CityJSON output
#
#################


import json
import os

years = [2020, 2040, 2060]
levels = ['marginal', 'reasonable', 'optimal']

# open initial (template) config file
f = open('root_config.json')
config = json.load(f)

# adjust config file to layers
for l in levels:
    for y in years:
        config['sourceFolder'] = "C:\\Users\\Iris Reitsma\\Documents\\Master\\jaar 2\\stage\\root_model\\output\\{}\\{}\\".format(l, y)
        config['outputFolder'] = "C:\\Users\\Iris Reitsma\\Documents\\Master\\jaar 2\\stage\\root_model\\output_bin\\{}\\{}\\roots_".format(l, y)
        json_string = json.dumps(config)

        # replace config file
        with open('root_config.json', 'w') as outfile:
            outfile.write(json_string)

        # execute TileBakeTool
        os.system('TileBakeTool\\TileBakeTool.exe --config "C:\\Users\\Iris Reitsma\\Documents\\Master\\jaar 2\\stage\\root_model\\root_config.json"')
