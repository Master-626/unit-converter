from click.testing import CliRunner

from unit_converter.cli import main

runner = CliRunner()


def test_length_output_format():
    result = runner.invoke(main, ["length", "1", "--from", "m", "--to", "cm"])
    assert result.exit_code == 0
    assert result.output == "\n📏 1.0 m = 100.0 cm\n"


def test_weight_output_format():
    result = runner.invoke(main, ["weight", "1", "--from", "lb", "--to", "kg"])
    assert result.exit_code == 0
    assert result.output == "\n⚖️  1.0 lb = 0.453592 kg\n"


def test_temperature_output_format():
    result = runner.invoke(main, ["temp", "0", "--from", "c", "--to", "f"])
    assert result.exit_code == 0
    assert result.output == "\n🌡️  0.0°C = 32.0°F\n"


def test_volume_output_uses_exact_gallon():
    result = runner.invoke(main, ["volume", "1", "--from", "gal", "--to", "l"])
    assert result.exit_code == 0
    assert result.output == "\n🥤 1.0 gal = 3.785412 l\n"


def test_units_aliases_list_the_same_symbols():
    mass = runner.invoke(main, ["units", "mass"])
    assert mass.exit_code == 0
    assert "kg" in mass.output
    assert "lb" in mass.output

    temp = runner.invoke(main, ["units", "temp"])
    assert temp.exit_code == 0
    for unit in ("c", "f", "k"):
        assert unit in temp.output


def test_units_list_output():
    result = runner.invoke(main, ["units", "length"])
    assert result.exit_code == 0
    assert result.output == (
        "\n📋 Available units for length:\n"
        "  • mm\n  • cm\n  • m\n  • km\n  • in\n  • ft\n  • yd\n  • mi\n"
    )


def test_unknown_unit_is_a_clean_error():
    result = runner.invoke(main, ["length", "1", "--from", "parsec", "--to", "m"])
    assert result.exit_code == 1
    assert "Unknown length unit" in result.output
    assert "Traceback" not in result.output


def test_case_and_names_work_from_the_cli():
    result = runner.invoke(main, ["temp", "100", "--from", "Celsius", "--to", "F"])
    assert result.exit_code == 0
    assert "212.0" in result.output


def test_non_finite_cli_value_is_rejected():
    result = runner.invoke(main, ["length", "nan", "--from", "m", "--to", "cm"])
    assert result.exit_code == 1
    assert "finite" in result.output


def test_below_absolute_zero_cli_error():
    result = runner.invoke(main, ["temp", "-300", "--from", "c", "--to", "k"])
    assert result.exit_code == 1
    assert "absolute zero" in result.output
    assert "Traceback" not in result.output


def test_scientific_notation_values():
    positive = runner.invoke(main, ["length", "1e-3", "--from", "km", "--to", "m"])
    assert positive.exit_code == 0
    assert positive.output == "\n📏 0.001 km = 1.0 m\n"

    negative = runner.invoke(main, ["length", "-1e-3", "--from", "km", "--to", "m"])
    assert negative.exit_code == 0
    assert negative.output == "\n📏 -0.001 km = -1.0 m\n"


def test_negative_values_are_not_parsed_as_options():
    before_options = runner.invoke(main, ["temp", "-40", "--from", "c", "--to", "f"])
    assert before_options.exit_code == 0
    assert before_options.output == "\n🌡️  -40.0°C = -40.0°F\n"

    after_options = runner.invoke(main, ["length", "--from", "m", "--to", "cm", "-1"])
    assert after_options.exit_code == 0
    assert after_options.output == "\n📏 -1.0 m = -100.0 cm\n"

    with_separator = runner.invoke(main, ["temp", "--from", "c", "--to", "f", "--", "-40"])
    assert with_separator.exit_code == 0
    assert with_separator.output == "\n🌡️  -40.0°C = -40.0°F\n"


def test_missing_target_still_explains_the_option():
    result = runner.invoke(main, ["length", "1", "--from", "m"])
    assert result.exit_code == 2
    assert "Missing option '--to'" in result.output


def test_to_and_all_are_mutually_exclusive():
    result = runner.invoke(main, ["weight", "1", "--from", "kg", "--to", "g", "--all"])
    assert result.exit_code == 2
    assert "--all" in result.output


def test_convert_all_lists_every_length_unit():
    result = runner.invoke(main, ["length", "1", "--from", "m", "--all"])
    assert result.exit_code == 0
    for snippet in ("mm", "cm", "km", "1000.0", "0.001", "39.370079", "3.28084"):
        assert snippet in result.output


def test_convert_all_temperature():
    result = runner.invoke(main, ["temp", "0", "--from", "c", "--all"])
    assert result.exit_code == 0
    for snippet in ("°C", "°F", "°K", "0.0", "32.0", "273.15"):
        assert snippet in result.output


def test_length_help_documents_all():
    result = runner.invoke(main, ["length", "--help"])
    assert result.exit_code == 0
    assert "--from" in result.output
    assert "--to" in result.output
    assert "--all" in result.output


def test_version_matches_package():
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.1" in result.output
