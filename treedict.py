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
    'Robinia pseudoacacia':
        {
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 25,
        'max_crown': 18
        },
    'Tilia europaea `Zwarte Linde`':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Aesculus hippocastanum':
        {
        'height_class': 1,
        'crown_class': 'broad',
        'max_height': 25,
        'max_crown': 20
        },
    'Pyrus calleryana `Chanticleer`':
        {
        'height_class': 2,
        'crown_class': 'small',
        'max_height': 12,
        'max_crown': 6
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
        'height_class': 1,
        'crown_class': 'regular',
        'max_height': 15,
        'max_crown': 8
        },
    'Cornus controversa':
        {
        'height_class': 2,
        'crown_class': 'broad',
        'max_height': 12,
        'max_crown': 12
        },

}
#
# x = None
# if x:
#     print('oi')
# if not x:
#     print('doei')
# species_list = []
# df = pd.read_csv('Wallen_trees.csv')
# for index, tree in df.iterrows():
#     # read out name
#     name = tree['Soortnaam_WTS']
#     # print('name', name)
#     species_list.append(name)
#     # if name in tree_properties:
#     #     properties = tree_properties[name]
#     #     print(name, properties)
#     #     c = properties['max_crown']
#     #     print(c)
#     #     print()
#
# print(Counter(species_list))
# print(len(species_list))
