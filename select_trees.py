#############################################################################
# Code for selecting trees from the gemeente files based on a bounding box
#############################################################################

from helpers import wgs_to_rd
import pandas as pd
import copy


# define bounding box with two coorinates of vertices of box
lat_1, lng_1 = 52.355310, 4.892947
lat_2, lng_2 = 52.353315, 4.899928
lat_values = [lat_1, lat_2]
lng_values = [lng_1, lng_2]
max_lat = max(lat_values)
min_lat = min(lat_values)
max_lng = max(lng_values)
min_lng = min(lng_values)

# read out dataframes containing the gemeente trees
df0 = pd.read_csv('data/BOMEN_0.csv', sep=';')
df1 = pd.read_csv('data/BOMEN_1.csv', sep=';')
df2 = pd.read_csv('data/BOMEN_2.csv', sep=';')
df3 = pd.read_csv('data/BOMEN_3.csv', sep=';')

# concatinate dataframes
df_tot = pd.concat([df0, df1, df2, df3], ignore_index = True)

# select trees that fall within bounding box
df_selected = copy.deepcopy(df_tot)
for index, row in df_tot.iterrows():

    # keep track of progress
    if index % 100 == 0:
        print(index)
    
    # check if tree falls in bounding box, otherwise drop
    lat, lng = row['LAT'], row['LNG']
    if lat > min_lat and lat < max_lat and lng > min_lng and lng < max_lng:
        print('inside')
    else:
        df_selected = df_selected.drop(index)

# save new dataframe
df_selected.to_csv('data/sarphati_trees.csv')
