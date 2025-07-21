# test_load.py
import pandas as pd

data = pd.read_pickle("xgb_pipeline.pkl")
print(type(data))
