import pandas as pd

filename = 'LM_XB403_Choice_Cuts_2016-2023.csv'

df = pd.read_csv(filename, low_memory=False)

# print("\nColumn Names:")
# print(df.columns)

columns_to_keep = ['total_pounds', 'weighted_average', 'report_date', 'item_description']
df = df[columns_to_keep]

df['total_pounds'] = df['total_pounds'].str.replace(',', '')
df['weighted_average'] = df['weighted_average'].str.replace(',', '')

df['report_date'] = pd.to_datetime(df['report_date'], errors='coerce').dt.strftime('%Y-%m-%d')

rename_mapping = {
    'Loin, tndrloin, trmd, heavy (189A  4)': 'tndrloin',
    'Loin, top butt, bnls, heavy (184  1)': 'butt_bnls',
    'Loin, top butt, CC (184B  3)': 'butt_CC'
}

filtered_df = df[df['item_description'].isin(rename_mapping.keys())].copy()
filtered_df['item_description'] = filtered_df['item_description'].map(rename_mapping)


series_tndrloin_total_pounds = filtered_df[filtered_df['item_description'] == 'tndrloin'][['report_date', 'total_pounds']]
series_butt_bnls_total_pounds = filtered_df[filtered_df['item_description'] == 'butt_bnls'][['report_date', 'total_pounds']]
series_butt_CC_total_pounds = filtered_df[filtered_df['item_description'] == 'butt_CC'][['report_date', 'total_pounds']]

series_tndrloin_weighted_average = filtered_df[filtered_df['item_description'] == 'tndrloin'][['report_date', 'weighted_average']]
series_butt_bnls_weighted_average = filtered_df[filtered_df['item_description'] == 'butt_bnls'][['report_date', 'weighted_average']]
series_butt_CC_weighted_average = filtered_df[filtered_df['item_description'] == 'butt_CC'][['report_date', 'weighted_average']]

# Print the series
print("\nSeries - tndrloin and total_pounds:")
print(series_tndrloin_total_pounds)

print("\nSeries - butt_bnls and total_pounds:")
print(series_butt_bnls_total_pounds)

print("\nSeries - butt_CC and total_pounds:")
print(series_butt_CC_total_pounds)

print("\nSeries - tndrloin and weighted_average:")
print(series_tndrloin_weighted_average)

print("\nSeries - butt_bnls and weighted_average:")
print(series_butt_bnls_weighted_average)

print("\nSeries - butt_CC and weighted_average:")
print(series_butt_CC_weighted_average)

series_tndrloin_total_pounds.to_csv('series_tndrloin_total_pounds.csv', index=False)
series_butt_bnls_total_pounds.to_csv('series_butt_bnls_total_pounds.csv', index=False)
series_butt_CC_total_pounds.to_csv('series_butt_CC_total_pounds.csv', index=False)

series_tndrloin_weighted_average.to_csv('series_tndrloin_weighted_average.csv', index=False)
series_butt_bnls_weighted_average.to_csv('series_butt_bnls_weighted_average.csv', index=False)
series_butt_CC_weighted_average.to_csv('series_butt_CC_weighted_average.csv', index=False)

# butt cc missing dates
# butt bnls many missing values

