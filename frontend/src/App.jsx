import './App.css'
import { useEffect, useState } from "react"
import socket from './services/socket'

export default function TradingUI() {
  const [inputs, setInputs] = useState({
    exchange: "OKX",
    spotAsset: "BTC/USDT",
    orderType: "market",
    quantity: 100,
    volatility: "Medium",
    feeTier: "Standard",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs({ ...inputs, [name]: value });
  };

  const [tick, setTick] = useState(null)

  useEffect(() =>{
    socket.on("orderbook_tick", (data)=>{
      const renderStart = performance.now();
      setTick(data);
      
      // Log render time after state update
      requestAnimationFrame(() => {
        const renderEnd = performance.now();
        console.log(`UI Update Time: ${Math.round(renderEnd - renderStart)}ms`);
      });
    });

    return () =>{
      socket.off("orderbook_tick");
    };
  }, []);


  const handleSubmit = () => {
  socket.emit("start_simulation", inputs);
  };



  return (
    <div className="max-w-7xl mx-auto px-4 py-6 bg-blue-50 min-h-screen">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left Panel - Input Parameters */}
        <div className="w-full lg:w-1/2 bg-white rounded-2xl shadow p-6 border border-blue-200">
          <h2 className="text-2xl font-bold mb-6 text-black">Input Parameters</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-100 p-4 rounded-xl border border-blue-300">
              <label className="block text-sm font-medium text-black mb-1">Exchange</label>
              <input
                type="text"
                name="exchange"
                value={inputs.exchange}
                onChange={handleChange}
                className="w-full p-2 border border-blue-300 rounded-md bg-blue-50 text-black"
                disabled
              />
            </div>

            <div className="bg-white p-4 rounded-xl border border-blue-300">
              <label className="block text-sm font-medium text-black mb-1">Spot Asset</label>
              <input
                type="text"
                name="spotAsset"
                value={inputs.spotAsset}
                onChange={handleChange}
                className="w-full p-2 border border-blue-300 rounded-md text-black"
              />
            </div>

            <div className="bg-blue-100 p-4 rounded-xl border border-blue-300">
              <label className="block text-sm font-medium text-black mb-1">Order Type</label>
              <input
                type="text"
                name="orderType"
                value={inputs.orderType}
                onChange={handleChange}
                className="w-full p-2 border border-blue-300 rounded-md bg-blue-50 text-black"
                disabled
              />
            </div>

            <div className="bg-white p-4 rounded-xl border border-blue-300">
              <label className="block text-sm font-medium text-black mb-1">Quantity (USD)</label>
              <input
                type="number"
                name="quantity"
                value={inputs.quantity}
                onChange={handleChange}
                className="w-full p-2 border border-blue-300 rounded-md text-black"
              />
            </div>

            <div className="bg-blue-100 p-4 rounded-xl border border-blue-300">
              <label className="block text-sm font-medium text-black mb-1">Volatility</label>
              <select
                name="volatility"
                value={inputs.volatility}
                onChange={handleChange}
                className="w-full p-2 border border-blue-300 rounded-md text-black bg-blue-50"
              >
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
              </select>
            </div>

            <div className="bg-white p-4 rounded-xl border border-blue-300">
              <label className="block text-sm font-medium text-black mb-1">Fee Tier</label>
              <select
                name="feeTier"
                value={inputs.feeTier}
                onChange={handleChange}
                className="w-full p-2 border border-blue-300 rounded-md text-black"
              >
                <option>Standard</option>
                <option value="tier_1">Lvl 1</option>
                <option value="tier_2">Lvl 2</option>
                <option value="tier_3">Lvl 3</option>
                <option value="tier_4">Lvl 4</option>
                <option value="tier_5">Lvl 5</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            className="mt-6 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-700 transition"
          >
            Submit
          </button>


        </div>

        {/* Right Panel - Output Values */}
        <div className="w-full lg:w-1/2 bg-white rounded-2xl shadow p-6 border border-blue-200">
          <h2 className="text-2xl font-bold mb-6 text-black">Processed Output</h2>
          <div className="space-y-4 text-left text-black">
            <div className="bg-blue-100 p-4 rounded-xl border border-blue-300">
              <span className="font-semibold">Expected Slippage ($):</span> {tick?.slippage ?? "-"} 
            </div>
            <div className="bg-white p-4 rounded-xl border border-blue-300">
              <span className="font-semibold">Expected Fees ($):</span> {tick?.fees ?? "-"}
            </div>
            <div className="bg-blue-100 p-4 rounded-xl border border-blue-300">
              <span className="font-semibold">Expected Market Impact ($):</span> {tick?.market_impact ?? "-"}
            </div>
            <div className="bg-white p-4 rounded-xl border border-blue-300">
              <span className="font-semibold">Net Cost ($):</span> {tick?.netCost ?? "-"}
            </div>
            <div className="bg-white p-4 rounded-xl border border-blue-300">
              <span className="font-semibold">Internal Latency (ms):</span> {tick?.latency_ms ?? "-"}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
