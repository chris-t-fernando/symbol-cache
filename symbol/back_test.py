from symbol.symbol_data import SymbolData
import pandas as pd


class BackTestData(SymbolData):
    def get_pause(interval: str) -> int:
        # causes the cache to never invalidate
        return 999999999

    def set_period(self, period: pd.Timestamp):
        self.period = period

    def get_first(self):
        result = super().get_first()
        if result.name > self.period:
            return

        return result

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
