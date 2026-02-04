import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("dataset1.csv")

X = df.drop("is_fake", axis=1)

# Load trained XGBoost model
model = joblib.load("xgb_dataset1.pkl")

# Feature importance
importance = model.feature_importances_

plt.figure()
plt.barh(X.columns, importance)
plt.xlabel("Importance Score")
plt.title("Feature Importance – Dataset 1 (XGBoost)")
plt.show()
