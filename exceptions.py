import pandas as pd
import numpy as np

def crown_unknown(height_class, bgt_class, circulation, fast_growth):
    '''If the crown diameter is unknown, take as upper boundary the optimal volume for the tree with a broad crown, and as lower bound the
    marginal volume for the tree with a small crown. The middle value is the reasonable volume with a regular crown.'''

    # read out data corresponding to type of growth
    if fast_growth == True:
        df = pd.read_csv('data/volume_data_fast.csv')
    else:
        df = pd.read_csv('data/volume_data_regular.csv')

    # determine optimal volume
    init_volume_opt = df.optimal_init[(df.height == height_class) & (df.crown == 'broad') & (df.place == bgt_class)].values[0]
    growth_rate_opt = df.optimal_growth[(df.height == height_class) & (df.crown == 'broad') & (df.place == bgt_class)].values[0]
    optimal_vol = init_volume_opt + circulation * growth_rate_opt

    # determine reasonable volume
    init_volume_rea = df.reasonable_init[(df.height == height_class) & (df.crown == 'regular') & (df.place == bgt_class)].values[0]
    growth_rate_rea = df.reasonable_growth[(df.height == height_class) & (df.crown == 'regular') & (df.place == bgt_class)].values[0]
    reasonable_vol = init_volume_rea + circulation * growth_rate_rea

    # determine marginal volume
    init_volume_mar = df.marginal_init[(df.height == height_class) & (df.crown == 'small') & (df.place == bgt_class)].values[0]
    growth_rate_mar = df.marginal_growth[(df.height == height_class) & (df.crown == 'small') & (df.place == bgt_class)].values[0]
    marginal_vol = init_volume_mar + circulation * growth_rate_mar

    return np.array([optimal_vol, reasonable_vol, marginal_vol])


def bgt_unknown(height_class, crown_class, circulation, fast_growth):
    '''..'''
    # read out data corresponding to type of growth
    if fast_growth == True:
        df = pd.read_csv('data/volume_data_fast.csv')
    else:
        df = pd.read_csv('data/volume_data_regular.csv')

    # determine optimal volume
    init_volume_opt = df.optimal_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'heavy_load')].values[0]
    growth_rate_opt = df.optimal_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'heavy_load')].values[0]
    optimal_vol = init_volume_opt + circulation * growth_rate_opt

    # determine reasonable volume as average of two middle classes
    init_volume_light = df.reasonable_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'light_load')].values[0]
    growth_rate_light = df.reasonable_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'light_load')].values[0]
    init_volume_moderate = df.reasonable_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'moderate_load')].values[0]
    growth_rate_moderate = df.reasonable_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'moderate_load')].values[0]
    init_volume_rea = (init_volume_light + init_volume_moderate)/2
    growth_rate_rea = (growth_rate_light + growth_rate_moderate)/2
    reasonable_vol = init_volume_rea + circulation * growth_rate_rea

    # determine marginal volume
    init_volume_mar = df.marginal_init[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'open_ground')].values[0]
    growth_rate_mar = df.marginal_growth[(df.height == height_class) & (df.crown == crown_class) & (df.place == 'open_ground')].values[0]
    marginal_vol = init_volume_mar + circulation * growth_rate_mar

    return np.array([optimal_vol, reasonable_vol, marginal_vol])
