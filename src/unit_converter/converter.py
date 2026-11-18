"""
Core unit conversion logic.
"""

import math
from decimal import ROUND_HALF_UP, Decimal

# International avoirdupois pound (exact since 1959). The ounce is 1/16 pound,
# so 16 oz converts back to 1 lb instead of drifting from a truncated constant.
_POUND_KG = 0.45359237

# US liquid gallon is exactly 231 cubic inches. Quarts, pints, cups, and fluid
# ounces are power-of-two subdivisions, so ratios such as 1 gal = 4 qt stay exact.
_US_GALLON_LITERS = 231 * (0.0254 ** 3) * 1000

_KELVIN_OFFSET = 273.15
_ABSOLUTE_ZERO_TOLERANCE = 1e-9


def _expand_aliases(units, extra):
    """Map canonical symbols and accepted spellings onto canonical symbols."""
    mapping = {name: name for name in units}
    unknown = [target for target in extra.values() if target not in mapping]
    if unknown:
        raise RuntimeError(f"Alias targets are not known units: {unknown}")
    mapping.update(extra)
    return mapping


def _normalize_token(unit):
    cleaned = unit.strip().lower()
    for char in ("°", "º", " ", "_", "-", "."):
        cleaned = cleaned.replace(char, "")
    return cleaned


