import pytest
from unit_converter.converter import UnitConverter


def test_length_conversion():
    """Test length conversion."""
    conv = UnitConverter()
    assert conv.convert_length(1, "m", "cm") == 100
    assert conv.convert_length(1000, "m", "km") == 1
    assert conv.convert_length(1, "mi", "km") == 1.609344


def test_weight_conversion():
    """Test weight conversion."""
    conv = UnitConverter()
    assert conv.convert_weight(1, "kg", "g") == 1000
    assert conv.convert_weight(1, "lb", "kg") == 0.453592


def test_temperature_conversion():
    """Test temperature conversion."""
    conv = UnitConverter()
    assert conv.convert_temperature(0, "c", "f") == 32.0
    assert conv.convert_temperature(100, "c", "f") == 212.0
    assert conv.convert_temperature(32, "f", "c") == 0.0


def test_volume_conversion():
    """Test volume conversion."""
    conv = UnitConverter()
    assert conv.convert_volume(1, "l", "ml") == 1000
    assert conv.convert_volume(1, "gal", "l") == 3.78541


def test_list_units():
    """Test listing available units."""
    conv = UnitConverter()
    length_units = conv.list_units("length")
    assert "m" in length_units
    assert "km" in length_units
