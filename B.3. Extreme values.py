# Using some basic descriptive statistics, can you identify the periods with values that seem extreme or abnormal?
#   Yes, I generated tables for each of the 6 series, including:
#   extreme values, when they occurred, and their z-scores relative to the distribution.
#   At a glance, COVID prices for all cuts were extreme (2020-2023)

import pandas as pd
import numpy as np

series_tndrloin_weighted_average = pd.read_csv('series_tndrloin_weighted_average.csv')
series_butt_bnls_weighted_average = pd.read_csv('series_butt_bnls_weighted_average.csv')
series_butt_CC_weighted_average = pd.read_csv('series_butt_CC_weighted_average.csv')

series_tndrloin_total_pounds = pd.read_csv('series_tndrloin_total_pounds.csv')
series_butt_bnls_total_pounds = pd.read_csv('series_butt_bnls_total_pounds.csv')
series_butt_CC_total_pounds = pd.read_csv('series_butt_CC_total_pounds.csv')

series_tndrloin_weighted_average['report_date'] = pd.to_datetime(series_tndrloin_weighted_average['report_date'])
series_butt_bnls_weighted_average['report_date'] = pd.to_datetime(series_butt_bnls_weighted_average['report_date'])
series_butt_CC_weighted_average['report_date'] = pd.to_datetime(series_butt_CC_weighted_average['report_date'])

series_tndrloin_total_pounds['report_date'] = pd.to_datetime(series_tndrloin_total_pounds['report_date'])
series_butt_bnls_total_pounds['report_date'] = pd.to_datetime(series_butt_bnls_total_pounds['report_date'])
series_butt_CC_total_pounds['report_date'] = pd.to_datetime(series_butt_CC_total_pounds['report_date'])

def drop_zeros(df, column):
    return df[df[column] != 0]

series_tndrloin_total_pounds = drop_zeros(series_tndrloin_total_pounds, 'total_pounds')
series_butt_bnls_total_pounds = drop_zeros(series_butt_bnls_total_pounds, 'total_pounds')
series_butt_CC_total_pounds = drop_zeros(series_butt_CC_total_pounds, 'total_pounds')

series_tndrloin_weighted_average = drop_zeros(series_tndrloin_weighted_average, 'weighted_average')
series_butt_bnls_weighted_average = drop_zeros(series_butt_bnls_weighted_average, 'weighted_average')
series_butt_CC_weighted_average = drop_zeros(series_butt_CC_weighted_average, 'weighted_average')

combined_pounds_df = series_tndrloin_total_pounds.merge(series_butt_bnls_total_pounds, on='report_date', suffixes=('_tndrloin', '_butt_bnls'))
combined_pounds_df = combined_pounds_df.merge(series_butt_CC_total_pounds, on='report_date', suffixes=('', '_butt_CC'))

combined_pounds_df.rename(columns={
    'total_pounds': 'total_pounds_butt_CC',
    'total_pounds_tndrloin': 'total_pounds_tndrloin',
    'total_pounds_butt_bnls': 'total_pounds_butt_bnls',
}, inplace=True)

combined_weighted_df = series_tndrloin_weighted_average.merge(series_butt_bnls_weighted_average, on='report_date', suffixes=('_tndrloin', '_butt_bnls'))
combined_weighted_df = combined_weighted_df.merge(series_butt_CC_weighted_average, on='report_date', suffixes=('', '_butt_CC'))

combined_weighted_df.rename(columns={
    'weighted_average': 'weighted_average_butt_CC',
    'weighted_average_tndrloin': 'weighted_average_tndrloin',
    'weighted_average_butt_bnls': 'weighted_average_butt_bnls',
}, inplace=True)

def identify_extreme_values(df, column):
    mean_val = df[column].mean()
    std_val = df[column].std()
    df['z_score'] = (df[column] - mean_val) / std_val
    extreme_values = df[(df['z_score'] > 2) | (df['z_score'] < -2)]
    return extreme_values

extreme_tndrloin_pounds = identify_extreme_values(combined_pounds_df, 'total_pounds_tndrloin')
extreme_butt_bnls_pounds = identify_extreme_values(combined_pounds_df, 'total_pounds_butt_bnls')
extreme_butt_CC_pounds = identify_extreme_values(combined_pounds_df, 'total_pounds_butt_CC')

extreme_tndrloin_weighted = identify_extreme_values(combined_weighted_df, 'weighted_average_tndrloin')
extreme_butt_bnls_weighted = identify_extreme_values(combined_weighted_df, 'weighted_average_butt_bnls')
extreme_butt_CC_weighted = identify_extreme_values(combined_weighted_df, 'weighted_average_butt_CC')

print("Extreme values for Tenderloin (Total Pounds):")
print(extreme_tndrloin_pounds[['report_date', 'total_pounds_tndrloin', 'z_score']])

print("\nExtreme values for Top Sirloin Boneless (Total Pounds):")
print(extreme_butt_bnls_pounds[['report_date', 'total_pounds_butt_bnls', 'z_score']])

print("\nExtreme values for Top Sirloin Cap-Off (Total Pounds):")
print(extreme_butt_CC_pounds[['report_date', 'total_pounds_butt_CC', 'z_score']])

print("Extreme values for Tenderloin (Weighted Average):")
print(extreme_tndrloin_weighted[['report_date', 'weighted_average_tndrloin', 'z_score']])

print("\nExtreme values for Top Sirloin Boneless (Weighted Average):")
print(extreme_butt_bnls_weighted[['report_date', 'weighted_average_butt_bnls', 'z_score']])

print("\nExtreme values for Top Sirloin Cap-Off (Weighted Average):")
print(extreme_butt_CC_weighted[['report_date', 'weighted_average_butt_CC', 'z_score']])

extreme_tndrloin_pounds[['report_date', 'total_pounds_tndrloin', 'z_score']].to_csv('extreme_tndrloin_pounds.csv', index=False)
extreme_butt_bnls_pounds[['report_date', 'total_pounds_butt_bnls', 'z_score']].to_csv('extreme_butt_bnls_pounds.csv', index=False)
extreme_butt_CC_pounds[['report_date', 'total_pounds_butt_CC', 'z_score']].to_csv('extreme_butt_CC_pounds.csv', index=False)

extreme_tndrloin_weighted[['report_date', 'weighted_average_tndrloin', 'z_score']].to_csv('extreme_tndrloin_weighted.csv', index=False)
extreme_butt_bnls_weighted[['report_date', 'weighted_average_butt_bnls', 'z_score']].to_csv('extreme_butt_bnls_weighted.csv', index=False)
extreme_butt_CC_weighted[['report_date', 'weighted_average_butt_CC', 'z_score']].to_csv('extreme_butt_CC_weighted.csv', index=False)



