
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_symbols(csv: str) -> list[str]:
    if not csv:
        return []
    parts = [p.strip().upper() for p in csv.replace('
', ',').split(',')]
    syms = [p for p in parts if p]
    out = []
    seen = set()
    for s in syms:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out[:20]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    APP_NAME: str = 'IBKR Signal Gateway'
    DB_URL: str = 'sqlite:///./data/app.db'
    USE_MOCK_DATA: int = 1

    SYMBOLS: str = ''
    ALLOW_BUY: int = 1
    ALLOW_SELL: int = 1

    IBKR_HOST: str = '127.0.0.1'
    IBKR_PORT: int = 7496
    IBKR_CLIENT_ID: int = 12

    @property
    def symbols_list(self) -> list[str]:
        return _parse_symbols(self.SYMBOLS)

    @property
    def allow_buy(self) -> bool:
        return bool(int(self.ALLOW_BUY))

    @property
    def allow_sell(self) -> bool:
        return bool(int(self.ALLOW_SELL))


settings = Settings()
