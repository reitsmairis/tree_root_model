import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import fsolve
import math


def lin(x, a, b, c, d, e):
    '''linear'''
    y = a + b*x
    return y

def quad(x, a, b, c, d, e):
    '''quadratic'''
    y = a + b*x + c*x**2
    return y

def cub(x, a, b, c, d, e):
    '''cubic'''
    y = a + b*x + c*x**2 + d*x**3
    return y

def quart(x, a, b, c, d, e):
    '''quartic'''
    y = a + b*x + c*x**2 + d*x**3 + e*x**4
    return y

def loglogw1(x, a, b, mse, d, e):
    '''loglog, weight 1'''
    y = np.exp(a + b*np.log(np.log(x + 1)) + mse/2)
    return y

def loglogw2(x, a, b, mse, d, e):
    '''loglog, weight 1/SQRT(x)'''
    y = np.exp(a + b*np.log(np.log(x + 1)) + np.sqrt(x)*mse/2)
    return y

def loglogw3(x, a, b, mse, d, e):
    '''loglog, weight 1/x'''
    y = np.exp(a + b*np.log(np.log(x + 1)) + x*mse/2)
    return y

def loglogw4(x, a, b, mse, d, e):
    '''loglog, weight 1/x^2'''
    y = np.exp(a + b*np.log(np.log(x + 1)) + x**2*mse/2)
    return y

def expow1(x, a, b, mse, d, e):
    '''exponential, weight 1'''
    y = np.exp(a + b*x + mse/2)
    return y

def expow2(x, a, b, mse, d, e):
    '''exponential, weight 1/SQRT(x)'''
    y = np.exp(a + b*x + np.sqrt(x)*mse/2)
    return y

def expow3(x, a, b, mse, d, e):
    '''exponential, weight 1/x'''
    y = np.exp(a + b*x + x*mse/2)
    return y

def expow4(x, a, b, mse, d, e):
    '''exponential, weight 1/x^2'''
    y = np.exp(a + b*x + x**2*mse/2)
    return y


def get_value(info, x):
    ''' go from x to y'''
    y_values = np.array([])

    for i in range(len(info)):
        eq = info['EqName'].values[i]
        a, b, c, d, e = info.values[i][8:13]
        y = eval(eq + '(x, a, b, c, d, e)')
        y_values = np.append(y_values, y)

    return np.mean(y_values)


def intersect_value(info, y):
    ''' go from y to x'''
    x_values = np.array([])

    for i in range(len(info)):
        eq = info['EqName'].values[i]

        # change nan values to 0, otherwise intersection wont work
        params = info.values[i][8:13]
        params_0 = [0 if math.isnan(j) else j for j in params]
        a, b, c, d, e = params_0

        # calculate intersection
        x = fsolve(lambda q: eval(eq + '(q, *{})'.format((a,b,c,d,e))) - y, x0=10)
        x_values = np.append(x_values, x)

    return np.mean(x_values)

def predict_value(indep_var_value, name, independent_var_str, predicts_str):
    info = data_df[(data_df['Scientific Name'] == name) & (data_df['Independent variable'] == independent_var_str) & (data_df['Predicts component '] == predicts_str)]
    if not info.empty:
        value = get_value(info, indep_var_value)
        return value

    # start checking without cultivar name
    else:
        group = name.split()
        if len(group) > 1:
            species = str(group[0] + ' ' + group[1])
            genus = str(group[0])

            # check species without cultivar name
            info_species = data_df[(data_df['Scientific Name'].apply(lambda x: str(x.split()[0] + ' ' + x.split()[1]) == species)) & (data_df['Independent variable'] == independent_var_str) & (data_df['Predicts component '] == predicts_str)]

            if not info_species.empty:
                value = get_value(info_species, indep_var_value)
                return value

            # start checking with only genus
            else:
                # check genus
                info_genus = data_df[(data_df['Scientific Name'].apply(lambda x: str(x.split()[0]) == genus)) & (data_df['Independent variable'] == independent_var_str) & (data_df['Predicts component '] == predicts_str)]
                if not info_genus.empty:
                    value = get_value(info_genus, indep_var_value)
                    return value

                else:
                    return None


def dbh_from_height(height, name):
    # dbh calc from height
    info = data_df[(data_df['Scientific Name'] == name) & (data_df['Independent variable'] == 'dbh') & (data_df['Predicts component '] == 'tree ht')]
    if not info.empty:
        dbh = intersect_value(info, height)
        return dbh

    # start checking without cultivar name
    else:
        group = name.split()
        if len(group) > 1:
            species = str(group[0] + ' ' + group[1])
            genus = str(group[0])

            # check species without cultivar name
            info_species = data_df[(data_df['Scientific Name'].apply(lambda x: str(x.split()[0] + ' ' + x.split()[1]) == species)) & (data_df['Independent variable'] == 'dbh') & (data_df['Predicts component '] == 'tree ht')]
            if not info_species.empty:
                dbh = intersect_value(info_species, height)
                return dbh

            # start checking with only genus
            else:
                # check genus
                info_genus = data_df[(data_df['Scientific Name'].apply(lambda x: str(x.split()[0]) == genus)) & (data_df['Independent variable'] == 'dbh') & (data_df['Predicts component '] == 'tree ht')]
                if not info_genus.empty:
                    dbh = intersect_value(info_genus, height)
                    return dbh

                else:
                    print('helaas, crown to dbh')
                    return None


