from symbol.symbol_data import SymbolData
import pandas as pd


class BackTestData(SymbolData):
    def __init__(self, yf_symbol: str, time_manager, interval: str = "5m"):
        super().__init__(yf_symbol, interval)
        self._time_manager = time_manager

    def get_pause(interval: str) -> int:
        # causes the cache to never invalidate
        return 999999999

    #def get_first(self):
    #    result = super().get_first()
    #    if result.name > self.period:
    #        return
    #    return result

    @property
    def period(self):
        return self._time_manager.now

    def get_range(self, start: pd.Timestamp = None, end: pd.Timestamp = None):
        result = super().get_range(start, end)
        result = result[: self.period]
        return result

    def get_latest(self):
        result = super().get_range()
        result = result[: self.period]
        return result.iloc[-1]

    def in_bars(self, timestamp: pd.Timestamp):
        result = super().get_range()
        result = result[: self.period]
        return timestamp in result.index
