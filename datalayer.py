""""
This module contains functionality for downloading and processing covid-19 data originating from SSI (Statens Serum Institut).
"""

from io import StringIO
import pandas as pd
import requests

def get_csv_data(url, backup_file_path=None):
    """Downloads a CSV file from the given URL and returns it as a pandas DataFrame.
    If the download fails, the function will try to load the data from a backup file."""
    response = requests.get(url, timeout=(1, 2))

    if response.status_code == 200:
        data = StringIO(response.text)
        return pd.read_csv(data, delimiter=';')

    print("Failed to download CSV file. Status code:", response.status_code)
    if backup_file_path is None:
        print("No backup file path provided.")
        return pd.DataFrame()

    return pd.read_csv(backup_file_path, delimiter=';')

def get_confirmed_admitted_deceased_per_day_per_sex():
    """Returns a DataFrame containing the number of confirmed cases, admitted patients and deceased patients per day"""
    return get_csv_data("https://steenhulthin.github.io/infectious-diseases-data/03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv",
                        r'./data/03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv')



COLOR_TESTED = "limegreen"
COLOR_POSITIVE = "teal"
COLOR_ADMITTED = "orangered"
COLOR_DEAD = "crimson"

EMOJI_TESTED = "🧪"
EMOJI_POSITIVE = "🦠"
EMOJI_ADMITTED = "🛌"
EMOJI_DEAD = "💀"
