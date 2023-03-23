from symbol.symbol_data import SymbolData
from symbol.back_test import BackTestData
from math import floor, log10
from decimal import Decimal
import logging
from pandas import Timestamp

log = logging.getLogger(__name__)


class InvalidQuantity(Exception):
    ...


class InvalidPrice(Exception):
    ...


class Symbol:
    def __init__(
        self,
        yf_symbol: str,
        time_manager=None,
        min_quantity_increment: float = 1,
        min_quantity: float = 1,
        min_price_increment: float = 0.001,
        notional_units: bool = False,
        interval: str = "5m",
    ) -> None:
        self.yf_symbol = yf_symbol
        self.min_quantity_increment = min_quantity_increment
        self.min_quantity = min_quantity
        self.min_price_increment = Decimal(min_price_increment)
        self.notional_units = notional_units
        self.interval = interval
        self.time_manager = time_manager

        if time_manager and time_manager.back_test:

            # if back_testing:
            self.ohlc = BackTestData(
                yf_symbol=yf_symbol, interval=interval, time_manager=time_manager
            )
            # time_manager.add_symbol(self)
        else:
            self.ohlc = SymbolData(yf_symbol=yf_symbol, interval=interval)

    def __repr__(self) -> str:
        return self.yf_symbol

    def align_quantity(self, initial_quantity: float) -> float:
        aligned_quantity = Symbol._align_quantity(
            quantity=initial_quantity,
            increment=self.min_quantity,
            notional=self.notional_units,
        )

        if aligned_quantity < self.min_quantity:
            raise InvalidQuantity(
                f"Specified quantity of {initial_quantity} (aligned to "
                f"{aligned_quantity}) is less than minimum quantity for this symbol "
                f"of {self.min_quantity}"
            )

        return aligned_quantity

    def align_quantity_increment(self, incremental_quantity: float):
        aligned_quantity = Symbol._align_quantity(
            quantity=incremental_quantity,
            increment=self.min_quantity_increment,
            notional=self.notional_units,
        )

        if aligned_quantity < self.min_quantity:
            return self.min_quantity

        return aligned_quantity

    def _align_quantity(quantity: float, increment: float, notional: bool) -> float:
        mod_quantity = quantity % increment
        aligned_quantity = quantity - mod_quantity

        if notional:
            aligned_quantity = Symbol._hacky_float(aligned_quantity, increment)
        else:
            aligned_quantity = int(aligned_quantity)

        log.debug(
            f"Aligned quantity from {quantity} to {aligned_quantity} (increment {increment})"
        )
        return aligned_quantity

    def align_price(self, unit_price: float) -> float:
        dec_unit = Decimal(round(unit_price, 10))
        mod_unit = dec_unit % self.min_price_increment
        trimmed_unit = dec_unit - mod_unit
        aligned_price = Symbol._hacky_float(
            value=trimmed_unit, step_increment=self.min_price_increment
        )

        if aligned_price <= 0:
            raise ValueError(
                f"Align {unit_price} using {self.min_price_increment} resulted in non-sensical result of {aligned_price}"
            )

        log.debug(
            f"Aligned price from {unit_price} to {aligned_price} (increment {self.min_price_increment})"
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

    @property
    def period(self):
        return self.ohlc.period

    @period.setter
    def period(self, period: Timestamp):
        self.ohlc.period = period
