
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Signal
from ..config import settings

router = APIRouter(tags=['ui'])

templates = Jinja2Templates(directory='templates')


def _symbols_from_db(rows) -> list[str]:
    out = []
    seen = set()
    for r in rows:
        if r.symbol and r.symbol not in seen:
            seen.add(r.symbol)
            out.append(r.symbol)
    return out


def _apply_filter(rows, allowed: list[str], q: str | None):
    qn = (q or '').strip().upper()
    allowed_set = set([s.upper() for s in allowed]) if allowed else None
    filtered = []
    for r in rows:
        sym = (r.symbol or '').upper()
        if allowed_set is not None and sym not in allowed_set:
            continue
        if qn and qn not in sym:
            continue
        filtered.append(r)
    return filtered


@router.get('/')
def dashboard(request: Request, q: str | None = None):
    db: Session = SessionLocal()
    rows = db.query(Signal).order_by(Signal.ts.desc()).limit(200).all()

    symbols = settings.symbols_list or _symbols_from_db(rows)
    filtered_rows = _apply_filter(rows, settings.symbols_list, q)

    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'signals': filtered_rows,
        'symbols': symbols,
        'allow_buy': settings.allow_buy,
        'allow_sell': settings.allow_sell,
        'q': (q or '').strip(),
        'filtered': bool(settings.symbols_list),
    })


@router.get('/chart/{symbol}')
def chart_view(request: Request, symbol: str):
    symbol = symbol.upper().strip()
    symbols = settings.symbols_list
    return templates.TemplateResponse('chart.html', {
        'request': request,
        'symbol': symbol,
        'symbols': symbols or [symbol],
        'allow_buy': settings.allow_buy,
        'allow_sell': settings.allow_sell,
    })
