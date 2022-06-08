########################################################################################
# Code for requestigng the ahn and rivm servers for tree height and groundlevel height
########################################################################################

from urllib.request import urlopen
import json
import numpy as np


def WMS_calculator(x, y):
    '''Creates bounding box of that returns 3 by 3 pixels of which 
    the middle one should be read out (i=1, j=1 in url).'''

    x_min = x - 1
    y_min = y - 1
    x_max = x + 1
    y_max = y + 1

    return x_min, y_min, x_max, y_max


def get_rivm(x_min, y_min, x_max, y_max):
    
    # retrieve rivm information
    url = 'https://apps.geodan.nl/public/atlasnextgen/configuration/proxy/?configuration=58bf95bc-67bf-402d-a355-af211ad33949&url=https%3A%2F%2Fgeodata.rivm.nl%2Fgeoserver%2Fwms%3FSERVICE%3DWMS%26VERSION%3D1.3.0%26REQUEST%3DGetFeatureInfo%26FORMAT%3Dimage%252Fpng%26TRANSPARENT%3Dtrue%26QUERY_LAYERS%3Ddank%253Arivm_087_20170415_gm_boomhoogte%26LAYERS%3Ddank%253Arivm_087_20170415_gm_boomhoogte%26SERVICEKEY%3D5da6383b-b70c-11eb-ad75-52540072701a%26STYLES%3D%26BUFFER%3D5%26EXCEPTIONS%3DINIMAGE%26FEATURE_COUNT%3D10%26INFO_FORMAT%3Dapplication%252Fjson%26I%3D1%26J%3D1%26WIDTH%3D256%26HEIGHT%3D256%26CRS%3DEPSG%253A28992%26BBOX%3D{}%252C{}%252C{}%252C{}&layerid=1554471415790'.format(str(x_min), str(y_min), str(x_max), str(y_max))

    # store response of the url
    response = urlopen(url)

    # read out height from json file
    json_data = json.loads(response.read())
    features = json_data['features'][0]
    properties = features['properties']
    height = properties['GRAY_INDEX']

    return height


def backup_treeheight(rd_x, rd_y):
    '''Reads out tree height from AHN4 DTM 50cm (2020-2022) at coordinate 
    and gaussian noise around coordinate and reads out rivm tree height (2017) 
    as backup. Takes the maximal value of all retrieved heights as tree height.'''

    # generate Gaussian noise
    points = 20 # amount of extra sample points (noise)
    std = 0.5 # standard deviation of noise
    noise_x = np.random.normal(rd_x, std, points)
    noise_y = np.random.normal(rd_y, std, points)

    # add original coordinates
    noise_x = np.append(noise_x, rd_x)
    noise_y = np.append(noise_y, rd_y)

    # sample the tree height at the points
    heights = []
    for i in range(points+1):

        # create url corresponding to (x, y)-coordinate
        url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN4_DSM_50cm/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(noise_x[i], noise_y[i])

        # store response of the url
        response = urlopen(url)

        # read out height from json file
        json_data = json.loads(response.read())
        height_ahn = json_data['value']
        if height_ahn != 'NoData':
            heights.append(float(height_ahn))

    # sample rivm tree height
    x_min, y_min, x_max, y_max = WMS_calculator(rd_x, rd_y)
    height_rivm = get_rivm(x_min, y_min, x_max, y_max)
    if height_rivm != -9999:
        heights.append(height_rivm)

    # take the maximal height of the points as the tree height
    tree_height = max(heights)

    return tree_height


def get_mean_height(x, y):
    '''Take average of nearby points when ground level not known.'''

    # create sample points at adjacent grid cells
    coords = [(x+0.5, y+0.5), (x-0.5, y+0.5), (x-0.5, y-0.5), (x+0.5, y-0.5)]

    # sample the ground heigth at the points
    heights = []
    for c in coords:

        # create url corresponding to (x, y)-coordinate
        url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN4_DTM_50cm/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(c[0], c[1])

        # store response of the url
        response = urlopen(url)

        # read out json file
        json_data = json.loads(response.read())
        height = json_data['value']

        # try AHN3 if nodata was returned from AHN4
        if height == 'NoData':
            url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN3_i/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(x, y)

            # store response of the url
            response = urlopen(url)

            # read out json file
            json_data = json.loads(response.read())
            height = json_data['value']
        
        # store returned groundlevel heights
        if height != 'NoData':
            heights.append(float(height))

    # take the mean height of the points as the groundlevel height
    ground_level = np.mean(heights)

    return ground_level


def get_groundlevel(x, y):
    '''Reads out height from AHN4 DTM 50cm at coordinate.'''

    # create url corresponding to (x, y)-coordinate
    url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN4_DTM_50cm/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(x, y)

    # store response of the url
    response = urlopen(url)

    # read out json file
    json_data = json.loads(response.read())
    height = json_data['value']

    # try AHN3 if nodata was returned from AHN4
    if height == 'NoData':
        url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN3_i/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(x, y)

        # store response of the url
        response = urlopen(url)

        # read out json file
        json_data = json.loads(response.read())
        height = json_data['value']

    # try nearby coordinates if ahn3 and ahn4 dont have data
    if height == 'NoData':
        height = get_mean_height(x, y)

    return float(height)
