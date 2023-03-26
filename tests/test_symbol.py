import pytest
from symbol_cache.symbol import Symbol, SymbolData


def test_symbol_price():
    s = Symbol(yf_symbol="BTC-USD")
    aligned_price = s.align_price(50.4764754531)
    assert aligned_price == 50.476


def test_symbol_quantity():
    s = Symbol(yf_symbol="BTC-USD", alp_symbol="BTC/USD")
    aligned_price = s.align_quantity(50.4764754531)
    assert aligned_price == 50


def test_symbol_quantity_increment_notional():
    s = Symbol(
        yf_symbol="BTC-USD",
        alp_symbol="BTC/USD",
        min_quantity_increment=0.1,
        notional_units=True,
    )
    aligned_price = s.align_quantity_increment(50.4764754531)
    assert aligned_price == 50.4


def test_symbol_quantity_increment():
    s = Symbol(yf_symbol="BTC-USD", alp_symbol="BTC/USD", min_quantity_increment=10)
    aligned_price = s.align_quantity_increment(56)
    assert aligned_price == 50
