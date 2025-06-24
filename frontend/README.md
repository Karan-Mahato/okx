# OKX Trade Simulator Frontend

## Overview

This is the React-based frontend for the OKX Trade Simulator. It provides a real-time UI for simulating market orders, displaying slippage, fees, market impact, and net cost using live data from the backend.

---

## Technology Stack

- **React.js** (with Vite) — Fast, modern UI
- **Tailwind CSS** — Utility-first styling
- **Socket.IO Client** — Real-time backend events
- **Modular Components** — Main UI in `App.jsx`

---

## Directory Structure

```
frontend/
├── src/
│   ├── App.jsx         # Main UI (inputs/outputs)
│   ├── main.jsx        # App entry
│   ├── services/
│   │   └── socket.js   # WebSocket client
│   ├── assets/         # Static assets
│   └── App.css, index.css # Styling
├── public/             # Static files
├── package.json        # Dependencies & scripts
├── vite.config.js      # Vite config
```

---

## Key JavaScript Libraries

| Library          | Purpose                 |
| ---------------- | ----------------------- |
| react            | UI rendering            |
| socket.io-client | Real-time communication |
| tailwindcss      | Styling                 |
| vite             | Fast dev/build tooling  |

---

## UI & Functionality

- **Input Panel**: Enter exchange, asset, order type, quantity, volatility, and fee tier
- **Output Panel**: Displays slippage, fees, market impact, net cost, and latency
- **Real-time**: Updates instantly on new backend events

---

## Socket.IO Events

- **To Backend:**
  - `start_simulation`: Sends user-defined simulation parameters
- **From Backend:**
  - `orderbook_tick`: Receives simulated metrics

---

## Sample Payloads

**Input Example:**

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

**Output Example:**

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
npm install
```

### 2. Start the frontend development server

```sh
npm run dev
```

The app will be available at `http://localhost:5173` (default Vite port).

---

## Future Enhancements

- Historical trade simulation UI
- User login for fee tiers
- Real-time PnL and risk metrics
- Cross-exchange simulation support
