import pandas as pd

def calculate_ema(ohlc_df, period=20):
    ema_series = ohlc_df['Close'].ewm(span=period, adjust=False).mean()
    ema_df = pd.DataFrame({'Time': ohlc_df.index, 'EMA_20': ema_series})
    return ema_df.set_index('Time')