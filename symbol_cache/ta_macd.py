import pandas as pd
from dateutil import relativedelta
import btalib
import numpy as np


class MacdTA:
    __tabot_strategy__: bool = True

    class MacdColumns:
        df: pd.DataFrame

        def __init__(self, df: pd.DataFrame) -> None:
            self.df = df

    def get_interval_settings(interval):
        minutes_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m"]
        max_period = {
            "1m": 6,
            "2m": 59,
            "5m": 59,
            "15m": 59,
            "30m": 59,
            "60m": 500,
            "90m": 59,
        }

        if interval in minutes_intervals:
            return (
                relativedelta(minutes=int(interval[:-1])),
                relativedelta(days=max_period[interval]),
            )
        else:
            raise ValueError(f"Interval {interval} is not implemented")

    def do_ta(ohlc_data: pd.DataFrame):
        # def __init__(self, ohlc_data, interval="5m"):
        btadf = btalib.macd(ohlc_data).df

        # change names to avoid collision
        df = btadf.rename(
            columns={
                "macd": "macd_macd",
                "signal": "macd_signal",
                "histogram": "macd_histogram",
            }
        )

        df = df.assign(
            macd_crossover=False,
            # macd_signal_crossover=False,
            macd_above_signal=False,
            macd_cycle="red",
        )

        # signal here means MA26
        # macd here means MA12
        # so macd_above_signal means MA12 above MA26
        df["macd_above_signal"] = np.where(
            df["macd_macd"] > df["macd_signal"], True, False
        )
        # blue means MA12 is above MA26
        df["macd_cycle"] = np.where(df["macd_macd"] > df["macd_signal"], "blue", "red")
        # crossover happens when MA12 crosses over MA26
        df["macd_crossover"] = df.macd_above_signal.ne(df.macd_above_signal.shift())

        return MacdTA.MacdColumns(df)
