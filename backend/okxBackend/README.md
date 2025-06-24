# OKX Trade Simulator Backend

## Overview

This backend powers the real-time trade simulator for the OKX exchange. It provides APIs and real-time WebSocket events to estimate slippage, fees, market impact, and net cost for simulated market orders using live order book data.

---

## Technology Stack

- **FastAPI** — High-performance Python web framework
- **python-socketio** — WebSocket server for real-time events
- **asyncio** — Non-blocking I/O
- **websockets** — Connects to OKX WebSocket feeds
- **Custom modules**:
  - `slippage.py` — Regression model for price slippage
  - `impact.py` — Market impact estimator
  - `fees.py` — Dynamic fee calculator

---

## Directory Structure

```
backend/okxBackend/
├── main.py                # FastAPI + Socket.IO entrypoint
├── websocket_handler.py   # OKX streaming + emit logic
├── models/
│   ├── fees.py
│   ├── slippage.py
│   ├── impact.py
│   └── slippage_model.pkl # Trained regression model
├── modelTrain.py          # Model training script
├── Scripts/               # Virtual environment scripts
├── Lib/                   # Python packages
```

---

## Key Python Libraries

| Library             | Purpose                       |
| ------------------- | ----------------------------- |
| fastapi             | API and server management     |
| python-socketio     | WebSocket server              |
| websockets          | Connect to OKX WebSocket feed |
| asyncio             | Concurrency handling          |
| numpy, scikit-learn | Regression modeling           |
| uvicorn             | ASGI server for FastAPI app   |
| pandas, statsmodels | Data processing & stats       |

---

## Model Methodology

- **Slippage**: Linear regression on spread, depth, and order size.
- **Market Impact**: Square-root law: `Impact = α × sqrt(order_size / liquidity) + β`
- **Fees**: Tiered fee logic in `fees.py`

---

## Socket.IO Events

- **From Frontend:**
  - `start_simulation`: Starts a simulation with user parameters
- **To Frontend:**
  - `orderbook_tick`: Emits simulated metrics (slippage, fees, impact, net cost, latency)

---

## Sample Payloads

**Input:**

```json
{
  "exchange": "OKX",
  "spotAsset": "BTC/USDT",
  "orderType": "market",
  "quantity": 100,
  "volatility": "High",
  "feeTier": "Lvl1"
}
```

**Output:**

```json
{
  "slippage": 0.92,
  "fees": 0.06,
  "market_impact": 1.21,
  "netCost": 2.19,
  "latency_ms": 14.2
}
```

---

## Setup & Usage

### 1. Install dependencies

```sh
pip install -r ../requirements.txt
```

### 2. Activate virtual environment (Windows)

```sh
Scripts\activate
```

### 3. Start the backend server

```sh
uvicorn main:sio_app --reload
```

The backend will be available for Socket.IO and REST API requests.

---

## Future Enhancements

- Historical trade simulation
- Limit order modeling
- User-specific fee tiers
- Real-time risk & PnL metrics
- Multi-exchange support