def estimate_dbh(cobra_df, gemeente_height, name, tree_number):
    dbh_list = np.array([])
    index = cobra_df.index[cobra_df.uid_gemeente == tree_number]

    # check if cobra estimated tree parameters
    if len(index) != 0 and cobra_df.at[index[0], 'boomhoogte'] != 3.0:

        # calculate dbh from crown
        crown_diameter = cobra_df.at[index[0], 'kroondiameter']
        crown_dbh = predict_value(crown_diameter, name, 'cdia', 'dbh')
        print('crown_dbh', crown_dbh)
        if crown_dbh != None:
            dbh_list = np.append(dbh_list, crown_dbh)

        # # read out Cobra dbh
        # cobra_dbh = cobra_df.at[index[0], 'stamdiameter']
        # print('cobra_dbh', cobra_dbh)
        # dbh_list = np.append(dbh_list, cobra_dbh)

    # calculate dbh from height
    height_dbh = dbh_from_height(gemeente_height, name)
    print('height_dbh', height_dbh)
    if height_dbh != None:
        dbh_list = np.append(dbh_list, height_dbh)

    return np.mean(dbh_list)


#
#
# cobra_df = pd.read_csv('data/cobra_data.csv')
# df = pd.read_csv('Wallen_trees.csv')
#
# # TODO dit als variableen meegeven
# data_df = pd.read_csv('data/RDS-2016-0005/Data/TS6_Growth_coefficients.csv')
# climate = 'PacfNW'
# data_df = data_df.drop(data_df[data_df.Region != climate].index)
#
# years = [2020] # years for which to calculate rootvolume
# for y in years:
#     true_h_list = []
#     calculated_h_list = []
#     for index, tree in df.iterrows():
#         if index < 140:
#             continue
#         print()
#         # retrieve tree id
#         tree_number = tree['Boomnummer']
#         print('tree_number', tree_number)
#
#
#         # read out name
#         name = tree['Soortnaam_WTS']
#         print('name', name)
#
#         height_string = tree['Boomhoogte']
#         height_range = []
#         for word in height_string.split():
#             if word.isdigit():
#                 height_range.append(int(word))
#         gemeente_height = np.mean(height_range) # TODO iets anders dan average? of wat als avarage precies op classification boundary valt?
#         print('gemeente height', gemeente_height)
#
#
#
#         # read out cobra information
#         index = cobra_df.index[cobra_df.uid_gemeente == tree_number]
#
#         if len(index) != 0:
#             crown_diameter = cobra_df.at[index[0], 'kroondiameter']
#             trunk_diameter = cobra_df.at[index[0], 'stamdiameter']
#             cobra_height = cobra_df.at[index[0], 'boomhoogte']
#             print('crown diameter', crown_diameter, 'trunk diameter', trunk_diameter, 'cobra_height', cobra_height)
#             true_h_list.append(crown_diameter)
#         else:
#             true_h_list.append(None)
#
#         dbh = estimate_dbh(cobra_df, gemeente_height, name, tree_number)
#         print('mean dbh', dbh)
#         age = predict_value(dbh, name, 'dbh', 'age')
#         dbh_2020 = predict_value(age, name, 'age', 'dbh')
#         print('dbh_2020', dbh_2020)
#         origin = tree['Plantjaar']
#         print('age', age, 'origin', origin)
#
#         height_2020 = predict_value(dbh_2020, name, 'dbh', 'tree ht')
#         crown_2020 = predict_value(dbh_2020, name, 'dbh', 'crown dia')
#         calculated_h_list.append(crown_2020)
#         print('height 2020', height_2020, 'crown_2020', crown_2020)
#
#         # for future
#         if age == None:
#             age = 0
#         dbh_2040 = predict_value(age + 20, name, 'age', 'dbh')
#         print('dbh_2040', dbh_2040)
#         origin = tree['Plantjaar']
#         print('age', age, 'origin', origin)
#
#         height_2040 = predict_value(dbh_2040, name, 'dbh', 'tree ht')
#         crown_2040 = predict_value(dbh_2040, name, 'dbh', 'crown dia')
#         calculated_h_list.append(crown_2040)
#         print('height 2020', height_2040, 'crown_2020', crown_2040)
# #
# print(len(calculated_h_list))
# plt.scatter(true_h_list, calculated_h_list)
# plt.xlabel('cobra crown', fontsize=14)
# plt.ylabel('estimated crown 2020', fontsize=14)
# x=np.arange(0,25,1)
# plt.plot(x, x, c='C1')
# # plt.fill_between(x, x+1.5, x-1.5, color='C1', alpha=0.1)
# plt.show()
