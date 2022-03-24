#############################################################################
# Tree growth rootvolume method
#############################################################################

import numpy as np
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from exceptions import crown_unknown, bgt_unknown
from timedependency import *
from treedict import fast_growers


def main_treegrowth(year, mesh, name, tree_number, bgt_class, origin, type, data_df):

    # if year of planting is not known it is not possible to determine rootvolume
    if origin == 0:
        return np.array([0, 0, 0])

    # determine circulation of tree
    circulation = year - origin

    # age is the same as circulation
    age = year - origin

    # determine if tree grows fast or regular
    group = name.split()
    genus = str(group[0])
    if genus in fast_growers:
        fast_growth = True
    else:
        fast_growth = False

    # predict tree dbh
    dbh = predict_value(age, name, 'age', 'dbh', data_df)

    # determine height and crown class
    height = predict_value(dbh, name, 'dbh', 'tree ht', data_df)
    if not height:
        return np.array([0, 0, 0])
    height_class = height_classifier(height)
    crown_diameter = predict_value(dbh, name, 'dbh', 'crown dia', data_df)
    crown_class = crown_classifier(crown_diameter, height, type)

    # determine rootvolume
    if not bgt_class:
        rootvolume = bgt_unknown(height_class, crown_class, circulation, fast_growth)
    else:
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)

    return rootvolume 



