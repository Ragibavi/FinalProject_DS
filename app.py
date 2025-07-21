from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

DATA_PATH = "data/dataset.csv"

with open("model/xgb_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "API is running!"

@app.route("/data", methods=["GET"])
def get_all_data():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "Dataset file not found."}), 404

        df = pd.read_csv(DATA_PATH)
        data_preview = df.head(100).to_dict(orient="records")
        return jsonify(data_preview)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])

        input_df["created_at"] = pd.to_datetime(input_df["created_at"])
        input_df["actual_delivery_time"] = pd.to_datetime(input_df["actual_delivery_time"])
        
        input_df["order_hour"] = input_df["created_at"].dt.hour
        input_df["order_dayofweek"] = input_df["created_at"].dt.dayofweek
        input_df["order_month"] = input_df["created_at"].dt.month
        input_df["is_night"] = input_df["order_hour"].apply(lambda x: 1 if x < 6 or x > 20 else 0)
        input_df["is_peak_hour"] = input_df["order_hour"].apply(lambda x: 1 if x in [11,12,13,18,19] else 0)
        input_df["is_weekend"] = input_df["order_dayofweek"].apply(lambda x: 1 if x >= 5 else 0)
        input_df["item_diversity_ratio"] = input_df["num_distinct_items"] / input_df["total_items"]
        input_df["partner_load_ratio"] = input_df["total_busy_partners"] / (input_df["total_onshift_partners"] + 1)
        input_df["order_pressure"] = input_df["total_outstanding_orders"] / (input_df["total_onshift_partners"] + 1)
        input_df["order_size_score"] = input_df["subtotal"] / input_df["total_items"]
        input_df["complexity_score"] = input_df["total_items"] * input_df["item_diversity_ratio"]

        def price_range_score(row):
            range_ = row["max_item_price"] - row["min_item_price"]
            if range_ < 5:
                return 0 
            elif range_ > 20:
                return 2
            else:
                return 1

        input_df["price_range"] = input_df.apply(price_range_score, axis=1)

        prediction = model.predict(input_df)
        return jsonify({"prediction": float(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
