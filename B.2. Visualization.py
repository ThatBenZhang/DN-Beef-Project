# Are there periods of extreme values?
#   Yes, Q4 2019, Q1-2 2020, Q2-3 2021
# Outside of those periods, is there any visible seasonality?
#   Yes, tenderloin prices peaks in Q3-4, butt cuts in the summer
# Does the distribution of values have “long tails”? What does that mean?
#   Yes, a right skew is clearly visible, implying existence of extreme values or outliers in the data, high price
#   volatility. This can come from seasonal demand spikes, supply chain disruptions, changing economic conditions.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the pre-filtered CSV files
series_tndrloin_total_pounds = pd.read_csv('filled_series_tndrloin_total_pounds_2017-2023.csv')
series_butt_bnls_total_pounds = pd.read_csv('filled_series_butt_bnls_total_pounds_2017-2023.csv')
series_butt_CC_total_pounds = pd.read_csv('filled_series_butt_CC_total_pounds_2017-2023.csv')

series_tndrloin_weighted_average = pd.read_csv('filled_series_tndrloin_weighted_average_2017-2023.csv')
series_butt_bnls_weighted_average = pd.read_csv('filled_series_butt_bnls_weighted_average_2017-2023.csv')
series_butt_CC_weighted_average = pd.read_csv('filled_series_butt_CC_weighted_average_2017-2023.csv')

def clean_date(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    return df.dropna(subset=[date_column])

# Clean the date columns
series_tndrloin_total_pounds = clean_date(series_tndrloin_total_pounds, 'report_date')
series_butt_bnls_total_pounds = clean_date(series_butt_bnls_total_pounds, 'report_date')
series_butt_CC_total_pounds = clean_date(series_butt_CC_total_pounds, 'report_date')

series_tndrloin_weighted_average = clean_date(series_tndrloin_weighted_average, 'report_date')
series_butt_bnls_weighted_average = clean_date(series_butt_bnls_weighted_average, 'report_date')
series_butt_CC_weighted_average = clean_date(series_butt_CC_weighted_average, 'report_date')

def drop_zeros(df, column):
    return df[df[column] != 0]

series_tndrloin_total_pounds = drop_zeros(series_tndrloin_total_pounds, 'total_pounds')
series_butt_bnls_total_pounds = drop_zeros(series_butt_bnls_total_pounds, 'total_pounds')
series_butt_CC_total_pounds = drop_zeros(series_butt_CC_total_pounds, 'total_pounds')

series_tndrloin_weighted_average = drop_zeros(series_tndrloin_weighted_average, 'weighted_average')
series_butt_bnls_weighted_average = drop_zeros(series_butt_bnls_weighted_average, 'weighted_average')
series_butt_CC_weighted_average = drop_zeros(series_butt_CC_weighted_average, 'weighted_average')

def plot_and_save_data(df, x_column, y_column, title, filename):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=x_column, y=y_column)
    plt.title(title)
    plt.savefig(filename)
    plt.show()

# Plot and save the cleaned datasets
plot_and_save_data(series_tndrloin_total_pounds, 'report_date', 'total_pounds', 'Tndrloin Total Pounds', 'tndrloin_total_pounds_plot.png')
plot_and_save_data(series_butt_bnls_total_pounds, 'report_date', 'total_pounds', 'Butt Bnls Total Pounds', 'butt_bnls_total_pounds_plot.png')
plot_and_save_data(series_butt_CC_total_pounds, 'report_date', 'total_pounds', 'Butt CC Total Pounds', 'butt_CC_total_pounds_plot.png')

plot_and_save_data(series_tndrloin_weighted_average, 'report_date', 'weighted_average', 'Tndrloin Weighted Average', 'tndrloin_weighted_average_plot.png')
plot_and_save_data(series_butt_bnls_weighted_average, 'report_date', 'weighted_average', 'Butt Bnls Weighted Average', 'butt_bnls_weighted_average_plot.png')
plot_and_save_data(series_butt_CC_weighted_average, 'report_date', 'weighted_average', 'Butt CC Weighted Average', 'butt_CC_weighted_average_plot.png')

plt.figure(figsize=(12, 6))

plt.plot(series_tndrloin_total_pounds['report_date'], series_tndrloin_total_pounds['total_pounds'], label='Tndrloin Total Pounds', linewidth=0.7)
plt.plot(series_butt_bnls_total_pounds['report_date'], series_butt_bnls_total_pounds['total_pounds'], label='Butt Bnls Total Pounds', linewidth=0.7)
plt.plot(series_butt_CC_total_pounds['report_date'], series_butt_CC_total_pounds['total_pounds'], label='Butt CC Total Pounds', linewidth=0.7)

plt.xlabel('Report Date')
plt.ylabel('Total Pounds')
plt.title('Total Pounds Over Time')
plt.legend()
plt.savefig('total_pounds_over_time.png')
plt.show()

plt.figure(figsize=(12, 6))

plt.plot(series_tndrloin_weighted_average['report_date'], series_tndrloin_weighted_average['weighted_average'], label='Tndrloin Weighted Average', linewidth=0.7)
plt.plot(series_butt_bnls_weighted_average['report_date'], series_butt_bnls_weighted_average['weighted_average'], label='Butt Bnls Weighted Average', linewidth=0.7)
plt.plot(series_butt_CC_weighted_average['report_date'], series_butt_CC_weighted_average['weighted_average'], label='Butt CC Weighted Average', linewidth=0.7)

plt.xlabel('Report Date')
plt.ylabel('Weighted Average')
plt.title('Weighted Average Over Time')
plt.legend()
plt.savefig('weighted_average_over_time.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(series_tndrloin_weighted_average['weighted_average'], kde=True)
plt.title('Histogram of Tndrloin Weighted Average Prices')
plt.xlabel('Weighted Average Price')
plt.ylabel('Frequency')
plt.legend()
plt.savefig('tndrloin_histogram.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=series_tndrloin_weighted_average['weighted_average'])
plt.title('Box Plot of Tndrloin Weighted Average Prices')
plt.xlabel('Weighted Average Price')
plt.show()

plt.figure(figsize=(10, 6))
sns.kdeplot(series_tndrloin_weighted_average['weighted_average'], shade=True)
plt.title('Density Plot of Tndrloin Weighted Average Prices')
plt.xlabel('Weighted Average Price')
plt.ylabel('Density')
plt.legend()
plt.savefig('tndrloin_density.png')
plt.show()