def _require_real(value, label):
    """Reject booleans, non-numbers, NaN, and infinities."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        got = type(value).__name__
        raise ValueError(f"{label} value must be a real number, got {got}")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} value must be finite, got {value!r}")
    return number


def _resolve_unit(unit, aliases, kind):
    if not isinstance(unit, str):
        got = type(unit).__name__
        raise ValueError(f"{kind} unit must be a string, got {got}")
    key = _normalize_token(unit)
    if not key or key not in aliases:
        known = ", ".join(dict.fromkeys(aliases.values()))
        raise ValueError(f"Unknown {kind} unit: {unit!r}. Known units: {known}")
    return aliases[key]


def _round_temperature(value):
    """Round to 2 decimal places on the decimal value, half away from zero.

    Built-in ``round`` uses binary floats, so ``round(2.675, 2)`` is ``2.67``
    even though the decimal value 2.675 rounds to 2.68.
    """
    quantized = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(quantized)


_CATEGORY_ALIASES = {
    "length": "length",
    "weight": "weight",
    "mass": "weight",
    "volume": "volume",
    "temperature": "temperature",
    "temp": "temperature",
}


class UnitConverter:
    """Convert between different units of measurement."""

    # Length units (base: meters)
    length_units = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    }

    # Weight units (base: kilograms). "ton" is the metric ton (tonne).
    weight_units = {
        "mg": 0.000001,
        "g": 0.001,
        "kg": 1.0,
        "oz": _POUND_KG / 16,
        "lb": _POUND_KG,
        "ton": 1000.0,
    }

    # Volume units (base: liters). Gallons and smaller units are US liquid measure.
    volume_units = {
        "ml": 0.001,
        "l": 1.0,
        "gal": _US_GALLON_LITERS,
        "qt": _US_GALLON_LITERS / 4,
        "pt": _US_GALLON_LITERS / 8,
        "cup": _US_GALLON_LITERS / 16,
        "floz": _US_GALLON_LITERS / 128,
    }

    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert length from one unit to another."""
        return self._convert_linear(
            value, from_unit, to_unit, self.length_units, _LENGTH_ALIASES, "length"
        )

    def convert_weight(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert weight from one unit to another."""
        return self._convert_linear(
            value, from_unit, to_unit, self.weight_units, _WEIGHT_ALIASES, "weight"
        )

    def convert_volume(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert volume from one unit to another."""
        return self._convert_linear(
            value, from_unit, to_unit, self.volume_units, _VOLUME_ALIASES, "volume"
        )

    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
        number = _require_real(value, "Temperature")
        src = _resolve_unit(from_unit, _TEMP_ALIASES, "temperature")
        dst = _resolve_unit(to_unit, _TEMP_ALIASES, "temperature")

        if src == "c":
            celsius = number
        elif src == "f":
            celsius = (number - 32) * 5 / 9
        else:
            celsius = number - _KELVIN_OFFSET

        if celsius < -_KELVIN_OFFSET - _ABSOLUTE_ZERO_TOLERANCE:
            raise ValueError(
                f"Temperature {value} {from_unit} is below absolute zero (0 K)"
            )

        if dst == "c":
            result = celsius
        elif dst == "f":
            result = celsius * 9 / 5 + 32
        else:
            result = celsius + _KELVIN_OFFSET

        return _round_temperature(result)

    def convert_all(self, value: float, from_unit: str, category: str) -> dict:
        """Convert ``value`` into every unit of ``category``.

        Keys are canonical symbols in ``list_units`` order. Each value matches
        the corresponding single-unit method, including rounding.
        """
        normalized = self._normalize_category(category)
        convert = {
            "length": self.convert_length,
            "weight": self.convert_weight,
            "volume": self.convert_volume,
            "temperature": self.convert_temperature,
        }[normalized]
        return {
            unit: convert(value, from_unit, unit) for unit in self.list_units(normalized)
        }

    def list_units(self, category: str) -> list:
        """List available units for a category."""
        normalized = self._normalize_category(category)
        if normalized == "length":
            return list(self.length_units)
        if normalized == "weight":
            return list(self.weight_units)
        if normalized == "volume":
            return list(self.volume_units)
        return ["c", "f", "k"]

    def _normalize_category(self, category):
        if not isinstance(category, str):
            raise ValueError(f"Unknown category: {category}")
        key = category.strip().lower()
        normalized = _CATEGORY_ALIASES.get(key)
        if normalized is None:
            known = "length, weight, volume, temperature"
            raise ValueError(f"Unknown category: {category}. Known categories: {known}")
        return normalized

    @staticmethod
    def _convert_linear(value, from_unit, to_unit, factors, aliases, kind):
        number = _require_real(value, kind.capitalize())
        src = _resolve_unit(from_unit, aliases, kind)
        dst = _resolve_unit(to_unit, aliases, kind)
        return round(number * factors[src] / factors[dst], 6)


_LENGTH_ALIASES = _expand_aliases(
    UnitConverter.length_units,
    {
        "millimeter": "mm",
        "millimeters": "mm",
        "millimetre": "mm",
        "millimetres": "mm",
        "centimeter": "cm",
        "centimeters": "cm",
        "centimetre": "cm",
        "centimetres": "cm",
        "meter": "m",
        "meters": "m",
        "metre": "m",
        "metres": "m",
        "kilometer": "km",
        "kilometers": "km",
        "kilometre": "km",
        "kilometres": "km",
        "inch": "in",
        "inches": "in",
        "foot": "ft",
        "feet": "ft",
        "yard": "yd",
        "yards": "yd",
        "mile": "mi",
        "miles": "mi",
    },
)

_WEIGHT_ALIASES = _expand_aliases(
    UnitConverter.weight_units,
    {
        "milligram": "mg",
        "milligrams": "mg",
        "gram": "g",
        "grams": "g",
        "kilogram": "kg",
        "kilograms": "kg",
        "kgs": "kg",
        "ounce": "oz",
        "ounces": "oz",
        "pound": "lb",
        "pounds": "lb",
        "lbs": "lb",
        "tonne": "ton",
        "tonnes": "ton",
        "t": "ton",
        "metricton": "ton",
        "metrictonne": "ton",
    },
)

_VOLUME_ALIASES = _expand_aliases(
    UnitConverter.volume_units,
    {
        "milliliter": "ml",
        "milliliters": "ml",
        "millilitre": "ml",
        "millilitres": "ml",
        "liter": "l",
        "liters": "l",
        "litre": "l",
        "litres": "l",
        "gallon": "gal",
        "gallons": "gal",
        "quart": "qt",
        "quarts": "qt",
        "pint": "pt",
        "pints": "pt",
        "cups": "cup",
        "fluidounce": "floz",
        "fluidounces": "floz",
        "fluidoz": "floz",
    },
)

_TEMP_ALIASES = _expand_aliases(
    ("c", "f", "k"),
    {
        "celsius": "c",
        "centigrade": "c",
        "degc": "c",
        "fahrenheit": "f",
        "degf": "f",
        "kelvin": "k",
        "degk": "k",
    },
)
