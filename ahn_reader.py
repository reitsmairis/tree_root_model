from urllib.request import urlopen
import json
import numpy as np
from helpers import wgs_to_rd


def WMS_calculator(x, y):
    '''Creates bounding box of that returns 3 by 3 pixels of which the middle one should be read out (i=1, j=1 in url)'''
    x_min = x - 1
    y_min = y - 1
    x_max = x + 1
    y_max = y + 1

    return x_min, y_min, x_max, y_max

def get_rivm(x_min, y_min, x_max, y_max):
    url = 'https://apps.geodan.nl/public/atlasnextgen/configuration/proxy/?configuration=58bf95bc-67bf-402d-a355-af211ad33949&url=https%3A%2F%2Fgeodata.rivm.nl%2Fgeoserver%2Fwms%3FSERVICE%3DWMS%26VERSION%3D1.3.0%26REQUEST%3DGetFeatureInfo%26FORMAT%3Dimage%252Fpng%26TRANSPARENT%3Dtrue%26QUERY_LAYERS%3Ddank%253Arivm_087_20170415_gm_boomhoogte%26LAYERS%3Ddank%253Arivm_087_20170415_gm_boomhoogte%26SERVICEKEY%3D5da6383b-b70c-11eb-ad75-52540072701a%26STYLES%3D%26BUFFER%3D5%26EXCEPTIONS%3DINIMAGE%26FEATURE_COUNT%3D10%26INFO_FORMAT%3Dapplication%252Fjson%26I%3D1%26J%3D1%26WIDTH%3D256%26HEIGHT%3D256%26CRS%3DEPSG%253A28992%26BBOX%3D{}%252C{}%252C{}%252C{}&layerid=1554471415790'.format(str(x_min), str(y_min), str(x_max), str(y_max))

    # store response of the url
    response = urlopen(url)

    # read out json file
    json_data = json.loads(response.read())
    features = json_data['features'][0]
    properties = features['properties']
    height = properties['GRAY_INDEX']

    return height


def get_treeheight(rd_x, rd_y):
    '''Reads out height from AHN4 DTM 50cm (2020-2022) at coordinate and gaussian noise around coordinate
    and reads out rivm tree height (2017) as backup. Takes the maximal value of all retrieved heights as tree height'''

    points = 20 # amount of extra points
    std = 0.5 # standard deviation of noise

    noise_x = np.random.normal(rd_x, std, points)
    noise_y = np.random.normal(rd_y, std, points)

    # add original coordinates
    noise_x = np.append(noise_x, rd_x)
    noise_y = np.append(noise_y, rd_y)

    heights = []
    for i in range(points+1):

        # create url corresponding to (x, y)-coordinate
        url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN4_DSM_50cm/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(noise_x[i], noise_y[i])

        # store response of the url
        response = urlopen(url)

        # read out json file
        json_data = json.loads(response.read())
        height_ahn = json_data['value']
        if height_ahn != 'NoData':
            heights.append(float(height_ahn))

    # try rivm tree height
    x_min, y_min, x_max, y_max = WMS_calculator(rd_x, rd_y)
    height_rivm = get_rivm(x_min, y_min, x_max, y_max)
    if height_rivm != -9999:
        heights.append(height_rivm)

    return max(heights)
