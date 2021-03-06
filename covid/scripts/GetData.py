import csv
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import sys
import math
from datetime import date
import os
from os import listdir
from os.path import isfile, join
from sqlalchemy import create_engine, *

class CovidDataset:
    ### INITIALIZE ###
    def __init__(self):
        # Create dataset paths and get latest data
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.abspath(''))))
        self.reference_data_path = os.path.join(self.BASE_DIR, 'poetry/covid/covid/data/reference')
        self.timeseries_combined_data_path = os.path.join(self.BASE_DIR, 'poetry/covid/covid/data/timeseries/daily_combined')
        self.timeseries_split_data_path = os.path.join(self.BASE_DIR, 'poetry/covid/covid/data/timeseries/daily_split')
        self.timeseries_combined_files = [f for f in listdir(self.timeseries_combined_data_path) if isfile(os.path.join(self.timeseries_combined_data_path, f))]
        self.timeseries_split_files = [f for f in listdir(self.timeseries_split_data_path) if isfile(os.path.join(self.timeseries_split_data_path, f))]
        latest_data_file = max(self.timeseries_combined_files)
        self.latest_data_date = str(latest_data_file)[0:10]
        
        # Compile dictionary of data sources
        self.sources = {
            "confirmed": {
                "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
                "local_path": str(self.timeseries_split_data_path) + '/' + str(self.latest_data_date) + 'confirmed.csv'
            },
            "recovered": {
                "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
                "local_path": str(self.timeseries_split_data_path) + '/' + str(self.latest_data_date) + 'recovered.csv'    
            },
            "deaths": {
                "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
                "local_path": str(self.timeseries_split_data_path) + '/' + str(self.latest_data_date) + 'deaths.csv'
            },
            "combined": {
                "local_path": str(self.timeseries_combined_data_path) + '/' + str(self.latest_data_date) + '-combined.csv'
            },
        }
        self.confirmed_data_raw = {
            'new': self.getNewData('confirmed'),
            'old': self.getOldData('confirmed')
            }
        self.recovered_data_raw = {
            'new': self.getNewData('recovered'),
            'old': self.getOldData('recovered')
            }
        self.deaths_data_raw = {
            'new': self.getNewData('deaths'),
            'old': self.getOldData('deaths')
            }
        self.full_dataset_raw = [self.confirmed_data_raw, self.recovered_data_raw, self.deaths_data_raw]

        self.reference_data = self.loadReferenceData()
        self.needs_reference_data_refresh = False
        self.needs_timeseries_data_refresh = False
    
    ### CREATE DATASETS (REFERENCE AND TIMESERIES) ###
    
    def createNewReferenceData(self):
        # Continents reference data
        continents_df = []
        continents = ["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America", "None"]
        continents_df = pd.DataFrame(continents)
        continent_ids = list(range(0, len(continents)))
        continent_id_column_name = 'continent_id'
        continents_df[continent_id_column_name] = continent_ids
        continents_df.columns = ['name', 'continent_id']
        # Countries-continents reference data
        base_path = self.reference_data_path
        countries_continents_path = base_path + "/country_continent.csv"
        countries_continents_df=pd.read_csv(countries_continents_path, index_col=0)
        # Types reference data
        types_df = pd.DataFrame(["Confirmed", "Recovered", "Deaths"])
        type_ids = list(range(0, len(types_df)))
        type_id_column_name = 'type_id'
        types_df[type_id_column_name] = type_ids
        types_df.columns = ['name', 'type_id']
        # Province/State reference data
        province_state_df = self.deduplicate("Province/State", by_column_range=True, up_to_column=4)
        # Country reference data
        country_df = self.deduplicate("Country/Region", by_column_range=True, up_to_column=4, summarize=True, summary_column='Country/Region')
        province_state_df_merged = pd.merge(province_state_df, country_df, how='inner', on='Country/Region', left_index=False, right_index=False, sort=False,
         suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)
        province_state_df_merged = province_state_df_merged.drop('Country/Region', axis=1).drop('Lat_y', axis=1).drop('Long_y', axis=1)
        province_state_df_merged.columns = ['name', 'lat', 'long', 'province_state_id', 'country_id']
        country_df_merged = pd.merge(country_df, countries_continents_df, how='inner', on='Country/Region', left_index=False, right_index=False, sort=False,
         suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)
        country_df_merged = country_df_merged.drop('Continent', axis=1)
        country_df_merged.columns = ['name', 'lat', 'long', 'country_id', 'continent_id']
        # Combine all reference data into a list
        reference_data_list = [continents_df, countries_continents_df, country_df_merged, province_state_df_merged, types_df]
        keys = ['continent', 'country_continent','country', 'province_state', 'types']
        values = reference_data_list
        reference_data_dict = dict(zip(keys, values))
        self.new_reference_data = reference_data_dict
        return reference_data_dict
    
    def loadReferenceData(self):
        base_path = self.reference_data_path
        continent_path = base_path + "/continent.csv"
        country_path = base_path + "/country.csv"
        province_state_path = base_path + "/province_state.csv"
        countries_continents_path = base_path + "/country_continent.csv"
        types_path = base_path + "/types.csv"
        reference_data_paths = [continent_path, countries_continents_path, country_path, province_state_path, types_path]
        reference_data_list = []
        for path in reference_data_paths:
            df = pd.read_csv(path, index_col=0)
            reference_data_list.append(df)
        keys = ['continent', 'country_continent','country', 'province_state', 'types']
        values = reference_data_list
        reference_data_dict = dict(zip(keys, values))
        return reference_data_dict
    
    ### ACTIONS ###
    def getNewData(self, data_type):
        """Input url of csv, returns dataframe"""
        df = pd.read_csv(self.sources[str(data_type)]['url'])
        return df

    def getOldData(self, data_type):
        """Input filepath of csv, returns dataframe"""
        df = pd.read_csv(self.sources[str(data_type)]['local_path'])
        return df
    
    def deduplicate(self, column_name: str, by_column_range=False, up_to_column=4, summarize=False, summary_column='test'):
        item_list = []
        if by_column_range==True and summarize==False:
            for dataset in self.full_dataset_raw:
                items = pd.DataFrame(dataset['new'].iloc[:,0:up_to_column].drop_duplicates(keep='first').dropna().reset_index().drop(["index"],axis=1))
                item_list.append(items)
        elif by_column_range==True and summarize==True:
            for dataset in self.full_dataset_raw:
                data_by_column = pd.DataFrame(dataset['new'].iloc[:,0:up_to_column]).groupby(summary_column, as_index=False).mean()
                items = data_by_column.iloc[:,0:up_to_column].drop_duplicates(subset=summary_column, keep='first').dropna().reset_index()
                item_list.append(data_by_column)
        else:
            for dataset in self.full_dataset_raw:
                items = pd.DataFrame(dataset['new'][[column_name]].drop_duplicates(keep='first').dropna().reset_index().drop(["index"],axis=1))
                item_list.append(items)
        concatenated_df = pd.concat([item_list[0], item_list[1], item_list[2]], ignore_index=True)
        item_df = concatenated_df.drop_duplicates(subset=column_name, keep='first')
        item_ids = list(range(0, len(item_df)))
        id_column_name = column_name + '_id'
        item_df[id_column_name] = item_ids
        return item_df
    
    def saveData(self):
        timeseries_filenames = ["confirmed", "recovered", "deaths"]
        reference_filenames = ['continent', 'country_continent', 'country', 'province_state', 'types']
        base_dir_split = self.timeseries_split_data_path
        base_dir_combined = self.timeseries_combined_data_path
        base_dir_reference = self.reference_data_path
        for i, item in enumerate(self.full_dataset_cleaned_list):
            filename = base_dir_split + '/' + str(date.today()) + str(timeseries_filenames[i]) + ".csv" 
            item.to_csv(filename)
        filename_combined = base_dir_combined + '/' + str(date.today()) + "-combined.csv" 
        self.full_dataset_cleaned_combined.to_csv(filename_combined)
        
        for i, item in enumerate(self.new_reference_data.items()):
            filename = base_dir_reference + '/' + str(reference_filenames[i]) + ".csv"
            if reference_filenames[i]=='country_continent':
                continue
            item[1].to_csv(filename, index=False)
            
    def standardizeNewData(self):
        full_dataset_cleaned = []
        for i, dataset in enumerate(self.full_dataset_raw):
            # Join country_id, prov_state_id
            dataset_merged_country = pd.merge(dataset['new'], self.new_reference_data['country'].iloc[:,[0,3]], how='inner', on=None, left_on='Country/Region', right_on='name', sort=False,
                               suffixes=('_x', '_y'), copy=False, indicator=False, validate=None)
            dataset_merged_province = pd.merge(dataset_merged_country, self.new_reference_data['province_state'].iloc[:,[0,3]], how='left', on=None, left_on='Province/State', right_on='name', sort=False,
                               suffixes=('_x', '_y'), copy=False, indicator=False, validate=None)
            # Drop Lat, Long, Province/State, Country/Region
            cases = dataset_merged_province.drop('Country/Region', axis=1).drop("name_x", axis=1).drop("name_y", axis=1).drop("Lat", axis=1).drop("Long", axis=1).drop("Province/State", axis=1)
            # Melt dataframe using date columns as rows
            cases_melt = pd.melt(cases, id_vars=['country_id', 'province_state_id'], value_vars=['1/22/20'])
            # Join all melted time series columns
            for j, column in enumerate(cases.iloc[:,1:-2]):
                melted_df = pd.melt(cases, id_vars=['country_id', 'province_state_id'], value_vars=[column])
                cases_melt = cases_melt.append(melted_df)
            cases_melt.columns = ['country_id', 'province_state_id', 'date', 'count']
            cases_melt['date'] = pd.to_datetime(cases_melt['date'],infer_datetime_format=True)
            cases_melt["country_id"] = pd.to_numeric(cases_melt["country_id"], downcast='integer')
            cases_melt["province_state_id"] = pd.to_numeric(cases_melt["province_state_id"], downcast='integer')
            cases_melt["count"] = pd.to_numeric(cases_melt["count"], downcast='integer')
            cases_melt['case_type'] = i
            full_dataset_cleaned.append(cases_melt)
        self.full_dataset_cleaned_list = full_dataset_cleaned
        full_dataset_cleaned_combined = pd.concat(full_dataset_cleaned, ignore_index=True)
        full_dataset_cleaned_combined['province_state_id'] = full_dataset_cleaned_combined['province_state_id'].astype('Int64')
        full_dataset_cleaned_combined['country_id'] = full_dataset_cleaned_combined['country_id'].astype('Int64')
        full_dataset_cleaned_combined['count'] = full_dataset_cleaned_combined['count'].astype('Int64')
        self.full_dataset_cleaned_combined = full_dataset_cleaned_combined

    def validateData(self, data_type):
        # Validate reference data

        # Compare columns
        location_comparison = df.columns[0:4]==pd.Index(['Province/State', 'Country/Region', 'Lat', 'Long'])
        if not location_comparison.all():
            print("Location columns have changed")

        timeseries_comparison = df.columns[4:]==pd.Index(['Province/State', 'Country/Region', 'Lat', 'Long'])
        if not location_comparison.all():
            print("Location columns have changed")

        # Compare dataframe sizes
        old_size = old_df.size    
        new_size = new_df.size
        if old_size!=new_size:
            print("Data size mismatch: Old: ",  str(old_size), "; New: ", str(new_size))
        
        # Compate dataframe content
        df_diff = pd.concat([old_df,new_df]).drop_duplicates(keep=False)
        if df_diff.empty:
            print("No changes in data detected")

