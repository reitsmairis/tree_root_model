#############################################################################
# Static rootvolume method
#############################################################################

import numpy as np
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from exceptions import crown_unknown, bgt_unknown
from treedict import fast_growers


def main_static(year, mesh, name, tree_number, bgt_class, origin, type, rd_x, rd_y, height, crown):

    # if year of planting is not known it is not possible to determine rootvolume
    if origin == 0:
        return np.array([0, 0, 0])

    # determine circulation of tree
    circulation = year - origin

    # determine if tree grows fast or regular
    group = name.split()
    genus = str(group[0])
    if genus in fast_growers:
        fast_growth = True
    else:
        fast_growth = False

    # determine height class
    height_class = height_classifier(height)

    # if crown size & bgt value unknown
    if not crown and not bgt_class:
        return np.array([0, 0, 0])

    # determine rootvolume 
    elif crown and not bgt_class:
        crown_class = crown_classifier(crown, height, type)
        rootvolume = bgt_unknown(height_class, crown_class, circulation, fast_growth)
    elif not crown and bgt_class:
        rootvolume = crown_unknown(height_class, bgt_class, circulation, fast_growth) 
    else:
        crown_class = crown_classifier(crown, height, type)
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)

    return rootvolume

