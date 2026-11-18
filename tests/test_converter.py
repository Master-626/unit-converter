import pytest

from unit_converter.converter import UnitConverter


def test_length_conversion():
    """Test length conversion."""
    conv = UnitConverter()
    assert conv.convert_length(1, "m", "cm") == 100
    assert conv.convert_length(1000, "m", "km") == 1
    assert conv.convert_length(1, "mi", "km") == 1.609344
    assert conv.convert_length(1, "ft", "in") == 12
    assert conv.convert_length(1, "mi", "ft") == 5280
    assert conv.convert_length(1, "yd", "ft") == 3
    assert conv.convert_length(1, "in", "cm") == 2.54


def test_weight_conversion():
    """Test weight conversion."""
    conv = UnitConverter()
    assert conv.convert_weight(1, "kg", "g") == 1000
    # 6-decimal display of the exact international pound, 0.45359237 kg.
    assert conv.convert_weight(1, "lb", "kg") == 0.453592
    assert conv.convert_weight(1, "kg", "lb") == 2.204623
    assert conv.convert_weight(1, "oz", "g") == 28.349523
    assert conv.convert_weight(16, "oz", "lb") == 1
    assert conv.convert_weight(2, "lb", "kg") == 0.907185
    assert conv.convert_weight(1000, "lb", "kg") == 453.59237
    assert conv.convert_weight(1, "ton", "kg") == 1000


def test_temperature_conversion():
    """Test temperature conversion."""
    conv = UnitConverter()
    assert conv.convert_temperature(0, "c", "f") == 32.0
    assert conv.convert_temperature(100, "c", "f") == 212.0
    assert conv.convert_temperature(32, "f", "c") == 0.0
    assert conv.convert_temperature(0, "c", "k") == 273.15
    assert conv.convert_temperature(0, "k", "c") == -273.15
    assert conv.convert_temperature(0, "k", "f") == -459.67
    assert conv.convert_temperature(-40, "c", "f") == -40.0
    assert conv.convert_temperature(-459.67, "f", "k") == 0.0
    assert conv.convert_temperature(0, "f", "c") == -17.78


def test_temperature_rounds_decimal_halves():
    """Binary round() mis-rounds several exact hundredths."""
    conv = UnitConverter()
    assert conv.convert_temperature(2.675, "c", "c") == 2.68
    assert conv.convert_temperature(1.005, "c", "c") == 1.01
    assert conv.convert_temperature(-1.005, "c", "c") == -1.01


def test_volume_conversion():
    """Test volume conversion."""
    conv = UnitConverter()
    assert conv.convert_volume(1, "l", "ml") == 1000
    assert conv.convert_volume(1, "gal", "l") == 3.785412


def test_us_volume_units_keep_exact_ratios():
    """US liquid units are exact subdivisions of the gallon."""
    conv = UnitConverter()
    assert conv.convert_volume(1, "gal", "qt") == 4
    assert conv.convert_volume(1, "gal", "pt") == 8
    assert conv.convert_volume(1, "gal", "cup") == 16
    assert conv.convert_volume(1, "gal", "floz") == 128
    assert conv.convert_volume(4, "qt", "gal") == 1
    assert conv.convert_volume(1, "qt", "pt") == 2
    assert conv.convert_volume(1, "pt", "cup") == 2
    assert conv.convert_volume(1, "cup", "floz") == 8
    assert conv.convert_volume(128, "floz", "gal") == 1
    assert conv.convert_volume(1, "floz", "ml") == 29.57353
    assert conv.convert_volume(1, "fl oz", "cup") == 0.125


def test_list_units():
    """Test listing available units."""
    conv = UnitConverter()
    assert conv.list_units("length") == ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"]
    assert "m" in conv.list_units("length")
    assert "km" in conv.list_units("length")
    assert conv.list_units("weight") == ["mg", "g", "kg", "oz", "lb", "ton"]
    assert conv.list_units("volume") == ["ml", "l", "gal", "qt", "pt", "cup", "floz"]
    assert conv.list_units("temperature") == ["c", "f", "k"]


