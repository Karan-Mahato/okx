import joblib
import numpy as np
import pandas as pd
import os 
from dotenv import load_dotenv

load_dotenv()

class SlippageModel:
    def __init__(self):
        # Load model path from .env
        model_path_env = os.getenv("SLIPPAGE_MODEL_PATH")

        # Get this file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Build absolute path
        model_path = os.path.join(current_dir, os.path.basename(model_path_env))

        # Debug print
        print(f"[DEBUG] Trying to load model from: {model_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Slippage model not found at {model_path}")

        self.model = joblib.load(model_path)
        self.feature_names = ['spread','mid_price','depth_top5','order_size']

    def extract_features(self, tick, order_size_usd=100):
        try:
            bids = sorted([(float(p), float(q)) for p,q in tick["bids"]], reverse=True)
            asks = sorted([(float(p), float(q)) for p,q in tick["bids"]])

            best_bid, best_ask = bids[0][0], asks[0][0]
            mid_price = (best_bid+best_ask)/2
            spread = best_ask-best_bid

            depth_bid = sum([p*q for p,q in bids[:5]])
            depth_ask = sum([p*q for p,q in asks[:5]])
            total_depth = depth_bid+depth_ask

            return np.array([spread,mid_price,total_depth,order_size_usd])
        except Exception as e:
            print(f"[!] Feature extraction failed: {e}")

    def predict_slippage(self,tick):
        features = self.extract_features(tick)
        df = pd.DataFrame([features], columns=self.feature_names)
        if features is not None:
            return self.model.predict(df)[0]
        return None