import requests
import pandas as pd

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def print_list_of_dicts(data):
    for item in data:
        print(item)

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}")

url = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

try:
    data_list = fetch_data(url)

    if data_list:
        print_list_of_dicts(data_list)

    if data_list:
        save_to_csv(data_list, 'Beef_Tables_Dict.csv')

except Exception as e:
    print(e)
