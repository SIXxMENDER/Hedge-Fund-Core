# Psiquis Live Alpha
### Real-Time HFT Arbitrage Scanner (Hacker UI)

---

## Overview

**Psiquis Live Alpha** is a lightweight, high-frequency trading (HFT) scanner designed for real-time demonstration and analysis. It connects directly to Binance and Kraken via their public APIs to monitor order books for arbitrage opportunities.

Unlike the core **Quant Engine**, this module features a specialized "Hacker UI" for visualization, providing immediate feedback on market latency, spread analysis, and potential alpha generation.

## Key Features

*   **Async I/O Core:** Built on `asyncio` and `ccxt.async_support` for non-blocking, low-latency data fetching.
*   **Real-Time Order Book Analysis:** Fetches and analyzes Level 2 order book data (bids/asks) in milliseconds.
*   **Weighted Price Calculation:** Simulates real execution prices based on order book depth and investment size, rather than just top-of-book prices.
*   **Hacker UI:** A terminal-based interface that visualizes scanning status, latency, and detected opportunities with color-coded alerts.
*   **Simulation Mode:** Includes a `--simulate` flag to inject artificial arbitrage opportunities for demonstration purposes.

## Quick Start

### Prerequisites
*   Python 3.10+
*   `ccxt` library

### Installation
```bash
pip install ccxt
```

### Usage

**Run the Live Scanner:**
```bash
python main.py
```

**Run in Simulation Mode (Demo):**
```bash
python main.py --simulate
```

---

**[Contact Psiquis-X](mailto:orquestadrop6@gmail.com)**