class CovidDatabase:
    ### Initialize ###
    def __init__(self):
        try:
            COVID_DB_ENGINE_CONNECTION = os.getenv('COVID_DB_ENGINE_CONNECTION')
            self.engine = create_engine(COVID_DB_ENGINE_CONNECTION, echo=True)
            self.connection = self.engine.connect()
        except AttributeError:
            raise AttributeError('Could not find database connection environment variable. Please create it using "export COVID_DB_ENGINE_CONNECTION="postgresql+psycopg2://covid_superuser:PASSWORD@localhost:5432/covid".')
        metadata = MetaData()
        # Continent table
        self.metadata = {
            'continent': Table('continent', metadata,
                Column('continent_id', Integer, primary_key=True),
                Column('name', String(50), nullable=True),
            ),
            # Country table
            'country': Table('country', metadata,
                Column('country_id', Integer, primary_key=True),
                Column('name', String(50), nullable=True),
                Column('lat', Numeric, nullable=True),
                Column('lat', Numeric, nullable=True),
                Column('continent_id', Integer, ForeignKey("continent.continent_id"))
            ),
            # Province-state table
            'province_state': Table('province_state', metadata,
                Column('province_state_id', Integer, primary_key=True),
                Column('name', String(50), nullable=True),
                Column('lat', Numeric, nullable=True),
                Column('lat', Numeric, nullable=True),
                Column('country_id', Integer, ForeignKey("country.country_id"))
            ),
            # Type category table
            'type_category': Table('type_category', metadata,
                Column('type_category_id', Integer, primary_key=True),
                Column('name', String(50), nullable=True),
            ),
            # Case table
            'case_timeseries': Table('case_timeseries', metadata,
                Column('case_timeseries_id', Integer, primary_key=True),
                Column('count', Numeric, nullable=True),
                Column('date', TIMESTAMP, nullable=True),
                Column('case_type', Integer, ForeignKey("type_category.type_category_id")),
                Column('country_id', Integer, ForeignKey("country.country_id")),
                Column('province_state_id', Integer, ForeignKey("province_state.province_state_id"))
            )
        }
    def getTable(self, table_name):
        self.connection = self.engine.connect()
        row_list=[]
        with self.connection as con:
            rs = con.execute("SELECT * FROM " + str(table_name))
            for row in rs:
                row_list.append(row)

        row_df = pd.DataFrame(row_list)
        if table_name=='province_state':
            row_df.columns = ['province_state_id', 'name', 'lat', 'long', 'country_id']
        elif table_name=='country':
            row_df.columns = ['country_id', 'name', 'lat', 'long', 'continent_id']
        elif table_name=='continent':
            row_df.columns = ['continent_id', 'name']
        elif table_name=='type_category':
            row_df.columns = ['type_id', 'name']
        else:
            row_df.columns = ['case_timeseries_id','case_type', 'count', 'country_id', 'date', 'province_state_id']
        return(row_df)
    def updateData(self):
        return 0

# dataframe = CovidDataset()

def compareData(database_df, datasource_df):
    return database_df.equals(datasource_df)

if __name__ == '__main__':
    # print(dataframe)
    source_df = CovidDataset().createNewReferenceData()
    cdb = CovidDatabase()
    timeseries = cdb.getTable('country')
    print(timeseries, source_df)
    # url = str(sys.argv[1])
    # data_format = str(sys.argv[2])
    # df = make_dataframe(url, data_format)
    # print(df)def compareData(database_df, datasource_df):