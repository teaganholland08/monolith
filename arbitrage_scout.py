import urllib.request
import json
import time

class ArbitrageHunter:
    def __init__(self):
        self.pairs = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        self.binance_url = "https://api.binance.com/api/v3/ticker/price?symbol="
        self.kraken_url = "https://api.kraken.com/0/public/Ticker?pair="

        # Kraken uses slightly different symbols
        self.kraken_symbols = {"BTCUSDT": "XBTUSDT", "ETHUSDT": "ETHUSDT", "SOLUSDT": "SOLUSDT"}

    def get_binance_price(self, symbol):
        try:
            req = urllib.request.Request(self.binance_url + symbol)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                return float(data['price'])
        except Exception as e:
            return None

    def get_kraken_price(self, symbol):
        kraken_sym = self.kraken_symbols.get(symbol)
        if not kraken_sym: return None
        try:
            req = urllib.request.Request(self.kraken_url + kraken_sym)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                # Kraken returns a complex nested dict, e.g. data['result']['XBTUSDT']['c'][0]
                result_key = list(data['result'].keys())[0]
                return float(data['result'][result_key]['c'][0])
        except Exception as e:
            return None

    def scan(self):
        print("\n[GLOBAL SCANNER] Initiating Arbitrage Hunter across Binance & Kraken...")
        print("-" * 60)
        
        found_opportunity = False
        
        for pair in self.pairs:
            binance_price = self.get_binance_price(pair)
            kraken_price = self.get_kraken_price(pair)

            if binance_price and kraken_price:
                diff = abs(binance_price - kraken_price)
                margin = (diff / min(binance_price, kraken_price)) * 100

                print(f"[*] {pair} | Binance: ${binance_price:,.2f} | Kraken: ${kraken_price:,.2f}")
                
                if margin > 0.15: # 0.15% is typically enough to cover exchange fees
                    print(f"    [!] PROFIT OPPORTUNITY DETECTED: {margin:.3f}% spread (${diff:,.2f})")
                    found_opportunity = True
                else:
                    print(f"    [-] Spread: {margin:.3f}% (${diff:,.2f}) - Too low for safe execution.")
            time.sleep(1) # Rate limit respect
            
        print("-" * 60)
        if found_opportunity:
            print("[+] Scan complete. Actionable arbitrage paths found.")
        else:
            print("[-] Scan complete. Markets are highly efficient right now. Re-scanning recommended.")

if __name__ == "__main__":
    hunter = ArbitrageHunter()
    hunter.scan()
