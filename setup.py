from distutils.core import setup

from setuptools import find_packages

setup(
    name="symbol_cache",
    version="0.47",
    description="Stock ohlc data caching",
    author="Chris Fernando",
    author_email="chris.t.fernando@gmail.com",
    url="https://github.com/chris-t-fernando/symbol-cache",
    packages=find_packages(exclude=("tests",)),
    install_requires=["numpy", "pandas", "yfinance", "bta-lib"],
)
