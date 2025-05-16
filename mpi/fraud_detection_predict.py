import joblib
import os
import pandas as pd
import numpy as np

MODEL_FILENAME = 'fraud_rf_model.pkl'
STATUSES = ['submitted', 'accepted', 'rejected']

def load_model(filename=MODEL_FILENAME):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Model file {filename} not found.")
    return joblib.load(filename)


def predict_from_file(data_path='synthetic_test_data.csv', model_path=MODEL_FILENAME):
    """
    Loads the model and dataset from disk, processes the data, and returns predictions.
    """
    # Load model
    model = load_model(model_path)

    # Read dataset
    df = pd.read_csv(data_path)

    # Save customer_id for reference
    customer_ids = df['customer_id']

    # Preprocess
    df_processed = df.copy()
    df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp']).astype(int) / 10**9

    # Encode status using the same order as training (ensure consistent mapping)
    status_mapping = {status: idx for idx, status in enumerate(STATUSES)}
    df_processed['status'] = df_processed['status'].map(status_mapping)

    # Drop unused columns
    X = df_processed.drop(columns=['fraudulent', 'customer_id'], errors='ignore')

    # Generate predictions
    predictions = model.predict(X)

    # Return predictions alongside customer_ids
    result = pd.DataFrame({
        'customer_id': customer_ids,
        'predicted_fraudulent': predictions
    })

    return result

if __name__ == '__main__':
    # Generate predictions for test data
    prediction_results = predict_from_file()
    print(prediction_results.head())
    print(np.sum(prediction_results["predicted_fraudulent"]))
