import numpy as np
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from exceptions import crown_unknown, bgt_unknown
from treedict import fast_growers, tree_properties

def main_treedict(year, mesh, name, tree_number, bgt_class, origin, type):
    '''for 1 tree'''
    
    # if year of planting is not known it is not possible to determine rootvolume
    if origin == 0:
        print('year of planting was not known so rootvolume could not be determined')
        return np.array([0, 0, 0])
    circulation = year - origin
    print('origin', origin)

    # determine if tree grows fast or regular
    group = name.split()
    genus = str(group[0])
    if genus in fast_growers:
        fast_growth = True
    else:
        fast_growth = False

    # check boommonitor dict
    if name in tree_properties:
        attributes = tree_properties[name]
        print(name, attributes)
        height_class = attributes['height_class']
        crown_class = attributes['crown_class']
    else:
        height_class = None
        crown_class = None
        print('this tree species is not yet classified:', name)
    print('height class', height_class, 'crown class', crown_class)
    if not height_class:
        print('height class was not known so rootvolume could not be determined')
        return np.array([0, 0, 0])

    # if crown size & bgt value unknown
    if not crown_class and not bgt_class:
        print('both crownsize and bgt value unknown, rootvolume cannot be determined for tree', tree_number)
        return np.array([0, 0, 0])

    # what if bgt value unknown
    elif crown_class and not bgt_class:
        rootvolume = bgt_unknown(height_class, crown_class, circulation, fast_growth)
        print('bgt was unknown')

    # what if tree is not Cobra dataset (thus crown not known)
    elif not crown_class and bgt_class:
        rootvolume = crown_unknown(height_class, bgt_class, circulation, fast_growth)
        print('crownsize was unknown')

    else:
        print('no unknowns')
        # determine necessery root volume (TODO hier forloopje overheen voor grootte over tijd?)
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)
        print('rootvolume', rootvolume)

    return rootvolume