#
# import pandas as pd
# # compare height calculators and data
# cobra_df = pd.read_csv('data/cobra_data.csv')
# df = pd.read_csv('Wallen_trees.csv')
#
# for index, tree in df.iterrows():
#     print()
#     # if index > 5:
#     #     continue
#
#     # retrieve tree id
#     tree_number = tree['Boomnummer']
#     # use object number if tree number is unknown (=0)
#     if tree_number == 0:
#         tree_number = 'objNR_' + str(tree['OBJECTNUMMER'])
#     print('tree_number', tree_number)
#
#     # read out name
#     name = tree['Soortnaam_WTS']
#     print('name', name)
#
#     i = cobra_df.index[cobra_df.uid_gemeente == tree_number]
#     if len(i) != 0:
#         cobra_height = cobra_df.at[i[0], 'boomhoogte']
#         print('cobra height', cobra_height)
#
#     height_string = tree['Boomhoogte']
#     print('gemeente height', height_string)
#
#     # read out tree location from gemeente data
#     lng = tree['LNG']
#     lat = tree['LAT']
#
#     # convert location from WGS84 to Rijksdriehoek
#     # hoeft niet voor gisib, wel voor dingen van maps.amsteram, TODO maybe somehow coordinatensysteem checken?
#     rd_x, rd_y = wgs_to_rd(lat, lng)
#
#     height_ahn = get_treeheight(rd_x, rd_y)
#     print('height ahn', height_ahn)
#
#     x_min, y_min, x_max, y_max = WMS_calculator(rd_x, rd_y)
#     height_rivm = get_rivm(x_min, y_min, x_max, y_max)
#     print('height_rivm', height_rivm)
#
# print(hoi)
def get_mean_height(x, y):
    '''take average of nearby points when ground level not known'''
    coords = [(x+0.5, y+0.5), (x-0.5, y+0.5), (x-0.5, y-0.5), (x+0.5, y-0.5)]
    heights = []
    for c in coords:
        # create url corresponding to (x, y)-coordinate
        url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN4_DTM_50cm/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(c[0], c[1])

        # store response of the url
        response = urlopen(url)

        # read out json file
        json_data = json.loads(response.read())
        height = json_data['value']
        print(height)

        # try AHN3 if nodata was returned from AHN4
        if height == 'NoData':
            url = "https://ahn.arcgisonline.nl/arcgis/rest/services/AHNviewer/AHN3_i/ImageServer/identify?f=json&geometry=%7B%22x%22%3A{}%2C%22y%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&returnGeometry=true&returnCatalogItems=true&geometryType=esriGeometryPoint&pixelSize=%7B%22x%22%121762.38643022369%2C%22y%22%487011.29600616463%2C%22spatialReference%22%3A%7B%22wkid%22%3A28992%2C%22latestWkid%22%3A28992%7D%7D&renderingRules=%5B%7B%22rasterFunction%22%3A%22AHN2%20-%20Color%20Ramp%20C%22%7D%5D".format(x, y)

            # store response of the url
            response = urlopen(url)

            # read out json file
            json_data = json.loads(response.read())
            height = json_data['value']

        if height != 'NoData':
            heights.append(float(height))
    print(heights)
    ground_level = np.mean(heights)

    return ground_level


# had t eerst via wms op pdok maar daar waren waardes van weggelaten dus nu gwn via de ahn site (deze heeft ook ahn4 :)
def get_height(x, y):
    '''Reads out height from AHN4 DTM 50cm at coordinate'''

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

    # # try nearby coordinates if ahn3 and ahn4 dont have data
    # if height == 'NoData':
    #     coords = [(x+0.5, y+0.5), (x-0.5, y+0.5), (x-0.5, y-0.5), (x+0.5, y-0.5)]
    #     heights = []
    #     for c in coords:
    #         h = get_height(c[0], c[1])
    #         print(h)
    #         if h != 'NoData':
    #             heights.append(float(h))
    #     height = np.mean(heights)
    #     return(height)
    if height == 'NoData':
        height = get_mean_height(x, y)

    return float(height)

# test get_height
x, y = 121631.7739398157,486691.88852783048
get_height(x, y)

# def get_height(x_min, y_min, x_max, y_max):
#
#     # create url corresponding to bounding box
#     url = "https://geodata.nationaalgeoregister.nl/ahn3/ows?service=wms&version=1.3.0&request=GetFeatureInfo&bbox={},{},{},{}&crs=EPSG:28992&width=3&height=3&layers=ahn3_05m_dtm&styles=&format=image/png&query_layers=ahn3_05m_dtm&info_format=application/json&i=1&j=1".format(str(x_min), str(y_min), str(x_max), str(y_max))
#
#     # store response of the url
#     response = urlopen(url)
#
#     # read out json file
#     json_data = json.loads(response.read())
#     features = json_data['features'][0]
#     properties = features['properties']
#     height = properties['GRAY_INDEX']
#
#     return height

# # # test get_height, bron: https://geoforum.nl/t/ahn3-hoogte-opvragen-in-pyqgis/5604/2
# # url = "https://geodata.nationaalgeoregister.nl/ahn3/ows?service=wms&version=1.3.0&request=GetFeatureInfo&bbox=149999,449999,150001,450001&crs=EPSG:28992&width=3&height=3&layers=ahn3_05m_dtm&styles=&format=image/png&query_layers=ahn3_05m_dtm&info_format=application/json&i=1&j=1"
# # result = get_height(url)
# # print(result)
#
# def WMS_calculator(x, y):
#     '''Creates bounding box of that returns 3 by 3 pixels of which the middle one should be read out (i=1, j=1 in url)'''
#     x_min = x - 1
#     y_min = y - 1
#     x_max = x + 1
#     y_max = y + 1
#
#     return x_min, y_min, x_max, y_max
#
# # test WMS_calculator
# x, y = 121684, 485401
# x_min, y_min, x_max, y_max = WMS_calculator(x, y)
# result = get_height(x_min, y_min, x_max, y_max)
# print(result)
