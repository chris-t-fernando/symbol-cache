# TODO you need to solve for backtesting
# i think if you make a new class that inherits from SymbolData
# and overrides get_pause so the cache never invalidates
# and add a method to set the 'current' date and time
# and override the query methods, where you run super() then trim anything after the 'current' date and time
# finally, the logic in Symbol will need to be updated to be aware of backtesting, and which object to use
# of maybe inject it?

from symbol.symbol_data import SymbolData
import pandas as pd


class BackTest(SymbolData):
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
