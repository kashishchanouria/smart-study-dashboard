import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = "data/study_data_500.csv"
MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()

print("Original shape:", df.shape)
print("\nColumns:", df.columns.tolist())

# -----------------------------
# Handle blank strings as null
# -----------------------------
df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

# -----------------------------
# Fill null values properly
# numeric -> median
# object/string -> mode or Unknown
# -----------------------------
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
object_cols = df.select_dtypes(include=["object"]).columns.tolist()

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())

for col in object_cols:
    mode_values = df[col].mode(dropna=True)
    fill_value = mode_values.iloc[0] if not mode_values.empty else "Unknown"
    df[col] = df[col].fillna(fill_value)

# -----------------------------
# Optional: clean exam_date if present
# -----------------------------
if "exam_date" in df.columns:
    df["exam_date"] = pd.to_datetime(df["exam_date"], errors="coerce")
    df["exam_year"] = df["exam_date"].dt.year
    df["exam_month"] = df["exam_date"].dt.month
    df["exam_day"] = df["exam_date"].dt.day
    df["exam_weekday"] = df["exam_date"].dt.dayofweek
    df.drop(columns=["exam_date"], inplace=True)

# -----------------------------
# Save cleaned dataset
# -----------------------------
df.to_csv("model/cleaned_data.csv", index=False)
print("\nCleaned dataset saved at: model/cleaned_data.csv")

# -----------------------------
# Encode string columns safely
# (for cleaned numeric version only)
# -----------------------------
encoded_df = df.copy()
encoding_maps = {}

for col in encoded_df.select_dtypes(include=["object"]).columns:
    encoded_df[col] = encoded_df[col].astype(str).str.strip()
    encoded_df[col], uniques = pd.factorize(encoded_df[col])
    encoding_maps[col] = list(uniques)

joblib.dump(encoding_maps, "model/encoding_maps.pkl")
encoded_df.to_csv("model/encoded_data.csv", index=False)
print("Encoded dataset saved at: model/encoded_data.csv")

# -----------------------------
# Use only 4 features for prediction
# -----------------------------
feature_columns = ["sleep", "focus", "study_hours", "breaks"]
target_column = "predicted_score"

missing = [c for c in feature_columns + [target_column] if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns in dataset: {missing}")

X = df[feature_columns].copy()
y = df[target_column].copy()

# Make sure all features are numeric
for col in feature_columns:
    X[col] = pd.to_numeric(X[col], errors="coerce")
    X[col] = X[col].fillna(X[col].median())

y = pd.to_numeric(y, errors="coerce")
y = y.fillna(y.median())

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Train model
# -----------------------------
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    max_depth=10
)
model.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print("\nModel trained successfully!")
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")

# -----------------------------
# Save model + feature order
# -----------------------------
joblib.dump(model, "model/study_model.pkl")
joblib.dump(feature_columns, "model/feature_columns.pkl")

print("\nSaved files:")
print("- model/study_model.pkl")
print("- model/feature_columns.pkl")
print("- model/cleaned_data.csv")
print("- model/encoded_data.csv")
print("- model/encoding_maps.pkl")