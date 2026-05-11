import pandas_ta as ta
import pandas as pd

class TradingStrategy:
    def __init__(self, target_profit=2000, strike_count=5, strike_step=50):
        self.target_profit = target_profit
        self.strike_count = strike_count
        self.strike_step = strike_step
        self.small_body_pct = 0.05

    def calculate_indicators(self, df):
        df['MA20'] = ta.sma(df['close'], length=20)
        df['MA9'] = ta.sma(df['close'], length=9)
        adx = ta.adx(df['high'], df['low'], df['close'], length=14)
        df = pd.concat([df, adx], axis=1)
        # Consolidation: ATR comparison
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        df['is_consolidating'] = (df['high'] - df['low']).rolling(5).mean() < df['ATR']
        return df

    def check_signal(self, df):
        last = df.iloc[-1]
        body_pct = (abs(last['open'] - last['close']) / last['close']) * 100
        
        touches_ma = last['low'] <= last['MA20'] <= last['high']
        strong_trend = last['ADX_14'] > 25
        is_small = body_pct < self.small_body_pct
        
        if touches_ma and strong_trend and is_small and not last['is_consolidating']:
            if last['close'] > last['MA20']: return "BUY_CE"
            if last['close'] < last['MA20']: return "BUY_PE"
        return "WAIT"

    def get_ladder_strikes(self, spot, signal_type):
        atm = round(spot / self.strike_step) * self.strike_step
        strikes = []
        for i in range(1, self.strike_count + 1):
            if signal_type == "BUY_CE":
                strikes.append(atm - (i * self.strike_step)) # ITM is below for CE
            else:
                strikes.append(atm + (i * self.strike_step)) # ITM is above for PE
        return strikes