def test_category_names_are_flexible():
    conv = UnitConverter()
    assert conv.list_units(" Length ") == conv.list_units("length")
    assert conv.list_units("temp") == conv.list_units("temperature")
    assert conv.list_units("mass") == conv.list_units("weight")
    with pytest.raises(ValueError, match="Unknown category"):
        conv.list_units("speed")


def test_units_ignore_case_whitespace_and_common_names():
    conv = UnitConverter()
    assert conv.convert_length(1, "M", "CM") == 100
    assert conv.convert_length(1, " m ", "cm") == 100
    assert conv.convert_length(1, "meter", "kilometers") == 0.001
    assert conv.convert_length(12, "inches", "foot") == 1
    assert conv.convert_weight(1, "Lb", "Kg") == 0.453592
    assert conv.convert_weight(1, "tonne", "kg") == 1000
    assert conv.convert_weight(1, "t", "kg") == 1000
    assert conv.convert_volume(1, "Gallon", "quarts") == 4
    assert conv.convert_temperature(25, "C", "F") == 77
    assert conv.convert_temperature(0, "celsius", "fahrenheit") == 32
    assert conv.convert_temperature(100, "°C", "°F") == 212


def test_unknown_units_raise_value_error():
    conv = UnitConverter()
    with pytest.raises(ValueError, match="Unknown length unit"):
        conv.convert_length(1, "parsec", "m")
    with pytest.raises(ValueError, match="Unknown weight unit"):
        conv.convert_weight(1, "stone", "kg")
    with pytest.raises(ValueError, match="Unknown volume unit"):
        conv.convert_volume(1, "barrel", "l")
    with pytest.raises(ValueError, match="Unknown temperature unit"):
        conv.convert_temperature(0, "rankine", "c")
    with pytest.raises(ValueError, match="must be a string"):
        conv.convert_length(1, None, "m")


def test_non_finite_and_non_numeric_values_are_rejected():
    conv = UnitConverter()
    with pytest.raises(ValueError, match="finite"):
        conv.convert_length(float("nan"), "m", "cm")
    with pytest.raises(ValueError, match="finite"):
        conv.convert_volume(float("inf"), "l", "ml")
    with pytest.raises(ValueError, match="real number"):
        conv.convert_weight(True, "kg", "g")
    with pytest.raises(ValueError, match="real number"):
        conv.convert_temperature("25", "c", "f")


def test_negative_lengths_weights_and_volumes_stay_signed():
    """Signed deltas are valid; only non-finite numbers are rejected."""
    conv = UnitConverter()
    assert conv.convert_length(-1, "m", "cm") == -100
    assert conv.convert_weight(0, "lb", "kg") == 0
    assert conv.convert_volume(-2, "l", "ml") == -2000


def test_temperature_below_absolute_zero_is_rejected():
    conv = UnitConverter()
    with pytest.raises(ValueError, match="absolute zero"):
        conv.convert_temperature(-300, "c", "k")
    with pytest.raises(ValueError, match="absolute zero"):
        conv.convert_temperature(-1, "k", "c")
    assert conv.convert_temperature(0, "k", "k") == 0
    assert conv.convert_temperature(-273.15, "c", "k") == 0


def test_convert_all_matches_single_conversions():
    conv = UnitConverter()
    cases = [
        ("length", 3, "ft", conv.convert_length),
        ("weight", 2, "kg", conv.convert_weight),
        ("volume", 1, "cup", conv.convert_volume),
        ("temp", -40, "f", conv.convert_temperature),
    ]
    for category, value, unit, method in cases:
        results = conv.convert_all(value, unit, category)
        assert list(results) == conv.list_units(category)
        for target, converted in results.items():
            assert converted == method(value, unit, target)


def test_convert_all_rejects_a_unit_from_another_category():
    conv = UnitConverter()
    with pytest.raises(ValueError, match="Unknown length unit"):
        conv.convert_all(1, "kg", "length")
    with pytest.raises(ValueError, match="Unknown category"):
        conv.convert_all(1, "m", "speed")
