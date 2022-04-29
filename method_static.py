#############################################################################
# Static rootvolume method
#############################################################################

import numpy as np
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from treedict import fast_growers


def main_static(year, mesh, name, tree_number, bgt_class, origin, type, rd_x, rd_y, height, crown):

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

    # determine rootvolume
    if not crown or not bgt_class:
        return np.array([0, 0, 0])
    else:
        crown_class = crown_classifier(crown, height, type)
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)

    return rootvolume

