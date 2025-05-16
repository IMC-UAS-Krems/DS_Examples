import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
from datetime import datetime, timedelta
import random
import os

# Constants
STATUSES = ['submitted', 'accepted', 'rejected']
NUM_VENDORS = 100
MODEL_FILENAME = 'fraud_rf_model.pkl'

# Helper functions
def generate_random_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def generate_dataset(size):
    data = {
        'customer_id': np.arange(1, size + 1),
        'timestamp': [generate_random_timestamp(datetime(2022, 1, 1), datetime(2024, 1, 1)) for _ in range(size)],
        'status': np.random.choice(STATUSES, size=size),
        'vendor_id': np.random.randint(1, NUM_VENDORS + 1, size=size),
        'amount': np.round(np.random.uniform(10.0, 1000.0, size), 2),
        'fraudulent': np.random.choice([0, 1], size=size, p=[0.85, 0.15])  # Imbalanced fraud
    }
    return pd.DataFrame(data)

def preprocess_data(df):
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp']).astype(int) / 10**9  # Convert to Unix timestamp
    le_status = LabelEncoder()
    df['status'] = le_status.fit_transform(df['status'])
    return df, le_status

def train_model(df):
    X = df.drop(columns=['fraudulent', 'customer_id'])
    y = df['fraudulent']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Model performance:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_FILENAME)
    print(f"Model saved to {MODEL_FILENAME}")

    return model


if __name__ == '__main__':
    # Step 1: Generate training dataset
    df_train = generate_dataset(5000)
    df_train_processed, _ = preprocess_data(df_train)

    # Step 2: Train and save model
    train_model(df_train_processed)

    # Step 3: Generate another random dataset and save to CSV
    df_test = generate_dataset(1000)
    df_test.to_csv('synthetic_test_data.csv', index=False)
    print("Synthetic test data saved to synthetic_test_data.csv")

