import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self, target_profit=2000, strike_count=5, strike_step=50):
        self.target_profit = target_profit
        self.strike_count = strike_count
        self.strike_step = strike_step
        self.small_body_pct = 0.05

    def calculate_indicators(self, df):
        # 1. EMAs and SMAs
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA9'] = df['close'].rolling(window=9).mean()
        
        # 2. ATR Calculation (Manual)
        high_low = df['high'] - df['low']
        high_cp = np.abs(df['high'] - df['close'].shift())
        low_cp = np.abs(df['low'] - df['close'].shift())
        df['TR'] = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
        df['ATR'] = df['TR'].rolling(window=14).mean()

        # 3. ADX Calculation (Manual Wilder's Method)
        plus_dm = df['high'].diff()
        minus_dm = df['low'].diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        minus_dm = np.abs(minus_dm)

        tr_smooth = df['TR'].rolling(window=14).mean()
        plus_di = 100 * (plus_dm.rolling(window=14).mean() / tr_smooth)
        minus_di = 100 * (minus_dm.rolling(window=14).mean() / tr_smooth)
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        df['ADX'] = dx.rolling(window=14).mean()

        # 4. Consolidation Logic
        df['is_consolidating'] = (df['high'] - df['low']).rolling(5).mean() < df['ATR']
        return df

    def check_signal(self, df):
        if len(df) < 20: return "WAIT"
        last = df.iloc[-1]
        body_pct = (abs(last['open'] - last['close']) / last['close']) * 100
        
        touches_ma = last['low'] <= last['MA20'] <= last['high']
        strong_trend = last['ADX'] > 25
        is_small = body_pct < self.small_body_pct
        
        if touches_ma and strong_trend and is_small and not last['is_consolidating']:
            if last['close'] > last['MA20']: return "BUY_CE"
            if last['close'] < last['MA20']: return "BUY_PE"
        return "WAIT"

    def get_ladder_strikes(self, spot, signal_type):
        atm = round(spot / self.strike_step) * self.strike_step
        strikes = []
        for i in range(1, self.strike_count + 1):
            offset = i * self.strike_step
            strikes.append(atm - offset if "CE" in signal_type else atm + offset)
        return strikes
