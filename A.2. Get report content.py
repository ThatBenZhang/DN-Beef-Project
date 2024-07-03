# Exercise: Describe the contents of this report.
# ● What is the business significance?
#
# ● How are these values measured?
#
# ● What are the units?
#
# ● What is the difference between Choice and Select?
#
# Exercise: Find the LM_CT115 report under the Cattle section of the Datamart. Describe the contents of this report, including the business significance and units of the fields.


questions_LM_XB403 = [
    "Describe the contents of this report, LM_XB403",
    "What is the business significance?",
    "How are these values measured?",
    "What are the units?",
    "What is the difference between Choice and Select?"
]

answers_LM_XB403 = {
    "Describe the contents of this report, LM_XB403": "The USDA's 'National Daily Boxed Beef Cutout & Boxed Beef Cuts' report "
                                                      "provides detailed information on the negotiated sales of boxed beef "
                                                      "cutouts and individual boxed beef cuts. Key components contain boxed "
                                                      "beef cutout values; load counts; prices; price changes; spreads; and "
                                                      "volumes.",
    "What is the business significance?": "The detailed daily updates on the prices and volumes of various beef cuts "
                                          "facilitates price discovery, establishing market benchmarks for supply and "
                                          "demand sides to negotiate. It also provides supply chain insights, "
                                          "allowing producers, wholesalers, and retailers to manage inventories and "
                                          "forecast demand. The report also contains information on market "
                                          "fundamentals from tracking constantly changing market trends. "
                                          "Additionally, the data helps businesses manage price volatility risks and "
                                          "ensures regulatory compliance. Overall, this report is a valuable tool for "
                                          "making informed decisions and maintaining competitiveness in the beef "
                                          "market.",
    "How are these values measured?": "Data is gathered from actual sales reported daily to the USDA, between meat "
                                      "packers and buyers, including specifics on the type of beef cut, "
                                      "quality grade, negotiated price, and volume sold. The boxed beef cutout value "
                                      "is calculated by taking the weighted average price of individual cuts and "
                                      "multiplying by their yield percentages from a standard carcass, expressed in "
                                      "dollars per hundredweight (cwt). The report also tracks daily price changes "
                                      "and spreads between different grades like Choice and Select, reflecting market "
                                      "trends. ",
    "What are the units?": "The primary units used are dollars per hundredweight (cwt) and pounds, with one cwt "
                           "equaling 100 pounds. The weight of beef cuts is measured in pounds, and the total volume "
                           "of sales is often conveyed in terms of loads, where one load is equivalent to 40,"
                           "000 pounds.",
    "What is the difference between Choice and Select?": "The primary difference between Choice and Select grades of "
                                                         "beef lies in their marbling and tenderness. Choice beef is "
                                                         "known for having moderate marbling, referring to the fat "
                                                         "interspersed within the muscle. This level of marbling "
                                                         "means Choice beef is generally tender, flavorful. Select "
                                                         "beef, has less marbling compared to Choice, resulting in "
                                                         "leaner cuts. It is typically less tender and juicy than "
                                                         "Choice."
}

questions_LM_CT115 = [
    "Describe the contents of this report, LM_CT115",
    "What is the business significance?",
    "How are these values measured?",
    "What are the units?"
]

answers_LM_CT115 = {
    "Describe the contents of this report, LM_CT115": "National Daily Direct Slaughter Cattle - Negotiated Purchases Summary, "
                                                      "provides a summary of daily negotiated cash sales of slaughter cattle. It "
                                                      "includes information on the number of cattle traded, prices, "
                                                      "and weights, segmented by various types and grades of cattle. This "
                                                      "report is essential for market participants to understand current "
                                                      "pricing trends and market conditions in the cattle industry. It is "
                                                      "updated daily.",
    "What is the business significance?": "LM_CT115 includes prices, volumes, and weights, segmented by cattle "
                                          "types and grades. The report helps producers, processors, and traders make "
                                          "informed decisions on buying and selling cattle, understand market trends, "
                                          "and develop pricing strategies. By offering real-time market conditions, "
                                          "the report is useful in risk management and enhances transparency in the "
                                          "cattle market, ensuring fair trading practices.",
    "How are these values measured?": "Values reported comes from data collection via actual negotiated "
                                      "cash sales between cattle producers and buyers. This data includes transaction "
                                      "details such as the number of cattle traded, their weights, and the prices "
                                      "agreed upon. The report segments this information by various types and grades "
                                      "of cattle, reflecting the market's daily activities.",
    "What are the units?": "Values are measured using head count for the number of cattle sold, weight in pounds for "
                           "the cattle, and price per hundredweight (cwt)."
}


def answer_questions_LM_XB403(questions_LM_XB403, answers_LM_XB403):
    results = {}
    for question in questions_LM_XB403:
        answer = answers_LM_XB403.get(question, "Question not found in the answer list")
        results[question] = answer
    return results


# Get the answers
results = answer_questions_LM_XB403(questions_LM_XB403, answers_LM_XB403)


def answer_questions_LM_CT115(questions_LM_CT115, answers_LM_CT115):
    results_LM_CT115 = {}
    for question in questions_LM_CT115:
        answer = answers_LM_CT115.get(question, "Question not found in the answer list")
        results_LM_CT115[question] = answer
    return results_LM_CT115

# Get the answers
results_LM_CT115 = answer_questions_LM_CT115(questions_LM_CT115, answers_LM_CT115)

# Print the answers
for question, answer in results.items():
    print(f"Q: {question}")
    print(f"A: {answer}")
    print()
for question, answer in results_LM_CT115.items():
    print(f"Q: {question}")
    print(f"A: {answer}")
    print()

import requests
import pandas as pd

def fetch_data(url):

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def normalize_data(data):

    data = [d for d in data if isinstance(d, dict)]

    all_keys = set().union(*(d.keys() for d in data))

    normalized_data = []
    for d in data:
        normalized_d = {key: d.get(key, None) for key in all_keys}
        normalized_data.append(normalized_d)

    return normalized_data

def save_to_csv(data, filename):

    normalized_data = normalize_data(data)

    df = pd.DataFrame(normalized_data)
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}")

url = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/2453/Choice%20Cuts?q=report_date=01/1/2016:12/31/2023"

try:

    raw_data = fetch_data(url)

    print("Raw JSON data:", raw_data)

    if 'results' in raw_data:
        data_list = raw_data['results']
    else:
        data_list = []

    print("Extracted data:", data_list)

    if data_list:
        save_to_csv(data_list, 'LM_XB403_data.csv')
    else:
        print("No data fetched from the API.")

except Exception as e:
    print(e)
