
# IBKR Signal Gateway v6 (US Stocks • Signal-only)

✅ US stocks only
✅ 15-minute timeframe
✅ Outside RTH (pre + post-market allowed)
✅ Max 20 symbols
✅ Signal-only (NO order placement)

## What’s new in v6
- `GET /api/signals` is now **filtered by `SYMBOLS`** from `.env` (same as dashboard)

## Configure
```bash
cp .env.example .env
```
Edit:
- `SYMBOLS=AAPL,MSFT,...` (max 20)
- `ALLOW_BUY=1/0`
- `ALLOW_SELL=1/0`

## Run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Open API (Swagger)
- http://127.0.0.1:8000/docs

## API examples
```bash
curl http://127.0.0.1:8000/api/config
curl "http://127.0.0.1:8000/api/signals?limit=20"
curl "http://127.0.0.1:8000/api/chart/AAPL?bars=240" | head
```

## Dashboard search
- http://127.0.0.1:8000/?q=AAPL
