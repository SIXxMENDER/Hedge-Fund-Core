import asyncio
import ccxt.async_support as ccxt
import sys
import time
import argparse
import random
from datetime import datetime

# --- HACKER UI CONSTANTS ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    print(Colors.CYAN + """
    ██████╗ ███████╗██╗ ██████╗ ██╗   ██╗██╗███████╗    ██╗  ██╗
    ██╔══██╗██╔════╝██║██╔═══██╗██║   ██║██║██╔════╝    ╚██╗██╔╝
    ██████╔╝███████╗██║██║   ██║██║   ██║██║███████╗     ╚███╔╝ 
    ██╔═══╝ ╚════██║██║██║▄▄ ██║██║   ██║██║╚════██║     ██╔██╗ 
    ██║     ███████║██║╚██████╔╝╚██████╔╝██║███████║    ██╔╝ ██╗
    ╚═╝     ╚══════╝╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝    ╚═╝  ╚═╝
    """ + Colors.ENDC)
    print(Colors.HEADER + "    HFT CORE v4.0 | ASYNC ORDER BOOK ANALYZER" + Colors.ENDC)
    print(Colors.HEADER + "    -----------------------------------------" + Colors.ENDC)
    print()

class HFTArbitrageBot:
    def __init__(self, symbol="BTC/USDT", simulate=False):
        self.symbol = symbol
        self.simulate = simulate
        self.investment = 1000.0  # USD size for weighted price calc
        self.fee_rate = 0.001     # 0.1% per trade
        self.iteration = 0
        self.exchanges = {}
        
    async def initialize(self):
        print(f"{Colors.BLUE}[INIT] Initializing Async Event Loop...{Colors.ENDC}")
        self.exchanges['binance'] = ccxt.binance({'enableRateLimit': True})
        self.exchanges['kraken'] = ccxt.kraken({'enableRateLimit': True})
        
        # Warmup
        tasks = [ex.load_markets() for ex in self.exchanges.values()]
        await asyncio.gather(*tasks)
        print(f"{Colors.GREEN}[OK] Connected to Liquidity Providers (Public API){Colors.ENDC}\n")

    async def close(self):
        for ex in self.exchanges.values():
            await ex.close()

    async def fetch_book(self, exchange_name):
        try:
            # Fetch Level 2 Order Book (Limit 5 for speed)
            return await self.exchanges[exchange_name].fetch_order_book(self.symbol, limit=5)
        except Exception:
            return None

    def get_weighted_price(self, order_book, side, amount_usd):
        """
        Calculates the real execution price for a given USD amount 
        by walking the order book depth.
        side: 'bids' (selling into) or 'asks' (buying from)
        """
        if not order_book or side not in order_book:
            return None
            
        remaining_usd = amount_usd
        total_qty = 0.0
        weighted_sum = 0.0
        
        for entry in order_book[side]:
            price, qty = entry[0], entry[1]
            cost = price * qty
            if cost >= remaining_usd:
                # Fill the rest
                fill_qty = remaining_usd / price
                total_qty += fill_qty
                weighted_sum += fill_qty * price
                remaining_usd = 0
                break
            else:
                # Consume this level
                total_qty += qty
                weighted_sum += qty * price
                remaining_usd -= cost
                
        if remaining_usd > 0:
            return None # Not enough liquidity
            
        return weighted_sum / total_qty

    async def run(self):
        await self.initialize()
        
        print(f"{Colors.WARNING}[SYSTEM] HFT Radar Active. Scanning {self.symbol} Order Books...{Colors.ENDC}")
        print(f"{Colors.BLUE}[CONFIG] Investment: ${self.investment} | Fee: {self.fee_rate*100}% | Sim: {self.simulate}{Colors.ENDC}\n")

        try:
            while True:
                self.iteration += 1
                
                # 1. Async Fetch
                t0 = time.time()
                tasks = {
                    'binance': self.fetch_book('binance'),
                    'kraken': self.fetch_book('kraken')
                }
                results = await asyncio.gather(*tasks.values(), return_exceptions=True)
                books = dict(zip(tasks.keys(), results))
                
                if not books['binance'] or not books['kraken'] or isinstance(books['binance'], Exception):
                    continue

                # 2. Simulation Injection (The "10/10" Demo Feature)
                if self.simulate and self.iteration % 10 == 0:
                    # Inject a massive anomaly in Kraken's book
                    # We lower Kraken ASK to create a BUY opportunity there
                    best_bid_binance = books['binance']['bids'][0][0]
                    fake_ask = best_bid_binance * 0.990 # 1% lower than Binance Bid
                    
                    # Overwrite the first level of Kraken Asks
                    books['kraken']['asks'][0] = [fake_ask, 5.0] # Price, Volume

                # 3. Calculate Real Execution Prices (Weighted)
                # Strategy A: Buy Binance (Ask), Sell Kraken (Bid)
                price_buy_bin = self.get_weighted_price(books['binance'], 'asks', self.investment)
                price_sell_krk = self.get_weighted_price(books['kraken'], 'bids', self.investment)
                
                # Strategy B: Buy Kraken (Ask), Sell Binance (Bid)
                price_buy_krk = self.get_weighted_price(books['kraken'], 'asks', self.investment)
                price_sell_bin = self.get_weighted_price(books['binance'], 'bids', self.investment)

                opportunity = None
                
                # Check Strategy A
                if price_buy_bin and price_sell_krk:
                    # Net Profit = (Sell * (1-fee)) - (Buy * (1+fee))
                    net_sell = price_sell_krk * (1 - self.fee_rate)
                    net_buy = price_buy_bin * (1 + self.fee_rate)
                    profit_pct = ((net_sell - net_buy) / net_buy) * 100
                    
                    if profit_pct > 0.05: # Min threshold
                        opportunity = ('BINANCE', 'KRAKEN', price_buy_bin, price_sell_krk, profit_pct)

                # Check Strategy B
                if not opportunity and price_buy_krk and price_sell_bin:
                    net_sell = price_sell_bin * (1 - self.fee_rate)
                    net_buy = price_buy_krk * (1 + self.fee_rate)
                    profit_pct = ((net_sell - net_buy) / net_buy) * 100
                    
                    if profit_pct > 0.05:
                        opportunity = ('KRAKEN', 'BINANCE', price_buy_krk, price_sell_bin, profit_pct)

                # 4. UI / UX
                latency = (time.time() - t0) * 1000
                
                if opportunity:
                    buy_ex, sell_ex, buy_p, sell_p, profit = opportunity
                    # Clear line
                    sys.stdout.write('\r' + ' ' * 100 + '\r')
                    
                    print(f"{Colors.GREEN}{Colors.BOLD}>>> ALPHA DETECTED [{profit:.3f}% NET] <<<{Colors.ENDC}")
                    print(f"  {Colors.CYAN}BUY :{Colors.ENDC} {buy_ex:<8} @ {buy_p:.2f}")
                    print(f"  {Colors.CYAN}SELL:{Colors.ENDC} {sell_ex:<8} @ {sell_p:.2f}")
                    print(f"  {Colors.GREEN}EST. PROFIT: ${self.investment * (profit/100):.2f} (Lat: {latency:.1f}ms){Colors.ENDC}")
                    print("-" * 50)
                    time.sleep(2) # Pause to let the user see it
                else:
                    # Radar Scan Line (Overwrites itself)
                    # Show best spread found (even if negative)
                    spread_a = (price_sell_krk - price_buy_bin) / price_buy_bin * 100 if (price_buy_bin and price_sell_krk) else -99
                    spread_b = (price_sell_bin - price_buy_krk) / price_buy_krk * 100 if (price_buy_krk and price_sell_bin) else -99
                    best_spread = max(spread_a, spread_b)
                    
                    color = Colors.FAIL if best_spread < 0 else Colors.WARNING
                    status = f"{Colors.BLUE}SCANNING{Colors.ENDC}"
                    
                    sys.stdout.write(
                        f"\r{status} | {self.symbol} | "
                        f"Bin: {books['binance']['asks'][0][0]:.2f}/{books['binance']['bids'][0][0]:.2f} | "
                        f"Krk: {books['kraken']['asks'][0][0]:.2f}/{books['kraken']['bids'][0][0]:.2f} | "
                        f"Spread: {color}{best_spread:.3f}%{Colors.ENDC} | "
                        f"Lat: {latency:.0f}ms"
                    )
                    sys.stdout.flush()
                
                await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}[STOP] HFT Engine Halted.{Colors.ENDC}")
        finally:
            await self.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Inject artificial arbitrage opportunities")
    parser.add_argument("--asset", type=str, default="BTC/USDT", help="Trading pair")
    args = parser.parse_args()

    try:
        bot = HFTArbitrageBot(symbol=args.asset, simulate=args.simulate)
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        pass