#############################################################################
# Code for selecting the correct climate data.
#############################################################################

import pandas as pd

# select climate
climate = 'PacfNW'

# load in df from paper and drop other climates
data_df = pd.read_csv('data/RDS-2016-0005/Data/TS6_Growth_coefficients.csv')
data_df = data_df.drop(data_df[data_df.Region != climate].index)
data_df.to_csv('data/grow_data.csv', index=False)