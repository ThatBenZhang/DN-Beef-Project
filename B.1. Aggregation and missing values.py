# I choose to aggregate weekly (year_week) using sum for 'total_pounds' and mean of 'weighted average'.
# This methods works well for tenderloin as the data is well populated.
# However, it works less well for butt_CC and even worse for butt_bnls as they both have significant missing data.
# Missing values during the beginning of COVID
# Fowards/backwards fill could be used to fill in some smaller segments of missing data, interpolation can also be used
# when linearity can be reasonably assumed. Rolling mean can smooth out short-term fluctuations, discarding larger gaps
# should be considered as they won't be as reliably filled by appropriate methods.

import pandas as pd

series_tndrloin_total_pounds = pd.read_csv('series_tndrloin_total_pounds.csv')
series_butt_bnls_total_pounds = pd.read_csv('series_butt_bnls_total_pounds.csv')
series_butt_CC_total_pounds = pd.read_csv('series_butt_CC_total_pounds.csv')

series_tndrloin_weighted_average = pd.read_csv('series_tndrloin_weighted_average.csv')
series_butt_bnls_weighted_average = pd.read_csv('series_butt_bnls_weighted_average.csv')
series_butt_CC_weighted_average = pd.read_csv('series_butt_CC_weighted_average.csv')

# series_tndrloin_total_pounds['total_pounds'] = pd.to_numeric(series_tndrloin_total_pounds['total_pounds'], errors='coerce')
# series_butt_bnls_total_pounds['total_pounds'] = pd.to_numeric(series_butt_bnls_total_pounds['total_pounds'], errors='coerce')
# series_butt_CC_total_pounds['total_pounds'] = pd.to_numeric(series_butt_CC_total_pounds['total_pounds'], errors='coerce')

# series_tndrloin_weighted_average['weighted_average'] = pd.to_numeric(series_tndrloin_weighted_average['weighted_average'], errors='coerce')
# series_butt_bnls_weighted_average['weighted_average'] = pd.to_numeric(series_butt_bnls_weighted_average['weighted_average'], errors='coerce')
# series_butt_CC_weighted_average['weighted_average'] = pd.to_numeric(series_butt_CC_weighted_average['weighted_average'], errors='coerce')

series_tndrloin_total_pounds['report_date'] = pd.to_datetime(series_tndrloin_total_pounds['report_date'])
series_butt_bnls_total_pounds['report_date'] = pd.to_datetime(series_butt_bnls_total_pounds['report_date'])
series_butt_CC_total_pounds['report_date'] = pd.to_datetime(series_butt_CC_total_pounds['report_date'])

series_tndrloin_weighted_average['report_date'] = pd.to_datetime(series_tndrloin_weighted_average['report_date'])
series_butt_bnls_weighted_average['report_date'] = pd.to_datetime(series_butt_bnls_weighted_average['report_date'])
series_butt_CC_weighted_average['report_date'] = pd.to_datetime(series_butt_CC_weighted_average['report_date'])

def get_year_week(df):
    df['year_week'] = df['report_date'].dt.strftime('%Y-%U')
    return df

series_tndrloin_total_pounds = get_year_week(series_tndrloin_total_pounds)
series_butt_bnls_total_pounds = get_year_week(series_butt_bnls_total_pounds)
series_butt_CC_total_pounds = get_year_week(series_butt_CC_total_pounds)

series_tndrloin_weighted_average = get_year_week(series_tndrloin_weighted_average)
series_butt_bnls_weighted_average = get_year_week(series_butt_bnls_weighted_average)
series_butt_CC_weighted_average = get_year_week(series_butt_CC_weighted_average)

weekly_tndrloin_total_pounds = series_tndrloin_total_pounds.groupby('year_week').agg({'total_pounds': 'sum'}).reset_index()
weekly_butt_bnls_total_pounds = series_butt_bnls_total_pounds.groupby('year_week').agg({'total_pounds': 'sum'}).reset_index()
weekly_butt_CC_total_pounds = series_butt_CC_total_pounds.groupby('year_week').agg({'total_pounds': 'sum'}).reset_index()

weekly_tndrloin_weighted_average = series_tndrloin_weighted_average.groupby('year_week').agg({'weighted_average': 'mean'}).reset_index()
weekly_butt_bnls_weighted_average = series_butt_bnls_weighted_average.groupby('year_week').agg({'weighted_average': 'mean'}).reset_index()
weekly_butt_CC_weighted_average = series_butt_CC_weighted_average.groupby('year_week').agg({'weighted_average': 'mean'}).reset_index()

