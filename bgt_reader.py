#############################################################################
# Code for requestigng the bgt value 
#############################################################################

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
        'building': None,
        'bordes': 'light_load',
        'kademuur': None,
        'waterloop': None
    }

    # check returned function of bgt 
    if 'functie' in properties:
        function = properties['functie']

        # check for 'berm' (roadside) because it can be multiple things
        if function == 'berm':
            appearance = properties['fysiek_voorkomen']
            ground_type = bgt_berm.get(appearance)

            return ground_type

        ground_type = bgt_functions.get(function)

        return ground_type

    # check returned appearance of bgt
    if 'fysiek_voorkomen' in properties:
        appearance = properties['fysiek_voorkomen']
        ground_type = bgt_appearance.get(appearance)

        return ground_type

    # check if returned bgt is a building
    if 'bag_pnd' in properties:
        ground_type = bgt_exceptions['building']

        return ground_type

    # check returned plus type of bgt
    if 'plus_type' in properties and properties['plus_type'] != '':
        type = properties['plus_type']
        ground_type = bgt_exceptions.get(type)

        return ground_type

    # check returned type of bgt
    if 'type' in properties:
        type = properties['type']
        ground_type = bgt_exceptions.get(type)

        return ground_type

    else:
        print('bgt unknown:', properties)

        return None


def get_properties(col, row, i, j):

    # create url corresponding to tilematrix coordinates
    url = "https://service.pdok.nl/lv/bgt/wmts/v1_0?service=WMTS&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetFeatureInfo&LAYER=achtergrondvisualisatie&STYLE=&FORMAT=image/png&TileCol={}&TileRow={}&TileMatrix=EPSG:28992:14&TileMatrixSet=EPSG:28992&I={}&J={}&infoformat=application/json&info_format=application/json&".format(str(col), str(row), str(i), str(j))

    # store response of the url
    response = urlopen(url)

    # read bgt properties out json file
    json_data = json.loads(response.read())
    features = json_data['features'][0]
    properties = features['properties']

    return properties


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

