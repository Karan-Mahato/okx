import asyncio
import websockets
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

WS_URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
ORDER_SIZE_USD = 100
NUM_SAMPLES = 60000
CSV_FILE = "slippage_dataset.csv"
MODEL_FILE = "slippage_model.pkl"

data_points = []

def extract_features(tick, order_size_usd):
    try:
        bids = sorted([(float(p), float(q)) for p, q in tick["bids"]], reverse=True)
        asks = sorted([(float(p), float(q)) for p, q in tick["asks"]])

        best_bid, best_ask = bids[0][0], asks[0][0]
        mid_price = (best_bid + best_ask) / 2
        spread = best_ask - best_bid

        depth_bid = sum([p * q for p, q in bids[:5]])
        depth_ask = sum([p * q for p, q in asks[:5]])
        total_depth = depth_bid + depth_ask

        remaining = order_size_usd
        cost = 0.0
        for price, qty in asks:
            price = float(price)
            qty = float(qty)
            value = price * qty
            if value >= remaining:
                cost += remaining
                break
            else:
                cost += value
                remaining -= value

        avg_execution_price = cost / order_size_usd if order_size_usd else mid_price
        slippage = avg_execution_price - mid_price

        return {
            "spread": spread,
            "mid_price": mid_price,
            "depth_top5": total_depth,
            "order_size": order_size_usd,
            "slippage": slippage
        }
    except Exception:
        return None

async def collect_data():
    global data_points
    counter = 0

    while counter < NUM_SAMPLES:
        try:
            async with websockets.connect(WS_URL, ping_interval=10, ping_timeout=10) as ws:
                print("[*] Connected to WebSocket")
                async for message in ws:
                    tick = json.loads(message)
                    features = extract_features(tick, ORDER_SIZE_USD)
                    if features:
                        data_points.append(features)
                        counter += 1

                        if counter % 500 == 0:
                            print(f"Collected {counter} samples...")

                        if counter >= NUM_SAMPLES:
                            print("[*] Reached required number of samples.")
                            return
        except websockets.ConnectionClosedError as e:
            print(f"[!] Connection closed with error: {e}. Reconnecting...")
            await asyncio.sleep(5)  # wait before reconnect
        except Exception as e:
            print(f"[!] Unexpected error: {e}. Reconnecting...")
            await asyncio.sleep(5)

def save_and_train():
    df = pd.DataFrame(data_points)
    df.to_csv(CSV_FILE, index=False)
    print(f"[+] Saved {len(df)} samples to {CSV_FILE}")

    X = df[["spread", "mid_price", "depth_top5", "order_size"]]
    y = df["slippage"]

    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    print(f"[+] Model trained and saved to {MODEL_FILE}")

if __name__ == "__main__":
    print("[*] Starting data collection...")
    asyncio.run(collect_data())
    print("[*] Training model...")
    save_and_train()
    print("[✔] Done!")
