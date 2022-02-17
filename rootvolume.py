import numpy as np
import pandas as pd


def rootvolume_calc(height_class, crown_class, bgt_class, circulation, fast_growth):
    '''Returns the optimal, reasonable and marginal root volumes of a tree with the input parameters.'''

    # read out data corresponding to type of growth
    if fast_growth == True:
        df = pd.read_csv('data/volume_data_fast.csv')
    else:
        df = pd.read_csv('data/volume_data_regular.csv')

    # determine optimal volume
    init_volume_opt = df.optimal_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == bgt_class)].values[0]
    growth_rate_opt = df.optimal_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == bgt_class)].values[0]
    optimal_vol = init_volume_opt + circulation * growth_rate_opt

    # determine reasonable volume
    init_volume_rea = df.reasonable_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == bgt_class)].values[0]
    growth_rate_rea = df.reasonable_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == bgt_class)].values[0]
    reasonable_vol = init_volume_rea + circulation * growth_rate_rea

    # determine marginal volume
    init_volume_mar = df.marginal_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == bgt_class)].values[0]
    growth_rate_mar = df.marginal_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == bgt_class)].values[0]
    marginal_vol = init_volume_mar + circulation * growth_rate_mar

    return np.array([optimal_vol, reasonable_vol, marginal_vol])


def height_classifier(h):
    '''Takes height of tree as input and classifies them into one
    of the three boommonitor classifications.'''

    # assign height class
    if h >= 15:
        height_class = 1
    if 8 <= h < 15:
        height_class = 2
    if h < 8:
        height_class = 3

    return height_class

def crown_classifier(c, h, type):
    '''Takes crown diameter of tree as input and classifies them into the
    boommonitor classifications.'''

    if type == 'Vormboom' or type == 'Knotboom':
        if c >= 5:
            crown_class = 'broad'
        if 3 <= c < 5:
            crown_class = 'regular'
        if c < 3:
            crown_class = 'small'
    else:
        if h >= 15:
            if c >= 15:
                crown_class = 'broad'
            if 10 <= c < 15:
                crown_class = 'regular'
            if c < 10:
                crown_class = 'small'
        if 8 <= h < 15:
            if c >= 12:
                crown_class = 'broad'
            if 8 <= c < 12:
                crown_class = 'regular'
            if c < 8:
                crown_class = 'small'
        if h < 8:
            if c >= 8:
                crown_class = 'broad'
            if 5 <= c < 8:
                crown_class = 'regular'
            if c < 5:
                crown_class = 'small'

    return crown_class

# # test
# h = 16
# c = 16
# circulation = 80
# bgt_class = 'light_load'
#
# height_class, crown_class = rootvolume_classifier(h, c)
# rootvolume = rootvolume_calc(height_class, crown_class, bgt_class, circulation)
#
#
# print(rootvolume)
