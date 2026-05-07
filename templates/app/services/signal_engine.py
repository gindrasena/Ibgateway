
import pandas as pd
from .indicators import ema, atr, supertrend
from ..config import settings


def compute_signal(df: pd.DataFrame):
    df = df.copy()
    df['ema200'] = ema(df['close'], 200)
    df['atr14'] = atr(df, 14)
    st, direction = supertrend(df, 10, 3.0)
    df['st_dir'] = direction

    last = df.iloc[-1]
    px = float(last['close'])

    atr_v = float(last['atr14']) if pd.notna(last['atr14']) else 0.0
    if atr_v <= 0:
        return 'HOLD', px, px, px

    ema200 = float(last['ema200']) if pd.notna(last['ema200']) else px
    st_dir = int(last['st_dir']) if pd.notna(last['st_dir']) else 0

    if px > ema200 and st_dir == 1:
        if settings.allow_buy:
            return 'BUY', px, px - atr_v, px + 3 * atr_v
        return 'HOLD', px, px, px

    if px < ema200 and st_dir == -1:
        if settings.allow_sell:
            return 'SELL', px, px + atr_v, px - 3 * atr_v
        return 'HOLD', px, px, px

    return 'HOLD', px, px, px
