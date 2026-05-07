
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0):
    df = df.copy()
    _atr = atr(df, period)
    hl2 = (df['high'] + df['low']) / 2.0
    basic_upper = hl2 + multiplier * _atr
    basic_lower = hl2 - multiplier * _atr

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()

    for i in range(1, len(df)):
        if pd.notna(final_upper.iloc[i-1]) and pd.notna(basic_upper.iloc[i]):
            if basic_upper.iloc[i] < final_upper.iloc[i-1] or df['close'].iloc[i-1] > final_upper.iloc[i-1]:
                final_upper.iloc[i] = basic_upper.iloc[i]
            else:
                final_upper.iloc[i] = final_upper.iloc[i-1]

        if pd.notna(final_lower.iloc[i-1]) and pd.notna(basic_lower.iloc[i]):
            if basic_lower.iloc[i] > final_lower.iloc[i-1] or df['close'].iloc[i-1] < final_lower.iloc[i-1]:
                final_lower.iloc[i] = basic_lower.iloc[i]
            else:
                final_lower.iloc[i] = final_lower.iloc[i-1]

    direction = pd.Series(index=df.index, dtype='int64')
    st = pd.Series(index=df.index, dtype='float64')

    direction.iloc[0] = 1
    st.iloc[0] = final_lower.iloc[0]

    for i in range(1, len(df)):
        prev_dir = direction.iloc[i-1]
        if prev_dir == 1:
            direction.iloc[i] = -1 if df['close'].iloc[i] < final_lower.iloc[i] else 1
        else:
            direction.iloc[i] = 1 if df['close'].iloc[i] > final_upper.iloc[i] else -1
        st.iloc[i] = final_lower.iloc[i] if direction.iloc[i] == 1 else final_upper.iloc[i]

    return st, direction
