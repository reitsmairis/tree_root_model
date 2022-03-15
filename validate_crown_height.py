import pandas as pd
import numpy as np
import os
import datetime
from helpers import wgs_to_rd
from exceptions import crown_unknown, bgt_unknown
from timedependency import *
import matplotlib.pyplot as plt


def validate(year, name, tree_number, origin, type, data_df):
    '''for 1 tree'''
    # todo cobra df maybe van tevoren al splitten dat ik niet steeds heel df meegeef

    # if year of planting is not known it is not possible to determine rootvolume
    if origin == 0:
        print('year of planting was not known so rootvolume could not be determined')
        return 0, 0
    circulation = year - origin
    print('origin', origin)

    # age is the same as circulation
    age = year - origin

    dbh = predict_value(age, name, 'age', 'dbh', data_df)
    print('dbh', dbh)

    # determine height and crown class
    height = predict_value(dbh, name, 'dbh', 'tree ht', data_df)
    if not height:
        print('height could not be determined so rootvolume could not be determined')
        return 0, 0

    crown_diameter = predict_value(dbh, name, 'dbh', 'crown dia', data_df)
    print('height', height, 'crown', crown_diameter)


    return height, crown_diameter



data_year = 2020 # from what year is the data (tree crown/height especially)


# todo eigenlijk ook ff met select_trees voor goede coords doen
cobra_df = pd.read_csv('data/cobra_data.csv')
df = pd.read_csv('data/wallengebied_trees.csv')

# load in df from paper
data_df = pd.read_csv('data/RDS-2016-0005/Data/TS6_Growth_coefficients.csv')
climate = 'PacfNW'
data_df = data_df.drop(data_df[data_df.Region != climate].index)
species = data_df['Scientific Name'].unique()

height_list_model = [[],[]]
crown_list_model = [[],[]]
height_list_data = [[],[]]
crown_list_data = [[],[]]
height_list_cobra = [[],[]]
height_list_model_cobra = [[],[]]

for index, tree in df.iterrows():
    print()
    i = 0
    # if index > 5:
    #     continue

    # retrieve tree id
    tree_number = tree['Boomnummer']
    # use object number if tree number is unknown (=0)
    if tree_number == 0:
        tree_number = 'objNR_' + str(tree['OBJECTNUMMER'])
    print('tree_number', tree_number)

    # read out name and type
    name = tree['Soortnaam_WTS']

    if name in species:
        i = 1
    type = tree['Boomtype']
    if type == 'Vormboom' or type == 'Knotboom':
        continue
    print('name', name, 'type', type)

    # read out origin
    origin = tree['Plantjaar']

    # predict height and crown with model
    height_model, crown_model = validate(data_year, name, tree_number, origin, type, data_df)

    # read out height string from gemeente data and convert to average of the range
    height_string = tree['Boomhoogte']
    if height_string != 'Onbekend' and height_model != 0:
        height_range = []
        for word in height_string.split():
            if word.isdigit():
                height_range.append(int(word))
        height_data = np.mean(height_range)
        height_list_data[i].append(height_data)
        height_list_model[i].append(height_model)

    # retrieve cobra crown
    index = cobra_df.index[cobra_df.uid_gemeente == tree_number]
    if len(index) != 0 and crown_model != 0:
        crown_data = cobra_df.at[index[0], 'kroondiameter']
        height_cobra = cobra_df.at[index[0], 'boomhoogte']
        if height_cobra > 3:
            height_list_cobra[i].append(height_cobra)
            height_list_model_cobra[i].append(height_model)
            crown_list_data[i].append(crown_data)
            crown_list_model[i].append(crown_model)


plt.title('IJburg', fontsize=14)
plt.scatter(height_list_model[0], height_list_data[0], c='C0', alpha=0.4, label='genus')
plt.scatter(height_list_model[1], height_list_data[1], c='C1', alpha=0.4, label='species')
plt.xlabel('model height (m)', fontsize=14)
plt.ylabel('data height (m)', fontsize=14)
x=np.arange(0,50,1)
plt.plot(x, x, c='black')
plt.fill_between(x, x+1.5, x-1.5, color='black', alpha=0.1)
plt.legend()
plt.savefig('plots/gemeente_height_wallengebied', dpi=300)
plt.show()

plt.title('IJburg', fontsize=14)
plt.scatter(height_list_model_cobra[0], height_list_cobra[0], c='C0', alpha=0.4, label='genus')
plt.scatter(height_list_model_cobra[1], height_list_cobra[1], c='C1', alpha=0.4, label='species')
plt.xlabel('model height (m)', fontsize=14)
plt.ylabel('cobra height (m)', fontsize=14)
x=np.arange(0,50,1)
plt.plot(x, x, c='black')
plt.legend()
plt.savefig('plots/cobra_height_wallengebied', dpi=300)
plt.show()

plt.title('IJburg', fontsize=14)
plt.scatter(crown_list_model[0], crown_list_data[0], c='C0', alpha=0.4, label='genus')
plt.scatter(crown_list_model[1], crown_list_data[1], c='C1', alpha=0.4, label='species')
plt.xlabel('model crown (m)', fontsize=14)
plt.ylabel('data crown (m)', fontsize=14)
x=np.arange(0,25,1)
plt.plot(x, x, c='black')
plt.legend()
plt.savefig('plots/crown_wallengebied', dpi=300)
plt.show()
