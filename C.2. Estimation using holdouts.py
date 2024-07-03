# Let's use one of the previous models for out-of-sample predictions. You can choose any of them.
# Exercise:
# 1. Split data in two subsets: before 2023 (train set) and 2023 (test set). 2. Fit OLS model on train set.
#   done
# 3. Predict on validation test set.
#   done
# 4. Compare to actual in 2023 to calculate the out-of-sample error.
#   done

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime

combined_df = pd.read_csv('combined_scaled_df.csv')

combined_df['report_date'] = pd.to_datetime(combined_df['report_date'])

train_df = combined_df[combined_df['report_date'] < '2023-01-01']
test_df = combined_df[combined_df['report_date'] >= '2023-01-01']

y_train = train_df['weighted_average_tndrloin_scaled']
X_train = train_df[['weighted_average_butt_bnls_scaled', 'weighted_average_butt_CC_scaled']]

X_train = sm.add_constant(X_train)

y_test = test_df['weighted_average_tndrloin_scaled']
X_test = test_df[['weighted_average_butt_bnls_scaled', 'weighted_average_butt_CC_scaled']]

X_test = sm.add_constant(X_test)

train_model = sm.OLS(y_train, X_train).fit()

print(train_model.summary())

y_pred = train_model.predict(X_test)

mae = np.mean(np.abs(y_test - y_pred))
rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Squared Error (RMSE): {rmse}")

test_dates = test_df['report_date']

plt.figure(figsize=(14, 7))
plt.plot(test_dates, y_test, label='Actual Values (2023)', color='blue', marker='o')
plt.plot(test_dates, y_pred, label='Predicted Values (2023)', color='red', linestyle='--', marker='x')
plt.xlabel('Date')
plt.ylabel('Scaled Weighted Average (Tenderloin)')
plt.title('Actual vs Predicted Values (2023)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Trained Prediction vs Test Values 2023')
plt.show()


