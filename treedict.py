###################################################################################################
# This file contains two dictionaries with information: 
# A dictionary with tree genera that are classified as fast growing.
# A dictionary with the tree height and crown classes, and their maximal crown and height in m.
###################################################################################################

import pandas as pd
from collections import Counter

fast_growers = [
    'Populus',
    'Salix',
    'Alnus'
]

tree_properties = {
    'Ulmus hollandica':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Ulmus hollandica `Vegeta`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Ulmus hollandica `Belgica`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 15
        },
    'Ulmus hollandica `Dampieri`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 7
        },
    'Ulmus hollandica `Groeneveld`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 10
        },
    'Ulmus hollandica `Pioneer`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 10
        },
    'Ulmus hollandica `Commelin`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 10
        },
    'Ulmus hollandica `Wredei`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 9
        },
    'Ulmus `Camperdownii`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 6
        },
    'Ulmus `Dodoens`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 6
        },
    'Ulmus `Homestead`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 10
        },
    'Ulmus `Clusius`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 8
        },
    'Ulmus `Lobel`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 18,
        'max_crown': 10
        },
    'Ulmus `Plantijn`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 18,
        'max_crown': 8
        },
    'Ulmus `New Horizon`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 10
        },
    'Ulmus `Rebona`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 10
        },
    'Ulmus `Sapporo Autumn Gold`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 12
        },
    'Ulmus glabra `Exoniensis`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 10
        },
    'Ulmus glabra':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 35,
        'max_crown': 20
        },
    'Ulmus laevis':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 20
        },
    'Ulmus minor':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 30,
        'max_crown': 20
        },
    'Ulmus minor `Sarniensis`':
        {
        'height_class': 1,
        'crown_class': 'small',
        'max_height': 25,
        'max_crown': 10
        },
    'Ulmus pumila':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 12,
        'max_crown': 13
        },
    'Ulmus Columella':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 20,
        'max_crown': 6
        },
    'Platanus hispanica':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Platanus hispanica `Alphen`s Globe`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 8,
        'max_crown': 8
        },
    'Platanus hispanica `Malburg`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 30,
        'max_crown': 18
        },
    'Platanus hispanica `Huissen`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 30,
        'max_crown': 15
        },
    'Platanus hispanica `Tremonia`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 10
        },
    'Platanus occidentalis':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 15
        },
    'Platanus orientalis `Digitata`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Platanus orientalis `Minaret`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 12,
        'max_crown': 5
        },
    'Platanus orientalis':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Tilia europaea `Zwarte Linde`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Tilia europaea `Koningslinde`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Tilia europaea':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 35
        },
    'Tilia americana':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 15
        },
    'Tilia mongolica':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 8
        },
    'Tilia platyphyllos':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Tilia tomentosa':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Tilia cordata `Bohlje`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 9
        },
    'Tilia cordata `Greenspire`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Tilia cordata `Rancho`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 9
        },
    'Tilia cordata':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 15
        },
    'Tilia tomentosa `Brabant`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 18
        },
    'Tilia europaea `Euchlora`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Tilia flavescens `Glenleven`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Pyrus calleryana `Chanticleer`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 12,
        'max_crown': 6
        },
    'Acer cissifolium':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 12,
        'max_crown': 8
        },
    'Acer davidii':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 9
        },
    'Acer negundo':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 14,
        'max_crown': 12
        },
    'Acer palmatum':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 10
        },
    'Acer platanoides `Autumn Blaze`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 12
        },
    'Acer platanoides `Crimson King`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 12
        },
    'Acer platanoides `Drummondii`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 12,
        'max_crown': 9
        },
    'Acer platanoides `Faassen`s Black`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 10
        },
    'Acer platanoides `Globosum`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 7,
        'max_crown': 7
        },
    'Acer platanoides `Royal Red`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 12
        },
    'Acer platanoides `Schwedleri`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Acer platanoides':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 20
        },
    'Acer pseudoplatanus `Atropurpureum`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Acer pseudoplatanus `Leopoldii`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Acer pseudoplatanus `Negenia`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Acer saccharinum `Asplenifolium`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 18
        },
    'Acer saccharinum `Laciniatum Wieri`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 20
        },
    'Acer saccharinum':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Acer tataricum subsp. ginnala':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 7,
        'max_crown': 9
        },
    'Acer freemanii `Elegant`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 12
        },
    'Acer freemanii':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 12
        },
    'Acer buergerianum':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 8
        },
    'Acer camestre':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 8
        },
    'Acer cappadocicum':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Acer griseum':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 9,
        'max_crown': 6
        },
    'Acer negundo `Variegatum`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 7
        },
    'Acer palmatum `Atropurpureum`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 6
        },
    'Acer pensylvanicum':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 5,
        'max_crown': 5
        },
    'Acer platanoides `Cleveland`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 12
        },
    'Acer platanoides `Fairview`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 7
        },
    'Acer platanoides `Farlake`s Green`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 10
        },
    'Acer pseudoplatanus `Bruchem`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Acer pseudoplatanus `Rotterdam`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 10
        },
    'Acer pseudoplatanus':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 30,
        'max_crown': 25
        },
    'Acer rubrum `Brandywine`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 12
        },
    'Acer rubrum `Karpick`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 6
        },
    'Acer rubrum':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 10
        },
    'Acer saccharinum `Pyramidale`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Acer saccharinum':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 20
        },
    'Acer freemanii `Celzam`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 8
        },
    'Acer `Lobel`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': None,
        'max_crown': None
        },
    'Acer campestre `Elsrijk`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 12,
        'max_crown': 8
        },
    'Acer platanoides `Columnare`':
        {
        'height_class': 1,
        'crown_class': 'small',
        'max_height': 15,
        'max_crown': 6
        },
    'Acer rubrum `Scanlon`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 12,
        'max_crown': 4
        },
    'Acer freemanii `Armstrong`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 15,
        'max_crown': 7
        },
    'Fraxinus americana':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Fraxinus biltmoreana':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': None,
        'max_crown': None
        },
    'Fraxinus excelsior `Aurea Pendula`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 8,
        'max_crown': 6
        },
    'Fraxinus excelsior `Eureka`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Fraxinus excelsior `Jaspidea`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 16,
        'max_crown': 12
        },
    'Fraxinus excelsior `Nana`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 6,
        'max_crown': 5
        },
    'Fraxinus excelsior `Pendula`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 8
        },
    'Fraxinus excelsior':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Fraxinus ornus `Mecsek`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 6,
        'max_crown': 4
        },
    'Fraxinus ornus':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 8
        },
    'Fraxinus angustifolia `Raywood`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Fraxinus angustifolia':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 10
        },
    'Fraxinus angustifolia `Altena`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 15
        },
    'Fraxinus excelsior `Atlas`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Fraxinus excelsior `Diversifolia`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 10
        },
    'Fraxinus excelsior `Westhof`s Glorie`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 15
        },
    'Fraxinus ornus `Louisa lady`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 5
        },
    'Fraxinus ornus `Paus Johannes-Paulus II`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 5
        },
    'Fraxinus pennsylvanica `Zundert`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 10
        },
    'Fraxinus pennsylvanica':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Quercus cerris':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 15
        },
    'Quercus coccinea `Splendens`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Quercus frainetto':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 18
        },
    'Quercus palustris':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 18
        },
    'Quercus petraea':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 25
        },
    'Quercus robur':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 35,
        'max_crown': 35
        },
    'Quercus rubra `Aurea`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 15
        },
    'Quercus rubra':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 25
        },
    'Quercus hispanica':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 20
        },
    'Quercus `Macon`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': None
        },
    'Quercus ilex':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 21
        },
    'Quercus `Columna`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 20,
        'max_crown': 5
        },
    'Quercus palustris `Green pillar`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 18,
        'max_crown': 3
        },
    'Quercus robur `Fastigiate Koster`':
        {
        'height_class': 1,
        'crown_class': 'small',
        'max_height': 20,
        'max_crown': 4
        },
    'Populus lasiocarpa':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 15
        },
    'Populus nigra `Brandaris`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Populus nigra':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 15
        },
    'Populus canadensis `Robusta`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 15
        },
    'Populus canadensis':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 30,
        'max_crown': 20
        },
    'Populus canescens `De Moffart`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 18
        },
    'Populus canescens':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Populus alba':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 20
        },
    'Populus simonii `Fastigiata`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 10
        },
    'Populus simonii':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 8
        },
    'Populus tremula':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 12
        },
    'Populus trichocarpa':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 30,
        'max_crown': 15
        },
    'Populus berolinensis':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 10
        },
    'Populus nigra `Italica`':
        {
        'height_class': 1,
        'crown_class': 'small',
        'max_height': 25,
        'max_crown': 5
        },
    'Alnus glutinosa `Laciniata`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 8
        },
    'Alnus incana':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 18,
        'max_crown': 10
        },
    'Alnus spaethii `Spaeth`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 18
        },
    'Alnus cordata':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 8
        },
    'Alnus glutinosa `Aurea`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 9
        },
    'Alnus glutinosa':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Alnus subcordata':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Salix alba':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 18
        },
    'Salix babylonica':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 10
        },
    'Salix sepulcralis `Chrysocoma`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 25
        },
    'Salix alba `Chermesina`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 12
        },
    'Salix babylonica `Tortuosa`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 12
        },
    'Salix caprea':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 8,
        'max_crown': 5
        },
    'Salix pentandra':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 10
        },
    'Betula pendula':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 12
        },
    'Betula utilis jacquemontii':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 8
        },
    'Betula ermanii':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 10
        },
    'Betula nigra':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 15,
        'max_crown': 10
        },
    'Betula papyrifera':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Betula pendula `Tristis`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 7
        },
    'Betula pendula `Youngii`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 6,
        'max_crown': 8
        },
    'Betula ermanii `Blush`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 14,
        'max_crown': 8
        },
    'Betula ermanii `Holland`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 8
        },
    'Betula pendula `Laciniata`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 6
        },
    'Betula pubescens':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Betula utilis `Doorenbos`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 10
        },
    'Betula utilis':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 8
        },
    'Betula pendula `Fastigiata`':
        {
        'height_class': 1,
        'crown_class': 'small',
        'max_height': 15,
        'max_crown': 6
        },
    'Betula pendula `Zwitsers Glorie`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 15,
        'max_crown': 8
        },
    'Prunus `Accolade`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 7,
        'max_crown': 5
        },
    'Prunus `Kiku-shidare-zakura`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 6,
        'max_crown': 4
        },
    'Prunus cerasifera `Nigra`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 8,
        'max_crown': 7
        },
    'Prunus serrulata `Kanzan`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 8
        },
    'Prunus serrulata':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 8,
        'max_crown': 10
        },
    'Prunus spinosa':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 4,
        'max_crown': 4
        },
    'Prunus subhirtella `Autumnalis`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 7,
        'max_crown': 5
        },
    'Prunus yedoensis':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 10
        },
    'Prunus `Mahogany Lustre`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 10
        },
    'Prunus `Pandora`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 6,
        'max_crown': 4
        },
    'Prunus `Spire`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 8,
        'max_crown': 4
        },
    'Prunus `Trailblazer`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 7,
        'max_crown': 5
        },
    'Prunus `Umineko`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 8,
        'max_crown': 4
        },
    'Prunus avium `Plena`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 10
        },
    'Prunus avium':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Prunus cerasus':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 12
        },
    'Prunus domestica':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 6,
        'max_crown': 6
        },
    'Prunus maackii':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 8
        },
    'Prunus padus':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 12,
        'max_crown': 8
        },
    'Prunus serotina':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 10
        },
    'Prunus virginiana `Shubert`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 10,
        'max_crown': 8
        },
    'Prunus eminens `Umbraculifera`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 5,
        'max_crown': 3
        },
    'Prunus gondouinii `Schnee`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 6,
        'max_crown': 6
        },
    'Prunus sargentii `Rancho`':
        {
        'height_class': 3,
        'crown_class': 'small',
        'max_height': 8,
        'max_crown': 4
        },
    'Prunus serrulata `Amanogawa`':
        {
        'height_class': 3,
        'crown_class': 'small',
        'max_height': 6,
        'max_crown': 1.5
        },
    'Prunus schmittii':
        {
        'height_class': 3,
        'crown_class': 'small',
        'max_height': 10,
        'max_crown': 4
        },
    'Carpinus betulus `Fastigiata`':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 18,
        'max_crown': 12
        },
    'Carpinus betulus':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 20,
        'max_crown': 15
        },
    'Carpinus japonica':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 10
        },
    'Carpinus betulus `Frans Fontaine`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 10,
        'max_crown': 3
        },
    'Crataegus persimilis `Splendens`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 8,
        'max_crown': 10
        },
    'Crataegus coccinea':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 7,
        'max_crown': 6
        },
    'Crataegus laevigata':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 7,
        'max_crown': 6
        },
    'Crataegus monogyna':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 8,
        'max_crown': 5
        },
    'Crataegus lavalleei':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 7,
        'max_crown': 5
        },
    'Crataegus media `Paul`s Scarlet`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 8,
        'max_crown': 8
        },
    'Crataegus monogyna `Stricta`':
        {
        'height_class': 3,
        'crown_class': 'small',
        'max_height': 10,
        'max_crown': 4
        },
    'Robinia pseudoacacia `Umbraculifera`':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 6,
        'max_crown': 7
        },
    'Robinia viscosa':
        {
        'height_class': 3,
        'crown_class': 'broad',
        'max_height': 10,
        'max_crown': 10
        },
    'Robinia pseudoacacia `Bessoniana`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Robinia pseudoacacia `Frisia`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 9
        },
    'Robinia pseudoacacia `Unifoliola`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 10
        },
    'Robinia pseudoacacia':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 20
        },
    'Robinia ambigua `Bellarosea`':
        {
        'height_class': 3,
        'crown_class': 'regular',
        'max_height': 8,
        'max_crown': None
        },
    'Robinia ambigua `Decaisneana`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 11,
        'max_crown': 10
        },
    'Robinia margaretta `Pink Cascade`':
        {
        'height_class': 2,
        'crown_class': 'regular',
        'max_height': 11,
        'max_crown': 10
        },
    'Robinia pseudoacacia `Pyramidalis`':
        {
        'height_class': 1,
        'crown_class': 'small',
        'max_height': 15,
        'max_crown': 5
        },
    'Aesculus flava':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 18,
        'max_crown': 15
        },
    'Aesculus hippocastanum `Baumannii`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 18
        },
    'Aesculus hippocastanum':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Aesculus pavia':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 8,
        'max_crown': 6
        },
    'Aesculus carnea `Briotii`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 15
        },
    'Aesculus carnea `Plantierensis`':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 12
        },
    'Aesculus carnea':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 20,
        'max_crown': 15
        },
    'Aesculus hippocastanum `Pyramidalis`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 15,
        'max_crown': 6
        },
    'Cornus controversa':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 12,
        'max_crown': 12
        }

}

