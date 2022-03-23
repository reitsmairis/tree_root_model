import numpy as np
from rootvolume import rootvolume_calc, height_classifier, crown_classifier
from exceptions import crown_unknown, bgt_unknown
from treedict import fast_growers

def main_static(year, mesh, name, tree_number, bgt_class, origin, type, rd_x, rd_y, height, crown):
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

    # determine height class
    height_class = height_classifier(height)



    # if crown size & bgt value unknown
    if not crown and not bgt_class:
        print('both crownsize and bgt value unknown, rootvolume cannot be determined for tree', tree_number)
        return np.array([0, 0, 0])

    # what if bgt value unknown
    elif crown and not bgt_class:
        print('bgt was unknown')
        crown_class = crown_classifier(crown, height, type)
        rootvolume = bgt_unknown(height_class, crown_class, circulation, fast_growth)


    # what if tree is not in Cobra Groeninzicht dataset (thus crown not known)
    elif not crown and bgt_class:
        rootvolume = crown_unknown(height_class, bgt_class, circulation, fast_growth)
        print('crownsize was unknown')


    else:
        print('no unknowns')
        crown_class = crown_classifier(crown, height, type)

        # determine necessery root volume (TODO hier forloopje overheen voor grootte over tijd?)
        rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth)
        print('rootvolume', rootvolume)

    return rootvolume

