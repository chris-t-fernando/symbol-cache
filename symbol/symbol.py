from symbol.symbol_data import SymbolData
from symbol.back_test import BackTestData
import logging

log = logging.getLogger(__name__)


class Symbol:
    def __init__(
        self,
        yf_symbol: str,
        alp_symbol: str,
        min_quantity_increment: float = 1,
        min_quantity: float = 1,
        min_price_increment: float = 0.001,
        interval: str = "5m",
        back_testing: bool = False,
    ) -> None:
        self.yf_symbol = yf_symbol
        self.alp_symbol = alp_symbol
        self.min_quantity_increment = min_quantity_increment
        self.min_quantity = min_quantity
        self.min_price_increment = min_price_increment
        self.interval = interval

        if back_testing:
            self.ohlc = BackTestData(yf_symbol=yf_symbol, interval=interval)
        else:
            self.ohlc = SymbolData(yf_symbol=yf_symbol, interval=interval)

    def __repr__(self) -> str:
        return self.yf_symbol
