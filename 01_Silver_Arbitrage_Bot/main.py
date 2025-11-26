# main.py

import sys
import time

# Requirement 1 & 2: Use 'ccxt' and wrap imports in a try/except block.
try:
    import ccxt
except ImportError:
    print("The 'ccxt' library is not installed.")
    print("Please install the required packages by running:")
    print("pip install ccxt")
    # A requirements.txt would typically just contain 'ccxt'
    # For a more complete setup, you might suggest:
    # print("pip install -r requirements.txt")
    sys.exit(1)

def initialize_exchanges():
    """
    Initializes and returns public instances of Binance and Kraken exchanges.
    """
    # Requirement 3: Connect to Binance and Kraken using PUBLIC APIs only.
    # No API keys are provided, so ccxt will use the public endpoints.
    try:
        binance = ccxt.binance({
            'options': {
                'defaultType': 'spot',
            },
        })
        kraken = ccxt.kraken()
        
        # Optional: Load markets to verify connection, though fetch_ticker will do this implicitly.
        binance.load_markets()
        kraken.load_markets()
        
        print("Successfully connected to Binance and Kraken public APIs.")
        return binance, kraken
        
    except ccxt.NetworkError as e:
        print(f"Network Error during initialization: {e}")
        print("Please check your internet connection.")
        sys.exit(1)
    except ccxt.ExchangeError as e:
        print(f"Exchange Error during initialization: {e}")
        print("One of the exchanges might be down or unavailable.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during initialization: {e}")
        sys.exit(1)

def fetch_prices(binance, kraken, symbol='BTC/USDT'):
    """
    Fetches the last traded price for a given symbol from two exchanges.
    """
    try:
        # Requirement 4 (part 1): Fetch BTC/USDT price from both.
        binance_ticker = binance.fetch_ticker(symbol)
        kraken_ticker = kraken.fetch_ticker(symbol)

        binance_price = binance_ticker.get('last')
        kraken_price = kraken_ticker.get('last')

        if binance_price is None or kraken_price is None:
            print(f"Warning: Could not fetch 'last' price for {symbol} from one or both exchanges.")
            return None, None

        return binance_price, kraken_price
    
    except ccxt.NetworkError as e:
        print(f"Network Error while fetching prices: {e}")
    except ccxt.ExchangeError as e:
        print(f"Exchange Error while fetching prices: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching prices: {e}")
        
    return None, None

def main():
    """
    Main function to run the arbitrage bot loop.
    """
    binance, kraken = initialize_exchanges()
    
    SYMBOL = 'BTC/USDT'
    ARBITRAGE_THRESHOLD_PERCENT = 0.5 # Requirement 4: 0.5% spread

    print(f"\nStarting arbitrage bot for {SYMBOL}...")
    print(f"Looking for opportunities with a spread greater than {ARBITRAGE_THRESHOLD_PERCENT}%.")
    print("-" * 60)

    # Requirement 5: Use a simple 'while True' loop.
    while True:
        binance_price, kraken_price = fetch_prices(binance, kraken, SYMBOL)

        if binance_price and kraken_price:
            # Requirement 4 (part 2): Calculate spread.
            higher_price = max(binance_price, kraken_price)
            lower_price = min(binance_price, kraken_price)
            
            spread_percentage = ((higher_price - lower_price) / lower_price) * 100

            # Get current timestamp for logging
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            print(
                f"[{timestamp}] "
                f"Binance: ${binance_price:,.2f} | "
                f"Kraken: ${kraken_price:,.2f} | "
                f"Spread: {spread_percentage:.3f}%"
            )

            # Requirement 4 (part 3): Check for arbitrage opportunity.
            if spread_percentage > ARBITRAGE_THRESHOLD_PERCENT:
                buy_exchange = "Binance" if binance_price < kraken_price else "Kraken"
                sell_exchange = "Kraken" if binance_price < kraken_price else "Binance"
                
                print("\n" + "!" * 25)
                print(f"  Arbitrage Opportunity Found! Spread: {spread_percentage:.3f}%")
                print(f"  -> BUY {SYMBOL} on {buy_exchange} at ${lower_price:,.2f}")
                print(f"  -> SELL {SYMBOL} on {sell_exchange} at ${higher_price:,.2f}")
                print("!" * 25 + "\n")
        
        # Requirement 5: sleep for 5 seconds.
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        sys.exit(0)