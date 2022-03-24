#############################################################################
# Code for interpolating the rootvolume numbers
#
# Soure of the number represented in the dataframe:
# Rekenprogramma boommonitor
# Norminstituut Bomen
#############################################################################

import numpy as np
import copy
import pandas as pd


def rootdata_preparation(df, year_interval, base, output_name):
    '''Takes a csv file with output numbers from the calculation program boommonitor (https://www.norminstituutbomen.nl/instrumenten/boommonitor/)
    and converts it to be usable for the rootvolume calculation'''

    # convert root volumes to list of floats
    df_conv = copy.deepcopy(df)
    df_conv.optimal = df.optimal.str.split(',').apply(lambda x: [float(i) for i in x])
    df_conv.reasonable = df.reasonable.str.split(',').apply(lambda x: [float(i) for i in x])
    df_conv.marginal = df.marginal.str.split(',').apply(lambda x: [float(i) for i in x])

    # compute differences between intervals of year_interval
    df_conv['differences_opt'] = df_conv.optimal.apply(lambda x: [x[i+1] - x[i] for i in range(len(x[:-1]))])
    df_conv['differences_rea'] = df_conv.reasonable.apply(lambda x: [x[i+1] - x[i] for i in range(len(x[:-1]))])
    df_conv['differences_mar'] = df_conv.marginal.apply(lambda x: [x[i+1] - x[i] for i in range(len(x[:-1]))])

    # compute growth rate per year
    df_conv['optimal_growth'] = df_conv.differences_opt.apply(lambda x: np.mean(x)/year_interval)
    df_conv['reasonable_growth'] = df_conv.differences_rea.apply(lambda x: np.mean(x)/year_interval)
    df_conv['marginal_growth'] = df_conv.differences_mar.apply(lambda x: np.mean(x)/year_interval)

    # calculate initial root volume of trees
    df_conv['optimal_init'] = df_conv.optimal.apply(lambda x: x[0]) - base * df_conv.optimal_growth
    df_conv['reasonable_init'] = df_conv.reasonable.apply(lambda x: x[0]) - base * df_conv.reasonable_growth
    df_conv['marginal_init'] = df_conv.marginal.apply(lambda x: x[0]) - base * df_conv.marginal_growth

    # store relevant information in new dataframe
    df_final = df_conv[['height', 'crown', 'place', 'optimal', 'reasonable', 'marginal', 'optimal_growth', 'reasonable_growth', 'marginal_growth', 'optimal_init', 'reasonable_init', 'marginal_init']]
    df_final.to_csv('data/{}.csv'.format(output_name))


# for regular growing trees
base = 20 # the years of the first number in the output matrix from boommonitor
year_interval = 20 # the amount of years between the numbers in the output matrix from boommonitor
df = pd.read_csv('data/boommonitor_data.csv', sep=';')
output_name = 'volume_data_regular'
rootdata_preparation(df, year_interval, base, output_name)

# for fast growing trees
base = 15 # the years of the first number in the output matrix from boommonitor
year_interval = 10 # the amount of years between the numbers in the output matrix from boommonitor
df = pd.read_csv('data/boommonitor_data.csv', sep=';')
output_name = 'volume_data_fast'
rootdata_preparation(df, year_interval, base, output_name)
