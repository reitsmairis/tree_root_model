# code om bomen in bounding box te selecteren, kan een stuk mooier maar ook ff afwachten wat ik met de cobra data mag en of ik t daarvoor dus ook moet doen

from helpers import wgs_to_rd
import pandas as pd
import copy

# define bounding box with two coorinates of vertices of box
lat_1, lng_1 = 52.355310, 4.892947
lat_2, lng_2 = 52.353315, 4.899928

# x_1, y_1 = wgs_to_rd(lat_1, lng_1)
# x_2, y_2 = wgs_to_rd(lat_2, lng_2)
#
# x_values = [x_1, x_2]
# y_values = [y_1, y_2]
#
# x_min = min(x_values)
# x_max = max(x_values)
# y_min = min(y_values)
# y_max = max(y_values)
# print('oi', x_1, y_1)
# print(x_min, x_max)
# print(y_min, y_max)

lat_values = [lat_1, lat_2]
lng_values = [lng_1, lng_2]
max_lat = max(lat_values)
min_lat = min(lat_values)
max_lng = max(lng_values)
min_lng = min(lng_values)

df0 = pd.read_csv('data/BOMEN_0.csv', sep=';')
df1 = pd.read_csv('data/BOMEN_1.csv', sep=';')
df2 = pd.read_csv('data/BOMEN_2.csv', sep=';')
df3 = pd.read_csv('data/BOMEN_3.csv', sep=';')

df_tot = pd.concat([df0, df1, df2, df3], ignore_index = True)


df_selected = copy.deepcopy(df_tot)
for index, row in df_tot.iterrows():
    # print(index)
    if index % 100 == 0:
        print(index)
    lat, lng = row['LAT'], row['LNG']
    if lat > min_lat and lat < max_lat and lng > min_lng and lng < max_lng:
        print('inside')
    else:
        # print('outside')
        df_selected = df_selected.drop(index)
df_selected.to_csv('data/sarphati_trees.csv')
