import csv
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import sys


url_test = "https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide"
url_test_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

url_csv_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
url_csv_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
url_csv_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

sources = {
    "confirmed": {
        "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
        "local_path": "data/cases_confirmed.csv"
    },
    "recovered": {
        "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv",
        "local_path": "data/cases_recovered.csv"    
    },
    "deaths": {
        "url": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
        "local_path": "data/cases_deaths.csv"
    },
}

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

def getData(url):
    """Input url of csv, returns dataframe"""
    df = pd.read_csv(url)
    return df

def makeReferenceData():
    continents = ["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America", "None"]
    continents_df = pd.DataFrame(continents)
    return continents_df

def prepData(data_type):
    df = pd.read_csv(sources[data_type]['url'])

def checkDataChange(data_type):
    old_data = pd.read_csv(sources[data_type]['local_path'])
    old_size = old_data.size
    
    new_data = pd.read_csv(sources[data_type]['url'])
    new_size = new_data.size
    if old_size!=new_size:
        print("Data size mismatch: Old: ",  str(old_size), "; New: ", str(new_size))


if __name__ == '__main__':
    url = str(sys.argv[1])
    data_format = str(sys.argv[2])
    df = make_dataframe(url, data_format)
    print(df)