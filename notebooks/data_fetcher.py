import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class Fetcher(BaseEstimator, TransformerMixin):

    def __init__(self, building_id=122, meter=0, primary_use=99):  # 99 referes to none

        self.building_id = building_id
        # self.meter = meter
        self.primary_use = primary_use

    def fit(self, x, y=None):
        return self  # nothing else to do

    def season_finder(self, month):  # 0 for spring - 1 for summer - 2 for fall - 3 for winter
        if month in [3, 4, 5]:
            return 0
        elif month in [6, 7, 8]:
            return 1
        elif month in [9, 10, 11]:
            return 2
        elif month in [12, 1, 2]:
            return 3

    def transform(self, x):
        df = x.copy()
        # Drop columns if they exist
        columns_to_drop = ['Unnamed: 0', 'precip_depth_1_hr', 'cloud_coverage', 'site_id']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

        # Filter the DataFrame based on building_id and primary_use
        if 'building_id' in df.columns and 'primary_use' in df.columns:
            if self.primary_use == 99:
                df = df.query(f'building_id=={self.building_id}')
                df.drop(['building_id', 'primary_use'], axis=1, inplace=True)
            else:
                df = df.query(f'building_id=={self.building_id} & primary_use =={self.primary_use}')
                df.drop(['building_id', 'primary_use'], axis=1, inplace=True)
        

        # Check if the timestamp column exists and perform related transformations
        if 'timestamp' in df.columns:
            df.loc[:, "timestamp"] = pd.to_datetime(df.loc[:, "timestamp"])
            df['season'] = df['timestamp'].dt.month.apply(self.season_finder)
            df['weekend'] = df['timestamp'].dt.dayofweek > 4
            df['day_of_the_week'] = df['timestamp'].dt.dayofweek
            df.set_index('timestamp', inplace=True)
        else:
            df['season'] = df['month'].apply(self.season_finder)
            df['weekend'] = df['day_of_the_week'] > 4  # Assuming 'day_of_the_week' is provided directly
            # If day_of_the_week is not provided, you might need to handle it differently

        return df


class Do_nothing(BaseEstimator, TransformerMixin):

    def __init__(self):  # 99 referes to none
        return

    def fit(self, x, y=None):
        return self  # nothing else to do

    def transform(self, x):
        return x.astype(int)
