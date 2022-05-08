# -*- coding: utf-8 -*-
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
import pandas as pd


def get_url(year):
    return f'https://s3.amazonaws.com/capitalbikeshare-data/{year}-capitalbikeshare-tripdata.zip'


zip_url = 'https://s3.amazonaws.com/capitalbikeshare-data/2010-capitalbikeshare-tripdata.zip'
zip_folder = '2010-capitalbikeshare-tripdata.zip'
ind_url = 'https://s3.amazonaws.com/capitalbikeshare-data/index.html'

years = [
    year
    for year in range(2010, 2018)
] + [
    str(year) + str(month).zfill(2)
    for year in range(2018, 2019)
    for month in range(1, 13)
]


def get_bike_data(file_path, is_folder):
    """
    params:
        file_path: (str) path of the zipfile, can be a downloaded zipfolder or a url of zipfile
        is_folder: (bool) should be true if the file_path is a downloaded folder and
                    false, if the file_path is the url to the zipfile on the bucket.
    returns:
        pandas DataFrame read in from the CSV file
    """
    if is_folder:
        with ZipFile(file_path) as zf:
            df = pd.read_csv(zf.open(zf.namelist()[0]))
            
    else:
        http_response = urlopen(file_path)
        with ZipFile(BytesIO(http_response.read())) as zf:
            df = pd.DataFrame()
            files = zf.namelist()
            for file in files:
                if file.endswith('.csv') and '__MACOSX' not in file:
                    df = pd.concat([df, pd.read_csv(zf.open(file))])

            # df = pd.read_csv(zf.open(zf.namelist()[0]))

    df['Start date'] = pd.to_datetime(df['Start date'])
    df['End date'] = pd.to_datetime(df['End date'])
    
    return df


if __name__ == '__main__':
    bike_share_df = get_bike_data(zip_url, is_folder=False)
    print(bike_share_df.head())

