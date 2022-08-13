from distutils.core import setup

setup(
    name="symbol_cache",
    version="0.28",
    description="Stock ohlc data caching",
    author="Chris Fernando",
    author_email="chris.t.fernando@gmail.com",
    url="https://github.com/chris-t-fernando/symbol-cache",
    packages=["symbol"],
    install_requires=["numpy", "pandas", "yfinance"],
)
