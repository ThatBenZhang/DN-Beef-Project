#  Describe the meaning of these values.
#   largest positive correlation is between butt bnls and butt_CC prices (.86)
#   largest negative correlation is between butt CC prices and volume (-.22)
#   negative own price/volume correlation (-.09) tenderloin, (-.19) butt_bnls, (-.22) butt CC
#  Discuss causality and whether you have any hypotheses for significance.
#   The weakening of own price/volume correlation of these cuts speaks to the likely price and income inelastic nature
#   of its consumer bases. When the least expensive cut of beef (butt CC) increases in price, more premium cuts
#   naturally increases in sync, this weakens from moderate expensive bnls (.86) to most expensive tenderloin (.7)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

series_tndrloin_total_pounds = pd.read_csv('series_tndrloin_total_pounds.csv')
series_butt_bnls_total_pounds = pd.read_csv('series_butt_bnls_total_pounds.csv')
series_butt_CC_total_pounds = pd.read_csv('series_butt_CC_total_pounds.csv')

series_tndrloin_weighted_average = pd.read_csv('series_tndrloin_weighted_average.csv')
series_butt_bnls_weighted_average = pd.read_csv('series_butt_bnls_weighted_average.csv')
series_butt_CC_weighted_average = pd.read_csv('series_butt_CC_weighted_average.csv')

series_tndrloin_total_pounds['report_date'] = pd.to_datetime(series_tndrloin_total_pounds['report_date'])
series_butt_bnls_total_pounds['report_date'] = pd.to_datetime(series_butt_bnls_total_pounds['report_date'])
series_butt_CC_total_pounds['report_date'] = pd.to_datetime(series_butt_CC_total_pounds['report_date'])

series_tndrloin_weighted_average['report_date'] = pd.to_datetime(series_tndrloin_weighted_average['report_date'])
series_butt_bnls_weighted_average['report_date'] = pd.to_datetime(series_butt_bnls_weighted_average['report_date'])
series_butt_CC_weighted_average['report_date'] = pd.to_datetime(series_butt_CC_weighted_average['report_date'])

def drop_zeros(df, column):
    return df[df[column] != 0]

series_tndrloin_total_pounds = drop_zeros(series_tndrloin_total_pounds, 'total_pounds')
series_butt_bnls_total_pounds = drop_zeros(series_butt_bnls_total_pounds, 'total_pounds')
series_butt_CC_total_pounds = drop_zeros(series_butt_CC_total_pounds, 'total_pounds')

series_tndrloin_weighted_average = drop_zeros(series_tndrloin_weighted_average, 'weighted_average')
series_butt_bnls_weighted_average = drop_zeros(series_butt_bnls_weighted_average, 'weighted_average')
series_butt_CC_weighted_average = drop_zeros(series_butt_CC_weighted_average, 'weighted_average')

combined_df = series_tndrloin_total_pounds.merge(series_butt_bnls_total_pounds, on='report_date', suffixes=('_tndrloin', '_butt_bnls'))

combined_df = combined_df.merge(series_butt_CC_total_pounds, on='report_date', suffixes=('', '_butt_CC'))

combined_df = combined_df.merge(series_tndrloin_weighted_average, on='report_date', suffixes=('', '_tndrloin_weighted'))

combined_df = combined_df.merge(series_butt_bnls_weighted_average, on='report_date', suffixes=('', '_butt_bnls_weighted'))

combined_df = combined_df.merge(series_butt_CC_weighted_average, on='report_date', suffixes=('', '_butt_CC_weighted'))

combined_df.rename(columns={
    'total_pounds': 'total_pounds_butt_CC',
    'weighted_average': 'weighted_average_tndrloin',
    'total_pounds_tndrloin': 'total_pounds_tndrloin',
    'total_pounds_butt_bnls': 'total_pounds_butt_bnls',
    'weighted_average_tndrloin_weighted': 'weighted_average_tndrloin',
    'weighted_average_butt_bnls_weighted': 'weighted_average_butt_bnls',
    'weighted_average_butt_CC_weighted': 'weighted_average_butt_CC'
}, inplace=True)

# print("Final columns:", combined_df.columns)

selected_columns = [
    'total_pounds_tndrloin', 'total_pounds_butt_bnls', 'total_pounds_butt_CC',
    'weighted_average_tndrloin', 'weighted_average_butt_bnls', 'weighted_average_butt_CC'
]
correlation_df = combined_df[selected_columns]

correlation_matrix = correlation_df.corr()

print(correlation_matrix)

correlation_matrix.to_csv('correlation_matrix.csv')

def scatter_plot_with_trendline(x, y, xlabel, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y)
    sns.regplot(x=x, y=y, scatter=False, color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.show()

scatter_plot_with_trendline(combined_df['total_pounds_tndrloin'], combined_df['weighted_average_tndrloin'],
                            'Total Pounds (Tenderloin)', 'Weighted Average Price (Tenderloin)',
                            'Tenderloin Price vs. Volume', 'tenderloin_price_vs_volume.png')

scatter_plot_with_trendline(combined_df['total_pounds_butt_bnls'], combined_df['weighted_average_butt_bnls'],
                            'Total Pounds (Top Sirloin Boneless)', 'Weighted Average Price (Top Sirloin Boneless)',
                            'Top Sirloin Boneless Price vs. Volume', 'top_sirloin_boneless_price_vs_volume.png')

scatter_plot_with_trendline(combined_df['total_pounds_butt_CC'], combined_df['weighted_average_butt_CC'],
                            'Total Pounds (Top Sirloin Cap-Off)', 'Weighted Average Price (Top Sirloin Cap-Off)',
                            'Top Sirloin Cap-Off Price vs. Volume', 'top_sirloin_cap_off_price_vs_volume.png')

def scatter_plot_with_trendline(x, y, xlabel, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y)
    sns.regplot(x=x, y=y, scatter=False, color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.show()

scatter_plot_with_trendline(combined_df['weighted_average_tndrloin'], combined_df['weighted_average_butt_bnls'],
                            'Weighted Average Price (Tenderloin)', 'Weighted Average Price (Top Sirloin Boneless)',
                            'Tenderloin vs. Top Sirloin Boneless Price', 'tenderloin_vs_top_sirloin_boneless_price.png')

scatter_plot_with_trendline(combined_df['weighted_average_tndrloin'], combined_df['weighted_average_butt_CC'],
                            'Weighted Average Price (Tenderloin)', 'Weighted Average Price (Top Sirloin Cap-Off)',
                            'Tenderloin vs. Top Sirloin Cap-Off Price', 'tenderloin_vs_top_sirloin_cap_off_price.png')

scatter_plot_with_trendline(combined_df['weighted_average_butt_bnls'], combined_df['weighted_average_butt_CC'],
                            'Weighted Average Price (Top Sirloin Boneless)', 'Weighted Average Price (Top Sirloin Cap-Off)',
                            'Top Sirloin Boneless vs. Top Sirloin Cap-Off Price', 'top_sirloin_boneless_vs_top_sirloin_cap_off_price.png')