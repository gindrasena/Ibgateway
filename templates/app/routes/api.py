
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Signal
from ..config import settings

from ..services.market_data import get_bars_15m
from ..services.indicators import ema, atr, supertrend

router = APIRouter(prefix='/api', tags=['api'])


@router.get('/config')
def get_config():
    return {
        'symbols': settings.symbols_list,
        'allow_buy': settings.allow_buy,
        'allow_sell': settings.allow_sell,
        'timeframe': '15m',
        'outside_rth': True,
        'max_symbols': 20,
        'use_mock_data': bool(int(settings.USE_MOCK_DATA)),
    }


@router.get('/signals')
def latest_signals(limit: int = 20):
    """Return latest signals.

    Filters by SYMBOLS (if set in .env) and respects ALLOW_BUY/ALLOW_SELL.
    """
    if limit < 1 or limit > 20:
        raise HTTPException(status_code=400, detail='limit must be 1..20')

    db: Session = SessionLocal()

    # Pull more then filter to keep newest ordering when filtering
    rows = db.query(Signal).order_by(Signal.ts.desc()).limit(500).all()

    allowed = set(settings.symbols_list) if settings.symbols_list else None

    def _map(sig: str) -> str:
        if sig == 'BUY' and not settings.allow_buy:
            return 'HOLD'
        if sig == 'SELL' and not settings.allow_sell:
            return 'HOLD'
        return sig

    out = []
    for r in rows:
        sym = (r.symbol or '').upper()
        if allowed is not None and sym not in allowed:
            continue
        out.append(dict(symbol=sym, signal=_map(r.signal), entry=r.entry, stop=r.stop, target=r.target, ts=r.ts))
        if len(out) >= limit:
            break

    return out


@router.get('/chart/{symbol}')
def chart_data(symbol: str, bars: int = 240):
    symbol = symbol.upper().strip()
    if not symbol or len(symbol) > 12:
        raise HTTPException(status_code=400, detail='Invalid symbol')
    if bars < 60 or bars > 600:
        raise HTTPException(status_code=400, detail='bars must be 60..600')

    df = get_bars_15m(symbol, n=bars)
    df['ema200'] = ema(df['close'], 200)
    df['atr14'] = atr(df, 14)
    st, direction = supertrend(df, 10, 3.0)
    df['st'] = st
    df['st_dir'] = direction

    t = [x.isoformat() for x in df.index.to_pydatetime()]
    return {
        'symbol': symbol,
        'timeframe': '15m',
        't': t,
        'open': df['open'].round(4).tolist(),
        'high': df['high'].round(4).tolist(),
        'low': df['low'].round(4).tolist(),
        'close': df['close'].round(4).tolist(),
        'ema200': df['ema200'].round(4).where(df['ema200'].notna(), None).tolist(),
        'st': df['st'].round(4).where(df['st'].notna(), None).tolist(),
        'st_dir': df['st_dir'].fillna(0).astype(int).tolist(),
        'atr14': df['atr14'].round(4).where(df['atr14'].notna(), None).tolist(),
    }
