# Question 1: Is the resulting model better than fitting a constant?
#   Yes
# Question 2: Are all regressors significant? Does the answer contradict Question 1?
#   Yes they are. The full model has significantly more explanatory power, lower AIC and BIC and is well-conditioned.
#   It is better than fitting a constant.
# Exercise: Drop one of the regressors and fit again.
#   done
# Question 3: Has the goodness of fit improved, deteriorated, or stayed approximately unchanged?
#   Goodness of fit stayed approximately unchanged, adjusted R-squared fell only slightly, suggesting the two butt cuts
#   contribute very similar information in terms of explaining variation in tenderloin prices.
# Question 4: Are all regressors more or less significant than before? Hint: check how the condition number has changed.
#   All regressor are similarly significant, full model standard errors are roughly double the partial, the condition
#   number (overfittedness) improved for the partial number (down from 3.7 to 1)
# Question 5: Are there any known deficiencies with the prior model with respect to bias or efficiency with this model?
#   Autocorrelation - consider adding lagged variables or using time series-specific models (ARIMA, SARIMA) to account for autocorrelation.
#   Multicollinearity - check VIF for the covariates. If multicollinearity is present, maybe combining correlated variables or using regularization techniques (ridge or lasso regression).
#   Improving model fit - look for additional relevant covariates or interactions between variables that might improve the model fit.
#   Residual Analysis - investigate the residuals to identify any patterns or structure that the model has not captured.

import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
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

# def drop_zeros(df, column):
#     return df[df[column] != 0]
#
# series_tndrloin_total_pounds = drop_zeros(series_tndrloin_total_pounds, 'total_pounds')
# series_butt_bnls_total_pounds = drop_zeros(series_butt_bnls_total_pounds, 'total_pounds')
# series_butt_CC_total_pounds = drop_zeros(series_butt_CC_total_pounds, 'total_pounds')
#
# series_tndrloin_weighted_average = drop_zeros(series_tndrloin_weighted_average, 'weighted_average')
# series_butt_bnls_weighted_average = drop_zeros(series_butt_bnls_weighted_average, 'weighted_average')
# series_butt_CC_weighted_average = drop_zeros(series_butt_CC_weighted_average, 'weighted_average')

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

columns_to_standardize = [
    'total_pounds_tndrloin', 'total_pounds_butt_bnls', 'total_pounds_butt_CC',
    'weighted_average_tndrloin', 'weighted_average_butt_bnls', 'weighted_average_butt_CC'
]

combined_df.replace([np.inf, -np.inf], np.nan, inplace=True)
combined_df.dropna(inplace=True)

for column in columns_to_standardize:
    mean_val = combined_df[column].mean()
    std_val = combined_df[column].std()
    combined_df[f'{column}_scaled'] = (combined_df[column] - mean_val) / std_val

combined_df.to_csv('combined_scaled_df.csv', index=False)

# print(combined_df.isnull().sum())
# print(np.isinf(combined_df).sum())

y = combined_df['weighted_average_tndrloin_scaled']

X = combined_df[['weighted_average_butt_bnls_scaled', 'weighted_average_butt_CC_scaled']]
X = sm.add_constant(X)

full_model = sm.OLS(y, X).fit()

robust_model = full_model.get_robustcov_results(cov_type='HC3')

intercept_only_model = sm.OLS(y, sm.add_constant(np.ones(len(y)))).fit()

print("Full Model Summary:")
print(full_model.summary())
# print(robust_model.summary())
print("\nConstant-Only Model Summary:")
print(intercept_only_model.summary())

y = combined_df['weighted_average_tndrloin_scaled']

X = combined_df[['weighted_average_butt_bnls_scaled']]
X = sm.add_constant(X)

partial_model = sm.OLS(y, X).fit()
robust_partial_model = partial_model.get_robustcov_results(cov_type='HC3')

print("\nPartial Model Summary:")
print(partial_model.summary())
# print(robust_partial_model.summary())

print("\nComparison:")
print(f"Full Model R-squared: {full_model.rsquared}")
# print(f"Robust Full Model R-squared: {robust_model.rsquared}")
print(f"Partial Model R-squared: {partial_model.rsquared}")
print(f"Intercept-Only Model R-squared: {intercept_only_model.rsquared}")
print(f"Full Model F-statistic: {full_model.fvalue}")
# print(f"Robust Model F-statistic: {robust_model.fvalue}")
print(f"Partial Model F-statistic: {partial_model.fvalue}")
print(f"Full Model p-value: {full_model.f_pvalue}")
# print(f"Robust Model p-value: {robust_model.f_pvalue}")
print(f"Partial Model p-value: {partial_model.f_pvalue}")

if full_model.f_pvalue < 0.05:
    print("The full model is significantly better than the intercept-only model.")
else:
    print("The full model is not significantly better than the intercept-only model.")

full_model = sm.OLS(y, X).fit()

fitted_values = full_model.predict(X)

plt.figure(figsize=(10, 6))
plt.scatter(y, fitted_values, alpha=0.5, label='Actual Values')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Fitted OLS Values')
plt.title('Fitted OLS Values vs Actual Values')
plt.savefig('Fitted OLS Values vs Actual Values')
plt.legend()
plt.show()

condition_number = np.linalg.cond(X)
print(f'\nCondition Number: {condition_number}')

print(f"\nAIC - Full Model: {full_model.aic}, Constant-Only Model: {intercept_only_model.aic}")
print(f"BIC - Full Model: {full_model.bic}, Constant-Only Model: {intercept_only_model.bic}")

rse = np.sqrt(full_model.mse_resid)
print(f"Full model Residual Standard Error (RSE): {rse}")
rse_partial = np.sqrt(partial_model.mse_resid)
print(f"Partial model Residual Standard Error (RSE): {rse_partial}")