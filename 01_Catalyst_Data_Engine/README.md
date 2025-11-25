# Catalyst Data Engine 📊

## Silver Level | Critical Task Accelerator

### Description

The **Catalyst Data Engine** is the fundamental market data ingestion and processing engine. This module connects with cryptocurrency exchanges (Binance) to download real-time OHLCV (Open, High, Low, Close, Volume) data and calculate key technical indicators.

### Value Proposition

> "We will eliminate your most costly operational bottleneck in less than 30 days. We deliver a surgical tool that automates a critical task, freeing your team to focus on strategy and reducing human error risk to zero. It's the fastest way to experience institutional-grade automation efficiency."

### Main Features

✅ **Exchange Connectivity:** Integration with Binance via ccxt library (easily extensible to other exchanges)

✅ **Historical Data Download:** Obtaining OHLCV data with configurable timeframes (1m, 5m, 15m, 1h, 4h, 1d)

✅ **Automatic Technical Indicators:**
- RSI (Relative Strength Index) with period 14
- MACD (Moving Average Convergence Divergence) with 12/26/9 parameters

✅ **Processing with Pandas:** Efficient data manipulation using DataFrames

✅ **Robust Error Handling:** Network exception and exchange error management

### Use Cases

- **Quantitative research automation:** Massive data download for backtesting
- **Multi-pair monitoring:** Scanning for opportunities across different assets
- **Indicator-based alerts:** Automatic detection of oversold/overbought conditions
- **AI model feeding:** Data preparation for machine learning

### Installation

```bash
pip install ccxt pandas pandas-ta
```

### Usage

```bash
python data_loader.py
```

### Configuration

You can modify the constants in the file to customize behavior:

```python
SYMBOL = 'BTC/USDT'      # Trading pair
TIMEFRAME = '1h'          # Time interval
DATA_LIMIT = 200          # Number of candles to download
```

### Example Output

```
🚀 Starting Catalyst Data Engine (Silver Tier)...

[*] Connecting to Binance to download 200 candles of BTC/USDT in 1h timeframe...
[+] OHLCV data downloaded successfully.
[*] Processing OHLCV data...
[+] Technical indicators calculated (RSI, MACD).

================================================================================
DATA AND TECHNICAL ANALYSIS SUMMARY
================================================================================

Total candles downloaded: 200

--------------------------------------------------------------------------------
CURRENT TECHNICAL INDICATOR VALUES
--------------------------------------------------------------------------------
Most recent closing price: $64,250.00
RSI(14): 58.32
MACD: 125.4523
MACD Signal: 98.3421
MACD Histogram: 27.1102
================================================================================

✅ Script executed successfully.
```

### Code Architecture

```
data_loader.py
├── fetch_ohlcv()              # Download data from Binance
├── process_ohlcv_to_dataframe()  # Process and calculate indicators
├── display_summary()          # Display data summary
└── main()                     # Orchestrate complete flow
```

### Next Steps

This Silver module is the perfect foundation for:
- **Scaling to Gold level:** Integrate automated execution bot
- **Implementing alerts:** Notifications when RSI/MACD cross thresholds
- **Expanding data sources:** Add news, social media sentiment

---

**Part of the Hedge Fund Core ecosystem | Algorithmic Trading Architecture**
