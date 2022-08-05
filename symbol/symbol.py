from symbol.symbol_data import SymbolData
from symbol.back_test import BackTestData
from math import floor, log10
from decimal import Decimal
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
        notional_units: bool = False,
        interval: str = "5m",
        back_testing: bool = False,
    ) -> None:
        self.yf_symbol = yf_symbol
        self.alp_symbol = alp_symbol
        self.min_quantity_increment = min_quantity_increment
        self.min_quantity = min_quantity
        self.min_price_increment = Decimal(min_price_increment)
        self.notional_units = notional_units
        self.interval = interval

        if back_testing:
            self.ohlc = BackTestData(yf_symbol=yf_symbol, interval=interval)
        else:
            self.ohlc = SymbolData(yf_symbol=yf_symbol, interval=interval)

    def __repr__(self) -> str:
        return self.yf_symbol

    def align_quantity(self, initial_quantity: float) -> float:
        return Symbol._align_quantity(
            quantity=initial_quantity, increment=self.min_quantity, notional=self.notional_units
        )

    def align_quantity_increment(self, incremental_quantity: float):
        return Symbol._align_quantity(
            quantity=incremental_quantity,
            increment=self.min_quantity_increment,
            notional=self.notional_units,
        )

    def _align_quantity(quantity: float, increment: float, notional: bool) -> float:
        mod_quantity = quantity % increment
        quantity = quantity - mod_quantity

        if notional:
            return Symbol._hacky_float(quantity, increment)
        else:
            return int(quantity)

    def align_price(self, unit_price: float) -> float:
        dec_unit = Decimal(unit_price)
        mod_unit = dec_unit % self.min_price_increment
        trimmed_unit = dec_unit - mod_unit
        aligned_price = Symbol._hacky_float(
            value=trimmed_unit, step_increment=self.min_price_increment
        )

        if aligned_price <= 0:
            raise ValueError(
                f"Align {unit_price} using {self.min_price_increment} resulted in non-sensical result of {aligned_price}"
            )

        return aligned_price

    def _hacky_float(value: Decimal, step_increment: float) -> float:
        # lord forgive me for my sins
        string_dec = str(value)
        dot_at = string_dec.find(".") + 1
        if dot_at == 0:
            # there isn't a . in the decimal
            return float(value)

        # works out precision based on min_price_increment size
        precision = abs(int(log10(abs(step_increment))))
        truncate_at = dot_at + precision
        truncated_string = string_dec[:truncate_at]
        float_value = float(truncated_string)

        return float_value
