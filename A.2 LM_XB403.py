import requests
import pandas as pd


def fetch_data(url):

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def extract_relevant_data(raw_data):

    # print("Raw data structure:", raw_data)

    if isinstance(raw_data, dict):

        # print("keys in the raw data:", raw_data.keys())

        if 'results' in raw_data:
            return raw_data['results']
        elif 'data' in raw_data:
            return raw_data['data']
        else:
            return []
    elif isinstance(raw_data, list):

        return raw_data
    else:
        return []

def normalize_data(data):

    all_keys = set().union(*(d.keys() for d in data if isinstance(d, dict)))

    normalized_data = []
    for d in data:
        normalized_d = {key: d.get(key, None) for key in all_keys}
        normalized_data.append(normalized_d)

    # print("Normalized data:", normalized_data)

    return normalized_data

def save_to_csv(data, filename):
    normalized_data = normalize_data(data)

    df = pd.DataFrame(normalized_data)
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}")


url = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/2453/Choice Cuts?q=report_date=01/1/2016:12/31/2023"

try:
    raw_data = fetch_data(url)

    data_list = extract_relevant_data(raw_data)

    # print("Extracted data:", data_list)

    if data_list:
        save_to_csv(data_list, 'LM_XB403_Choice_Cuts_2016-2023.csv')
    else:
        print("No data fetched from the API.")

except Exception as e:
    print(e)
