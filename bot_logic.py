import alpaca_trade_api as tradeapi
import pandas as pd
import time

class TradingBot:
    def __init__(self, api_key, api_secret, symbol, profit_target, stop_loss):
        self.api = tradeapi.REST(api_key, api_secret, base_url='https://paper-api.alpaca.markets')
        self.symbol = symbol.upper()
        self.profit_target = profit_target / 100
        self.stop_loss = stop_loss / 100

    def get_bars(self):
        # Fetch recent 5-minute bars (limit 50)
        bars = self.api.get_bars(self.symbol, tradeapi.TimeFrame(5, tradeapi.TimeFrameUnit.Minute), limit=50).df

        # Filter bars for the symbol only, since get_bars returns all symbols if multiple requested
        df = bars[bars['symbol'] == self.symbol].copy()

        # Rename columns for consistency
        df.rename(columns={'t':'t', 'o':'o', 'h':'h', 'l':'l', 'c':'c', 'v':'v'}, inplace=True)
        return df

    def check_dip_buy(self, df):
        # Simple logic: buy if last candle closes below MA20
        df['MA20'] = df['c'].rolling(window=20).mean()
        last_close = df['c'].iloc[-1]
        last_ma20 = df['MA20'].iloc[-1]
        return last_close < last_ma20

    def run(self):
        while True:
            df = self.get_bars()
            if self.check_dip_buy(df):
                qty = 1  # fixed quantity for demo
                last_price = df['c'].iloc[-1]
                take_profit = round(last_price * (1 + self.profit_target), 2)
                stop_loss = round(last_price * (1 - self.stop_loss), 2)

                try:
                    self.api.submit_order(
                        symbol=self.symbol,
                        qty=qty,
                        side='buy',
                        type='limit',
                        time_in_force='gtc',
                        order_class='bracket',
                        limit_price=last_price,
                        take_profit={'limit_price': take_profit},
                        stop_loss={'stop_price': stop_loss}
                    )
                    print(f"Bought {qty} {self.symbol} at {last_price}, TP={take_profit}, SL={stop_loss}")
                    break  # only one trade for demo
                except Exception as e:
                    print(f"Order error: {e}")
            time.sleep(60)
