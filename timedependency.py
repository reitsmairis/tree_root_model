#############################################################################
# Code for predicting tree dbh, height and crown
#############################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

    # execute equation with corresponding parameter values
    for i in range(len(info)):
        eq = info['EqName'].values[i]
        a, b, c, d, e = info.values[i][8:13]
        y = eval(eq + '(x, a, b, c, d, e)')
        y_values = np.append(y_values, y)

    return np.mean(y_values)


def predict_value(indep_var_value, name, independent_var_str, predicts_str, data_df):

    # check if cultivar name exists in dataframe
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
                info_genus = data_df[(data_df['Scientific Name'].apply(lambda x: str(x.split()[0]) == genus)) & (data_df['Independent variable'] == independent_var_str) & (data_df['Predicts component '] == predicts_str)]
                if not info_genus.empty:
                    value = get_value(info_genus, indep_var_value)
                    return value

                # when dataframe does not contain genus of tree
                else:
                    return None
