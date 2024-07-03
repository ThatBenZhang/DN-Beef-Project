# Exercise: Create a seasonality and trend model for tndrloin.
#   done
# Exercise: Describe the pros and cons of your chosen seasonality and one or two alternatives.
#   I chose yearly (52 weeks) for tenderloin and semi-annual (26 weeks) for butt cuts to better capture summer peaks.
#   It captures the distinct seasonal patterns of each series more accurately;  improves the fit and interpretability
#   of the model for butt cuts with different seasonal peaks; potentially improves model performance and forecast accuracy.
#   But this approach adds model complexity, makes direct comparison of seasonal patterns across different cuts more difficult.

#   Another specification is to have yearly seasonality for all cuts, this approach simplifies the analysis and model;
#   fewer parameters to tune; easier alignment of dates. But, it can overlook different seasonal patterns; might underfit
#   seasonal components; loses specificity in variations and trends specific for each cut.
# Question 1: Is the resulting model better than fitting a constant?
#   The full model has more explanatory power but suffers for severe multicollinearity, evident by the large condition
#   number.
# Question 2: Are all regressors significant? Does the answer contradict Question 1?
#   Given the multicollinearity evident in the regressors, not all regressors are statistically significant. In
#   particular, non of the seasonal trends are significant, and the standard errors of all estimates are quite large.
#   One must address these problems before claiming the full seasonal model is better than regressing on the constant.
# Exercise: Drop one or more of the regressors and fit again.
#   done
# Question 1: Has the goodness of fit improved, deteriorated, or stayed approximately unchanged?
#   After dropping seasonal and trend for boneless, the fit of the model stayed approximately unchanged.
# Question 2: Are all regressors more or less significant than before? Hint: check how the condition number has changed.
#   trends are still significant, seasonal components still suffer from strong multicollinearity and are insignificant
#   the conditional number dropped significantly, but still poor.
# Exercise: Create a simple plot of the fit vs actual.
#   done

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

series_tndrloin_weighted_average = pd.read_csv('weekly_tndrloin_weighted_average.csv')
series_butt_bnls_weighted_average = pd.read_csv('weekly_butt_bnls_weighted_average.csv')
series_butt_CC_weighted_average = pd.read_csv('weekly_butt_CC_weighted_average.csv')

series_tndrloin_weighted_average.dropna(inplace=True)
series_butt_bnls_weighted_average.dropna(inplace=True)
series_butt_CC_weighted_average.dropna(inplace=True)

period_tenderloin = 52
period_summer_peak = 26

stl_tndrloin = sm.tsa.STL(series_tndrloin_weighted_average['weighted_average'], period=period_tenderloin)
result_tndrloin = stl_tndrloin.fit()

trend_tndrloin = result_tndrloin.trend
seasonal_tndrloin = result_tndrloin.seasonal

stl_butt_bnls = sm.tsa.STL(series_butt_bnls_weighted_average['weighted_average'], period=period_summer_peak)
result_butt_bnls = stl_butt_bnls.fit()
trend_butt_bnls = result_butt_bnls.trend
seasonal_butt_bnls = result_butt_bnls.seasonal

stl_butt_CC = sm.tsa.STL(series_butt_CC_weighted_average['weighted_average'], period=period_summer_peak)
result_butt_CC = stl_butt_CC.fit()
trend_butt_CC = result_butt_CC.trend
seasonal_butt_CC = result_butt_CC.seasonal

y = trend_tndrloin

X = pd.DataFrame({
    'trend_butt_bnls': trend_butt_bnls,
    'trend_butt_CC': trend_butt_CC,
    'seasonal_tndrloin': seasonal_tndrloin,
    'seasonal_butt_bnls': seasonal_butt_bnls,
    'seasonal_butt_CC': seasonal_butt_CC
})

X.dropna(inplace=True)

y = y.loc[X.index]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
intercept_only_model = sm.OLS(y, sm.add_constant(np.ones(len(y)))).fit()

print("Full Model Summary:")
print(model.summary())
print("\nConstant-Only Model Summary:")
print(intercept_only_model.summary())

y = trend_tndrloin

X = pd.DataFrame({
    # 'trend_butt_bnls': trend_butt_bnls,
    'trend_butt_CC': trend_butt_CC,
    'seasonal_tndrloin': seasonal_tndrloin,
    'seasonal_butt_CC': seasonal_butt_CC
})

X.dropna(inplace=True)

y = y.loc[X.index]

X = sm.add_constant(X)

partial_model = sm.OLS(y, X).fit()

print("Partial Model Summary:")
print(partial_model.summary())

y = trend_tndrloin

X = pd.DataFrame({
    'trend_butt_bnls': trend_butt_bnls,
    'trend_butt_CC': trend_butt_CC,
    'seasonal_tndrloin': seasonal_tndrloin,
    'seasonal_butt_bnls': seasonal_butt_bnls,
    'seasonal_butt_CC': seasonal_butt_CC
})

X.dropna(inplace=True)

y = y.loc[X.index]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

fitted_values = model.predict(X)
residuals = y - fitted_values

plt.figure(figsize=(10, 6))
plt.scatter(y, fitted_values, alpha=0.5, label='Fitted Values')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label='Perfect Fit')  # Diagonal line
plt.xlabel('Actual Values (Trend Component)')
plt.ylabel('Fitted Values')
plt.title('Fitted Values vs Actual Values (Trend Component)')
plt.legend()
plt.savefig('Fitted OLS Values vs Actual Values (Trend Component)')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(fitted_values, residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--', lw=2)
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted Values')
plt.show()
