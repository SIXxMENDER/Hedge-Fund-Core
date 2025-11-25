# -*- coding: utf-8 -*-
"""
Professional-level script (Silver Tier) to connect to Binance,
download BTC/USDT OHLCV data and calculate RSI and MACD indicators.

This script is autonomous and ready to be executed.

External dependencies:
- ccxt: to interact with the Binance API.
- pandas: for data manipulation and analysis.
- ta: for technical indicator calculation.

To install dependencies, run in your terminal:
pip install ccxt pandas ta
"""

# --- Required Imports ---
import sys
import ccxt
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

# --- Configuration Constants ---
# You can modify these values to analyze other pairs or timeframes.
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'  # Timeframe (e.g., '1m', '5m', '15m', '1h', '4h', '1d')
DATA_LIMIT = 200  # Number of candles to download (sufficient for RSI(14) and MACD)


def fetch_ohlcv(symbol: str, timeframe: str, limit: int) -> list | None:
    """
    Connects to Binance using ccxt and downloads OHLCV data (Open, High, Low, Close, Volume).

    Args:
        symbol (str): The trading pair (e.g., 'BTC/USDT').
        timeframe (str): The time interval for candles (e.g., '1h').
        limit (int): The number of candles to download.

    Returns:
        list | None: A list of lists with OHLCV data, or None if an error occurs.
    """
    print(f"[*] Connecting to Binance to download {limit} candles of {symbol} in {timeframe} timeframe...")
    try:
        # Initialize the exchange (no API keys needed for public data)
        exchange = ccxt.binance()

        # Check that the exchange supports the required functionality
        if not exchange.has['fetchOHLCV']:
            print(f"[!] Error: The exchange {exchange.id} does not support OHLCV data download.", file=sys.stderr)
            return None

        # Download OHLCV data
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

        if not ohlcv:
            print(f"[!] No data received for {symbol}. Check the symbol and timeframe.", file=sys.stderr)
            return None

        print("[+] OHLCV data downloaded successfully.")
        return ohlcv

    except ccxt.NetworkError as e:
        print(f"[!] Network error while connecting to Binance: {e}", file=sys.stderr)
        return None
    except ccxt.ExchangeError as e:
        print(f"[!] Binance exchange error (check the symbol): {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[!] An unexpected error occurred while downloading data: {e}", file=sys.stderr)
        return None


def process_ohlcv_to_dataframe(ohlcv: list) -> pd.DataFrame:
    """
    Converts OHLCV data into a pandas DataFrame and adds technical indicators.

    Args:
        ohlcv (list): List of lists with OHLCV data.

    Returns:
        pd.DataFrame: DataFrame with processed data and calculated indicators.
    """
    print("[*] Processing OHLCV data...")

    # Create DataFrame with standard columns
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Convert timestamp to readable date
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate RSI (Relative Strength Index) with period 14 using ta library
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()

    # Calculate MACD (Moving Average Convergence Divergence) using ta library
    macd_indicator = MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd_indicator.macd()
    df['macd_signal'] = macd_indicator.macd_signal()
    df['macd_diff'] = macd_indicator.macd_diff()

    print("[+] Technical indicators calculated (RSI, MACD).")
    return df


def display_summary(df: pd.DataFrame) -> None:
    """
    Displays a summary of the data and the latest calculated values.

    Args:
        df (pd.DataFrame): DataFrame with processed data.
    """
    print("\n" + "="*80)
    print("DATA AND TECHNICAL ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nTotal candles downloaded: {len(df)}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nLast 5 rows:\n{df.tail()}")
    
    # Show latest indicator values
    last_row = df.iloc[-1]
    print("\n" + "-"*80)
    print("CURRENT TECHNICAL INDICATOR VALUES")
    print("-"*80)
    print(f"Most recent closing price: ${last_row['close']:.2f}")
    print(f"RSI(14): {last_row['rsi']:.2f}")
    print(f"MACD: {last_row['macd']:.4f}")
    print(f"MACD Signal: {last_row['macd_signal']:.4f}")
    print(f"MACD Histogram: {last_row['macd_diff']:.4f}")
    print("="*80 + "\n")


def main():
    """
    Main function that executes the complete script flow.
    """
    print("\n🚀 Starting Catalyst Data Engine (Silver Tier)...\n")
    
    # Step 1: Download OHLCV data
    ohlcv_data = fetch_ohlcv(SYMBOL, TIMEFRAME, DATA_LIMIT)
    
    if ohlcv_data is None:
        print("\n[!] Could not obtain data. Terminating script.")
        sys.exit(1)
    
    # Step 2: Process data and calculate indicators
    df = process_ohlcv_to_dataframe(ohlcv_data)
    
    # Step 3: Display summary
    display_summary(df)
    
    print("✅ Script executed successfully.\n")


if __name__ == "__main__":
    main()
