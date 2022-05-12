#############################################################################
# Tree dictionary rootvolume method
#############################################################################

import numpy as np
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from treedict import fast_growers, tree_properties


def main_treedict(year, name, bgt_class, origin, type):

    # determine circulation of tree
    circulation = year - origin

    # determine if tree grows fast or regular
    group = name.split()
    genus = str(group[0])
    if genus in fast_growers:
        fast_growth = True
    else:
        fast_growth = False

    # check height and crown class boommonitor dict
    if name in tree_properties:
        attributes = tree_properties[name]
        height_class = attributes['height_class']
        crown_class = attributes['crown_class']
    else:
        height_class = None
        crown_class = None
        #print('this tree species is not yet classified:', name)

    # rootvolume cannot be determined if height is not classified
    if not height_class:
        #print('height class was not known so rootvolume could not be determined')
        return np.array([0, 0, 0])

    # determine rootvolume
    if not crown_class or not bgt_class:
        return np.array([0, 0, 0])
    else:
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)

    return rootvolume


