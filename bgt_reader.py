from urllib.request import urlopen
import json
import math

def bgt_classifier(properties):
    '''Classifies bgt attribute output in one of the four used categories of ground type (open ground/light load/ moderate load/ heavy load)'''

    # classify bgt attributes
    bgt_functions = {
        'voetpad': 'light_load',
        'fietspad': 'light_load',
        'voetgangersgebied': 'light_load',
        'parkeervlak': 'moderate_load',
        'inrit': 'moderate_load',
        'rijbaan lokale weg': 'heavy_load'
    }
    bgt_appearance = {
        'groenvoorziening': 'open_ground',
        'loofbos': 'open_ground',
        'onverhard': 'open_ground'
    }
    bgt_berm = {
        'groenvoorziening': 'open_ground',
        'onverhard': 'open_ground',
        'open verharding': 'light_load'
    }
    bgt_exceptions = {
        'building': False,
        'bordes': 'light_load',
        'kademuur': False,
        'waterloop': False
    }

    # check function
    if 'functie' in properties:
        function = properties['functie']
        print('function:', function)

        # 'berm' (roadside) because it can be multiple things
        if function == 'berm':
            appearance = properties['fysiek_voorkomen']
            ground_type = bgt_berm.get(appearance)
            print('appearance berm:', appearance, 'ground_type:', ground_type)
            return ground_type

        ground_type = bgt_functions.get(function)
        print('function:', function, 'ground_type:', ground_type)
        return ground_type

    # check appearance
    if 'fysiek_voorkomen' in properties:
        appearance = properties['fysiek_voorkomen']
        ground_type = bgt_appearance.get(appearance)
        print('appearance:', appearance, 'ground_type:', ground_type)
        return ground_type

    # some trees are misplaced in buildings
    if 'bag_pnd' in properties:
        ground_type = bgt_exceptions['building']
        print('tree misplaced in building')
        return ground_type

    # some trees are placed in 'bordes'
    if 'plus_type' in properties and properties['plus_type'] != '':
        type = properties['plus_type']
        print('plustype', type)
        ground_type = bgt_exceptions.get(type)
        return ground_type

    # tree in kademuur:
    if 'type' in properties:
        type = properties['type']
        print('type', type)
        ground_type = bgt_exceptions.get(type)
        return ground_type


    else:
        print('bgt unknown', properties)
        return None



def get_properties(col, row, i, j):

    # create url corresponding to tilematrix coordinates
    url = "https://service.pdok.nl/lv/bgt/wmts/v1_0?service=WMTS&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetFeatureInfo&LAYER=achtergrondvisualisatie&STYLE=&FORMAT=image/png&TileCol={}&TileRow={}&TileMatrix=EPSG:28992:14&TileMatrixSet=EPSG:28992&I={}&J={}&infoformat=application/json&info_format=application/json&".format(str(col), str(row), str(i), str(j))

    # store response of the url
    response = urlopen(url)

    # read out json file
    json_data = json.loads(response.read())
    print(len(json_data['features']))
    features = json_data['features'][0]
    properties = features['properties']

    return properties

# # test get_function
# url = "https://service.pdok.nl/lv/bgt/wmts/v1_0?service=WMTS&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetFeatureInfo&LAYER=achtergrondvisualisatie&STYLE=&FORMAT=image/png&TileCol=7745&TileRow=8265&TileMatrix=EPSG:28992:14&TileMatrixSet=EPSG:28992&I=125&J=196&infoformat=application/json&info_format=application/json&"
# result = get_function(url)
# print(result)


def WMTS_calculator(x, y):
    '''Converts Rijksdriehoek coordinates to WMTS tilematrix coordinates, for more information see WMTS documentation: https://www.ogc.org/standards/wmts'''

    # tile matrix properties, source: GetCapabilities identifier 14 (zoom level), https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0?request=getcapabilities&service=wmts
    offset_x, offset_y = -285401.92, 903402.92 # top left corner
    denominator = 750 # defines scale of tile
    tile_width = 256 # in pixels, tile height is equal

    # calculate tile span in m
    pixel_size = 0.00028 # standardized rendering pixel size in m
    meters_per_unit = 1
    pixel_span = (pixel_size * denominator) / meters_per_unit
    tile_span = tile_width * pixel_span

    # calculate tilematrix column and row of coordinate
    wmts_col = (x - offset_x) / tile_span
    wmts_row = (offset_y - y) / tile_span

    # calculate pixel location within tile
    i = (wmts_col - math.floor(wmts_col)) * tile_width
    j = (wmts_row - math.floor(wmts_row)) * tile_width

    return math.floor(wmts_col), math.floor(wmts_row), round(i), round(j)


# test WMTS_calculator
rd_x, rd_y = 121137, 485369
col, row, i, j = WMTS_calculator(rd_x, rd_y)
result = get_properties(col, row, i, j)
classification = bgt_classifier(result)
print(classification)
