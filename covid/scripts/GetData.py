import csv
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import sys
import math
from datetime import date

class CovidDataset:
    def __init__(self):
        self.sources = {
            "confirmed": {
                "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
                "local_path": "data/timeseries/cases_confirmed.csv"
            },
            "recovered": {
                "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
                "local_path": "data/timeseries/cases_confirmed.csv"    
            },
            "deaths": {
                "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
                "local_path": "data/timeseries/cases_confirmed.csv"
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

        self.old_reference_data = self.loadOldReferenceData()
        self.needs_reference_data_refresh = False
        self.needs_timeseries_data_refresh = False


    def getNewData(self, data_type):
        """Input url of csv, returns dataframe"""
        df = pd.read_csv(self.sources[str(data_type)]['url'])
        return df

    def getOldData(self, data_type):
        """Input filepath of csv, returns dataframe"""
        df = pd.read_csv(self.sources[str(data_type)]['local_path'])
        return df

    def createNewReferenceData(self):
        # Continents reference data
        continents = ["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America", "None"]
        continents_df = pd.DataFrame(continents)
        # Types reference data
        types_df = pd.DataFrame(["Confirmed", "Recovered", "Deaths"])
        # Province/State reference data
        prov_state_list = []
        for dataset in self.full_dataset_raw:
            prov_state = pd.DataFrame(dataset['new'].iloc[:, 0:2].drop_duplicates(keep='first').dropna().reset_index().drop(["index"],axis=1))
            prov_state_list.append(prov_state)
        dfps = pd.concat([prov_state_list[0], prov_state_list[1], prov_state_list[2]], ignore_index=True)
        province_state_df = dfps.drop_duplicates(keep='first')
        # province_state_df.iloc[0,0] = "None"
        # Countries-continents reference data
        base_path = "data/reference/"
        countries_continents_path = base_path + "countries_continents.csv"
        countries_continents_df=pd.read_csv(countries_continents_path, index_col=0)
        # Country reference data
        base_path = "data/reference/"
        country_path = base_path + "country.csv"
        country_df=pd.read_csv(country_path, index_col=0)
        # Combine all reference data into a list
        reference_data_list = [continents_df, country_df, province_state_df, countries_continents_df, types_df]
        return reference_data_list
    
    def loadOldReferenceData(self):
        base_path = "data/reference/"
        continent_path = base_path + "continent.csv"
        country_path = base_path + "country.csv"
        province_state_path = base_path + "province_state.csv"
        countries_continents_path = base_path + "countries_continents.csv"
        types_path = base_path + "types.csv"
        reference_data_paths = [continent_path, country_path, province_state_path, countries_continents_path, types_path]
        reference_data_list = []
        for path in reference_data_paths:
            df = pd.read_csv(path, index_col=0)
            reference_data_list.append(df)
        return reference_data_list

    def standardizeNewData(self):
        full_dataset_cleaned = []
        for i, dataset in enumerate(self.full_dataset_raw):
            countries = dataset['new'].iloc[:,:4]
            timeseries = dataset['new'].iloc[:,4:]
#             print(i)
            # Create list of region codes present in the dataset and add column
            region_codes = []
            prov_state = countries.iloc[:, 0].drop_duplicates(keep='first').reset_index().drop(["index"],axis=1)
            for region in countries.iloc[:,0]:
                if isinstance(region, str):
                    pass
                elif np.isnan(region):
                    region_codes.append(0)
                    continue
                for i, item in enumerate(prov_state.iloc[:,0]):
                    if item == region:
                        region_codes.append(i)
            countries["region_codes"] = region_codes

            # Create list of continent codes and add column
            continents = []
            df_countries_continents = pd.read_csv("data/reference/countries_continents.csv", index_col=0)
            for item in countries.iloc[:,1]:
                old_size = len(continents)
                for country in df_countries_continents.iterrows():
                    if item==country[1][1]:
                        continents.append(country[1][0])
            
                new_size = len(continents)
                if old_size==new_size:
                    continents.append("NA")
            for i, line in enumerate(countries.iterrows()):
                if line[1][-1]=="NA":
                    print(line)
            countries["continent"] = continents
            
            continent_codes = []
            continents_df = pd.read_csv("data/reference/continent.csv", index_col=0)
            for continent in countries.iloc[:,-1]:
                if isinstance(continent, str):
                    pass
                elif np.isnan(continent):
                    print("Not a continent")
                for i, item in enumerate(continents_df.iloc[:,0]):
                    if item == continent:
                        continent_codes.append(i)
            countries["continent_codes"] = continent_codes

            # Create and append list of country codes
            country_codes = []
            country_df = pd.read_csv("data/reference/country.csv", index_col=0)
            for case in countries.iloc[:,1]:
                for i, item in enumerate(country_df.iloc[:,0]):
                    if item == case:
                        country_codes.append(i)
            countries['country_code'] = country_codes
            
            # Concatenate country and timeseries dataframes       
            cases = countries.drop('Country/Region', axis=1).drop("continent", axis=1).drop("Lat", axis=1).drop("Long", axis=1).drop("Province/State", axis=1)
            cases_full = pd.concat([cases, timeseries], axis=1)
            cases_full_melt = pd.melt(cases_full, id_vars=['region_codes', 'continent_codes', 'country_code'], value_vars=['1/22/20'])
            
            # Join all melted time series columns
            for i, column in enumerate(cases_full.iloc[:,4:]):
                melted_df = pd.melt(cases_full, id_vars=['region_codes', 'continent_codes', 'country_code'], value_vars=[column])
                cases_full_melt = cases_full_melt.append(melted_df)
            cases_full_melt['variable'] = pd.to_datetime(cases_full_melt['variable'],infer_datetime_format=True)
            cases_full_melt.columns = ['region_code', 'continent_code', 'country_code', 'date', 'count']
            cases_full_melt['case_type'] = i
            full_dataset_cleaned.append(cases_full_melt)
        self.full_dataset_cleaned = full_dataset_cleaned
    
    def combineCleansedData(self):
        full_dataset_combined = pd.DataFrame()
        case_types = ["Confirmed", "Recovered", "Deaths"]
        case_types_df = pd.DataFrame(case_types)
        for i, dataset in enumerate(self.full_dataset_cleaned):
            dataset['case_type'] = i
            full_dataset_combined = full_dataset_combined.append(dataset, ignore_index=True)
        self.full_dataset_combined = full_dataset_combined
    
    def saveData(self):
        filenames = ["confirmed", "recovered", "deaths"]
        base_dir_split = "data/timeseries/daily_split/"
        base_dir_combined = "data/timeseries/daily_combined/"
        for i, item in enumerate(self.full_dataset_cleaned):
            filename = base_dir_split + str(date.today()) + str(filenames[i]) + ".csv" 
            item.to_csv(filename)
        filename_combined = base_dir_combined + str(date.today()) + "-combined.csv" 
        self.full_dataset_combined.to_csv(filename_combined)

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
    
    def deduplicate(self, column_name: str):
        item_list = []
        for dataset in self.full_dataset_raw:
            items = pd.DataFrame(dataset['new'][[column_name]].drop_duplicates(keep='first').dropna().reset_index().drop(["index"],axis=1))
            item_list.append(items)
        concatenated_df = pd.concat([item_list[0], item_list[1], item_list[2]], ignore_index=True)
        item_df = concatenated_df.drop_duplicates(keep='first')
        item_ids = list(range(0, len(item_df)))
        id_column_name = column_name + '_id'
        item_df[id_column_name] = item_ids
        return item_df


def make_dataframe(url, data_format="csv"):
    if data_format == "xls":
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        data_attribute = soup.find_all("a", attrs={"data-toggle": "tooltip"})

        for link in data_attribute:
            data_link = link.get('href')

        with requests.Session() as s:
            download = s.get(data_link).content
            dataframe = pd.read_excel(download)
        return dataframe
    else:
        dataframe = pd.read_csv(url)
        return dataframe


if __name__ == '__main__':
    url = str(sys.argv[1])
    data_format = str(sys.argv[2])
    df = make_dataframe(url, data_format)
    print(df)