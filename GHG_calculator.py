#############################################################################
# Code for calculating the GHG values of groundwater level measures
#############################################################################

import pandas as pd
import numpy as np
import copy
import os


def convert_years(df):
    df_hyd = copy.deepcopy(df)

    # transform years to hydrolic years
    df_hyd['hydrolic_year'] = None
    hydyear = 0
    years_done = []
    for row in df_hyd.iterrows():
        index = row[0]
        year = int(row[1].year)
        month = int(row[1].month)
        day = int(row[1].day)

        # detect start of new hydrolic year
        if month <= 3 and day <= 31 and year not in years_done:
            hydyear += 1
            years_done.append(year)

        # if no measurement in first tree months, also change to other hydrolic year
        if years_done:
            if years_done[-1] - year > 1:
                hydyear += 1

        # save hydrolic year to dataframe
        df_hyd['hydrolic_year'][index] = hydyear

    return df_hyd


def calculate_GHG(df):

    # remove data that is not groundwater level measure
    index_date = df.index[df.parameter == 'datum'][0]
    df = df.iloc[index_date + 1: , :]

    # split year, month, day into seperate columns
    df['year'] = df['parameter'].apply(lambda x: str(x)[0:4])
    df['month'] = df['parameter'].apply(lambda x: str(x)[5:7])
    df['day'] = df['parameter'].apply(lambda x: str(x)[8:11])

    # convert values to floats
    df['value'] = df['value'].apply(lambda x: float(x.replace(',', '.')))

    # convert years to hydrolic years
    df = convert_years(df)

    # calculate 1st place
    group_1 = df.groupby('hydrolic_year')
    max_1 = group_1['value'].transform(lambda x: max(x))
    df['max_1'] = max_1
    df_2 = df.drop(index=df[df.value == df.max_1].index, axis=0)

    # calculate 2nd place
    group_2 = df_2.groupby('hydrolic_year')
    max_2 = group_2['value'].transform(lambda x: max(x))
    df_2['max_2'] = max_2
    df_3 = df_2.drop(index=df_2[df_2.value == df_2.max_2].index, axis=0)

    # calculate 3rd place
    group_3 = df_3.groupby('hydrolic_year')
    max_3 = group_3['value'].transform(lambda x: max(x))
    df_3['max_3'] = max_3

    # calculate GHGs
    df_3['GHG'] = (df_3['max_1'] + df_3['max_2'] + df_3['max_3'])/3
    grouped = df_3.groupby('hydrolic_year')
    GHG_df = grouped.mean()

    # calculate mean of GHGs
    GHG_mean = GHG_df['GHG'].mean()

    return GHG_mean


def create_points(files, path):
    '''Creates 3D points of (x,y)-coordinates and their GHG value and saves them as np.array'''

    points = []

    # loop through groundwaterlevel measure files
    for f in files:
        print(f)
        df = pd.read_csv(path + '/{}'.format(f), sep=';', encoding_errors='ignore', index_col=False, names=['parameter', 'value', 'unit'])
        GHG = calculate_GHG(df)

        # find x and y coordinate of measurement
        index_x = df.index[df.parameter == 'x-cordinaat'][0]
        index_y = df.index[df.parameter == 'y-cordinaat'][0]
        x = df.at[index_x, 'value']
        y = df.at[index_y, 'value']

        # save 3D point
        points.append([x, y, GHG])

    return np.array(points)


#################################### main ############################################

path = r"C:\Users\Iris Reitsma\Documents\Master\jaar 2\stage\notmain_code\grondwaterdata" # choose path to load groundwater measurements

# determine GHG values
files = os.listdir(path)
points = create_points(files, path)

np.save('grondwater/GHG_values_Amsterdam', points) # choose path to save GHG value output

######################################################################################