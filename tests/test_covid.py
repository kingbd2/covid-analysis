from covid import __version__
from covid import GetData.CovidDataset

def test_version():
    assert __version__ == '0.1.0'

url_csv_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

def test_url():
    df = GetData.getData(url_csv_confirmed)
    assert not df.empty
