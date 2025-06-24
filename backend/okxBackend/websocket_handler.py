import asyncio
import websockets
import json
import time
import os
from dotenv import load_dotenv, find_dotenv
from models.slippage import SlippageModel
import time
from models.impact import AlmgrenChrissModel
from models.fees import calculate_fee

load_dotenv(find_dotenv())
WS_URL = os.getenv("WS_URL")

slippage_model = SlippageModel()
impact_model = AlmgrenChrissModel()

"""
Connects to OKX's WebSocket endpoint and listens to L2 order book updates.
For each tick, extracts best bid/ask and calculates internal processing latency.
"""
async def orderbook_stream(sio, client_configs):
    while True:
        try:
            async with websockets.connect(WS_URL, ping_interval=20, ping_timeout=20) as ws:
                print("[*] Connected to OKX WebSocket")
                tick_count = 0

                async for message in ws:
                    tick_count += 1
                    tick = json.loads(message)

                    # Extract mid-price
                    best_bid = float(tick["bids"][0][0])
                    best_ask = float(tick["asks"][0][0])
                    mid_price = (best_bid + best_ask) / 2

                    for sid, config in client_configs.items():
                        try:
                            quantity_usd = float(config.get("quantity",100))
                            fee_tier = config.get("feeTier", "tier_1")
                            symbol = config.get("spotAsset", "BTC/USDT")

                            start = time.perf_counter()
                            start1 = time.perf_counter()

                            slippage = slippage_model.predict_slippage(tick)
                            latency_ms_slippage = round((time.perf_counter() - start1) * 1000, 3)

                            start2 = time.perf_counter()
                            market_impact = impact_model.estimate_impact(quantity=quantity_usd, price=mid_price)
                            latency_ms_marcket = round((time.perf_counter() - start2) * 1000, 3)
                            
                            #Expected fee    
                            start3 = time.perf_counter()
                            fees = calculate_fee(quantity_usd=quantity_usd, fee_tier=fee_tier)
                            latency_ms_fees = round((time.perf_counter() - start3) * 1000, 3)
                            
                            #Net Cost
                            netCost = slippage + fees + market_impact

                            latency_ms = round((time.perf_counter() - start) * 1000, 3)

                            # Prepare payload
                            payload = {
                                "tick_id": tick_count,
                                "timestamp": tick["timestamp"],
                                "symbol": tick["symbol"],
                                "mid_price": round(mid_price, 2),
                                "slippage": round(slippage, 6) if slippage else None,
                                "latency_ms": latency_ms,
                                "market_impact": round(market_impact, 6) if market_impact else None,
                                "fees": fees,
                                "netCost": round(netCost, 6) if netCost else None,
                            }

                            print(f"[Tick {tick_count}] Latency_total: {latency_ms}ms | Latency_slippage: {latency_ms_slippage}ms  | Latency_marcket: {latency_ms_marcket}ms | Latenc_fee: {latency_ms_fees}ms ")

                            # Emit to frontend
                            await sio.emit("orderbook_tick", payload, to=sid)
                            
                        except Exception as e:
                            print(f"[!] Error processing tick for sid {sid}: {e}")

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[WebSocket Closed] {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)

        except Exception as e:
            print(f"[Error] Unexpected exception: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)



# Store config per-client (sid)
async def handle_start_simulation(sid, data):
    from main import client_configs  # import the shared config dict
    print(f"[{sid}] Simulation started with inputs: {data}")
    client_configs[sid] = data
    await asyncio.sleep(0)  # Yield control

# Clean up on disconnect
async def handle_disconnect(sid):
    from main import client_configs
    print(f"[{sid}] Disconnected")
    client_configs.pop(sid, None)