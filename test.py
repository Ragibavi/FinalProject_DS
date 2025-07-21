# import pandas as pd
# import numpy as np
# import pickle
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Load model pipeline
# with open("xgb_pipeline.pkl", "rb") as f:
#     pipeline = pickle.load(f)

# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.get_json()
#         df = pd.DataFrame([data])  # wrap in list to make single-row DataFrame

#         # Tambahkan fitur tambahan yang dibutuhkan oleh pipeline
#         df["order_hour"] = pd.to_datetime(df["created_at"]).dt.hour
#         df["order_dayofweek"] = pd.to_datetime(df["created_at"]).dt.dayofweek
#         df["order_month"] = pd.to_datetime(df["created_at"]).dt.month
#         df["is_weekend"] = df["order_dayofweek"].isin([5, 6]).astype(int)
#         df["is_peak_hour"] = df["order_hour"].between(11, 13).astype(int)  # contoh saja
#         df["is_night"] = df["order_hour"].between(0, 6).astype(int)
        
#         # Perhitungan tambahan (pastikan sesuai logika training model)
#         df["partner_load_ratio"] = (
#             df["total_outstanding_orders"] / df["total_onshift_partners"].replace(0, np.nan)
#         ).fillna(0)
        
#         df["item_diversity_ratio"] = (
#             df["num_distinct_items"] / df["total_items"].replace(0, np.nan)
#         ).fillna(0)
        
#         df["order_size_score"] = df["total_items"] * df["subtotal"]
#         df["price_range"] = df["max_item_price"] - df["min_item_price"]
#         df["order_pressure"] = df["total_outstanding_orders"] - df["total_busy_partners"]
#         df["complexity_score"] = (
#             df["item_diversity_ratio"] * df["order_size_score"]
#         )

#         # Prediksi
#         pred = pipeline.predict(df)[0]
#         return jsonify({"prediction": float(pred)})
    
#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)

