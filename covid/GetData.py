import csv
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import sys


url_test = "https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide"
url_test_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
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