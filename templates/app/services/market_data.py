
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from ..config import settings


def get_bars_15m(symbol: str, n: int = 240) -> pd.DataFrame:
    if settings.USE_MOCK_DATA:
        return _mock_bars(symbol, n)
    return _mock_bars(symbol, n)


def _mock_bars(symbol: str, n: int) -> pd.DataFrame:
    seed = abs(hash(symbol.upper())) % (2**32)
    rng = np.random.default_rng(seed)

    now = datetime.now(timezone.utc)
    minutes = (now.minute // 15) * 15
    aligned = now.replace(minute=minutes, second=0, microsecond=0)
    idx = [aligned - timedelta(minutes=15*i) for i in range(n)][::-1]

    base = 50 + (seed % 350) / 10.0
    steps = rng.normal(0, 0.45, size=n).cumsum()
    close = np.maximum(base + steps, 1.0)

    open_ = np.r_[close[0], close[:-1]]
    spread = rng.uniform(0.05, 1.0, size=n)
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread

    df = pd.DataFrame({'open': open_, 'high': high, 'low': low, 'close': close}, index=pd.to_datetime(idx))
    df.index.name = 'time'
    return df
