from symbol.back_test import BackTestData
import pandas as pd

a = BackTestData(yf_symbol="BTC-USD")
a.set_period(pd.Timestamp("2022-07-07 12:34:00", tz="UTC"))
b = a.get_first()
c = a.get_range()
d = a.get_latest()
e = a.in_bars(pd.Timestamp("2022-07-07 12:30:00", tz="UTC"))
f = a.in_bars(pd.Timestamp("2022-07-07 12:35:00", tz="UTC"))

a.set_period(pd.Timestamp("2022-07-07 13:34:00", tz="UTC"))
h = a.in_bars(pd.Timestamp("2022-07-07 12:50:00", tz="UTC"))
i = a.in_bars(pd.Timestamp("2022-07-07 13:35:00", tz="UTC"))
print("asdas")