weekly_tndrloin_total_pounds.to_csv('weekly_tndrloin_total_pounds.csv', index=False)
weekly_tndrloin_weighted_average.to_csv('weekly_tndrloin_weighted_average.csv', index=False)
weekly_butt_bnls_total_pounds.to_csv('weekly_butt_bnls_total_pounds.csv', index=False)
weekly_butt_bnls_weighted_average.to_csv('weekly_butt_bnls_weighted_average.csv', index=False)
weekly_butt_CC_total_pounds.to_csv('weekly_butt_CC_total_pounds.csv', index=False)
weekly_butt_CC_weighted_average.to_csv('weekly_butt_CC_weighted_average.csv', index=False)

series_tndrloin_total_pounds = pd.read_csv('series_tndrloin_total_pounds.csv')
series_butt_bnls_total_pounds = pd.read_csv('series_butt_bnls_total_pounds.csv')
series_butt_CC_total_pounds = pd.read_csv('series_butt_CC_total_pounds.csv')

series_tndrloin_weighted_average = pd.read_csv('series_tndrloin_weighted_average.csv')
series_butt_bnls_weighted_average = pd.read_csv('series_butt_bnls_weighted_average.csv')
series_butt_CC_weighted_average = pd.read_csv('series_butt_CC_weighted_average.csv')

start_date = '2017-01-01'
series_tndrloin_total_pounds = series_tndrloin_total_pounds[series_tndrloin_total_pounds['report_date'] >= start_date]
series_butt_bnls_total_pounds = series_butt_bnls_total_pounds[series_butt_bnls_total_pounds['report_date'] >= start_date]
series_butt_CC_total_pounds = series_butt_CC_total_pounds[series_butt_CC_total_pounds['report_date'] >= start_date]

series_tndrloin_weighted_average = series_tndrloin_weighted_average[series_tndrloin_weighted_average['report_date'] >= start_date]
series_butt_bnls_weighted_average = series_butt_bnls_weighted_average[series_butt_bnls_weighted_average['report_date'] >= start_date]
series_butt_CC_weighted_average = series_butt_CC_weighted_average[series_butt_CC_weighted_average['report_date'] >= start_date]

series_tndrloin_total_pounds.to_csv('filtered_series_tndrloin_total_pounds.csv', index=False)
series_butt_bnls_total_pounds.to_csv('filtered_series_butt_bnls_total_pounds.csv', index=False)
series_butt_CC_total_pounds.to_csv('filtered_series_butt_CC_total_pounds.csv', index=False)

series_tndrloin_weighted_average.to_csv('filtered_series_tndrloin_weighted_average.csv', index=False)
series_butt_bnls_weighted_average.to_csv('filtered_series_butt_bnls_weighted_average.csv', index=False)
series_butt_CC_weighted_average.to_csv('filtered_series_butt_CC_weighted_average.csv', index=False)

def fill_missing_data(df, column):
    df[column] = df[column].ffill().bfill()
    return df

series_tndrloin_total_pounds = fill_missing_data(series_tndrloin_total_pounds, 'total_pounds')
series_butt_bnls_total_pounds = fill_missing_data(series_butt_bnls_total_pounds, 'total_pounds')
series_butt_CC_total_pounds = fill_missing_data(series_butt_CC_total_pounds, 'total_pounds')

series_tndrloin_weighted_average = fill_missing_data(series_tndrloin_weighted_average, 'weighted_average')
series_butt_bnls_weighted_average = fill_missing_data(series_butt_bnls_weighted_average, 'weighted_average')
series_butt_CC_weighted_average = fill_missing_data(series_butt_CC_weighted_average, 'weighted_average')

series_tndrloin_total_pounds.to_csv('filled_series_tndrloin_total_pounds_2017-2023.csv', index=False)
series_butt_bnls_total_pounds.to_csv('filled_series_butt_bnls_total_pounds_2017-2023.csv', index=False)
series_butt_CC_total_pounds.to_csv('filled_series_butt_CC_total_pounds_2017-2023.csv', index=False)

series_tndrloin_weighted_average.to_csv('filled_series_tndrloin_weighted_average_2017-2023.csv', index=False)
series_butt_bnls_weighted_average.to_csv('filled_series_butt_bnls_weighted_average_2017-2023.csv', index=False)
series_butt_CC_weighted_average.to_csv('filled_series_butt_CC_weighted_average_2017-2023.csv', index=False)