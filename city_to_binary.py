#############################################################################
# This code creates config files corresponding to the different years and ambition levels,
# together with the TileBakeTool it is then possible to create binary formats from the CityJSON output
#
# Source of the TileBakeTool:
# https://github.com/Amsterdam/CityDataToBinaryModel
#############################################################################

import json
import os


####################### adjust model parameters #####################################

models = ['treedict'] # models with which the CityJSON output was generated, options: 'static', 'treedict', 'treegrowth'

years = [2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060] # years for which the rootvolume is calculated

areas = ['Amsterdam'] # areas for which the rootvolume is calculated

levels = ['marginal', 'reasonable', 'optimal'] # ambition levels used

#####################################################################################


# open initial (template) config file
f = open('root_config.json')
config = json.load(f)

# adjust config file to corresponding area, model, level and year and execute TileBakeTool
for a in areas:
    for m in models:
        for l in levels:
            for y in years:
                config['sourceFolder'] = "C:\\Users\\Iris Reitsma\\Documents\\Master\\jaar 2\\stage\\root_model\\output\\{}\\{}\\{}\\{}\\".format(a, m, l, y)
                config['outputFolder'] = "C:\\Users\\Iris Reitsma\\Documents\\Master\\jaar 2\\stage\\root_model\\output_bin\\{}\\{}\\{}\\{}\\roots_".format(a, m, l, y)
                json_string = json.dumps(config)

                # replace config file
                with open('root_config.json', 'w') as outfile:
                    outfile.write(json_string)

                # execute TileBakeTool
                os.system('TileBakeTool\\TileBakeTool.exe --config "C:\\Users\\jacco\\Documents\\Iris\\root_config.json"')
