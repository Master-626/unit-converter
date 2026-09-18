"""
Core unit conversion logic.
"""


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

    # Weight units (base: kilograms)
    weight_units = {
        "mg": 0.000001,
        "g": 0.001,
        "kg": 1.0,
        "oz": 0.0283495,
        "lb": 0.453592,
        "ton": 1000.0,
    }

    # Volume units (base: liters)
    volume_units = {
        "ml": 0.001,
        "l": 1.0,
        "gal": 3.78541,
        "qt": 0.946353,
        "pt": 0.473176,
        "cup": 0.236588,
        "floz": 0.0295735,
    }

    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert length from one unit to another."""
        meters = value * self.length_units[from_unit]
        result = meters / self.length_units[to_unit]
        return round(result, 6)

    def convert_weight(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert weight from one unit to another."""
        kg = value * self.weight_units[from_unit]
        result = kg / self.weight_units[to_unit]
        return round(result, 6)

    def convert_volume(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert volume from one unit to another."""
        liters = value * self.volume_units[from_unit]
        result = liters / self.volume_units[to_unit]
        return round(result, 6)

    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between Celsius, Fahrenheit, Kelvin."""
        # First convert to Celsius
        if from_unit == "c":
            celsius = value
        elif from_unit == "f":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "k":
            celsius = value - 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {from_unit}")

        # Then convert to target
        if to_unit == "c":
            result = celsius
        elif to_unit == "f":
            result = celsius * 9 / 5 + 32
        elif to_unit == "k":
            result = celsius + 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {to_unit}")

        return round(result, 2)

    def list_units(self, category: str) -> list:
        """List available units for a category."""
        if category == "length":
            return list(self.length_units.keys())
        elif category == "weight":
            return list(self.weight_units.keys())
        elif category == "volume":
            return list(self.volume_units.keys())
        elif category == "temperature":
            return ["c", "f", "k"]
        else:
            raise ValueError(f"Unknown category: {category}")
