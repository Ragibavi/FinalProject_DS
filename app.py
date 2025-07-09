from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

CSV_FILE = 'dataset.csv'
PICKLE_FILE = 'dataset.pkl'

if not os.path.exists(PICKLE_FILE):
    if os.path.exists(CSV_FILE):
        df_csv = pd.read_csv(CSV_FILE)
        df_csv.to_pickle(PICKLE_FILE)
        print("CSV file found. Successfully converted to pickle.")
    else:
        columns = [
            "market_id", "created_at", "actual_delivery_time", "store_id",
            "store_primary_category", "order_protocol", "total_items", "subtotal",
            "num_distinct_items", "min_item_price", "max_item_price",
            "total_onshift_partners", "total_busy_partners", "total_outstanding_orders"
        ]
        pd.DataFrame(columns=columns).to_pickle(PICKLE_FILE)
        print("New pickle file created with predefined columns.")

@app.route('/api/insert', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        df = pd.read_pickle(PICKLE_FILE)
        new_df = pd.DataFrame([data])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_pickle(PICKLE_FILE)

        return jsonify({"message": "Data inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_pickle(PICKLE_FILE)
        return df.to_json(orient="records"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
