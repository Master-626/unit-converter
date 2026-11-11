"""
CLI interface for unit-converter.
"""

import sys

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .converter import UnitConverter

console = Console()


def _is_negative_number(token):
    """True for tokens such as ``-40`` or ``-1e-3``, which Click treats as options."""
    if len(token) < 2 or not token.startswith("-"):
        return False
    try:
        float(token)
    except ValueError:
        return False
    return True


def _allow_negative_numbers(args):
    """Move negative numeric arguments behind ``--``.

    Click parses ``-40`` as the short option ``-4``. Putting the number after
    ``--`` keeps ``uconv temp -40 --from c --to f`` working, including when the
    number is written before the options.
    """
    tokens = sys.argv[1:] if args is None else list(args)
    if "--" in tokens or not any(_is_negative_number(token) for token in tokens):
        return tokens

    kept = []
    numbers = []
    for token in tokens:
        if _is_negative_number(token):
            numbers.append(token)
        else:
            kept.append(token)
    return kept + ["--"] + numbers


class _ConverterGroup(click.Group):
    """Group entry point that accepts negative measurement values."""

    def main(self, args=None, prog_name=None, complete_var=None, standalone_mode=True, **extra):
        return super().main(
            args=_allow_negative_numbers(args),
            prog_name=prog_name,
            complete_var=complete_var,
            standalone_mode=standalone_mode,
            **extra,
        )

_METHODS = {
    "length": "convert_length",
    "weight": "convert_weight",
    "temp": "convert_temperature",
    "volume": "convert_volume",
}

_EMOJI = {
    "length": "📏",
    "weight": "⚖️",
    "temp": "🌡️",
    "volume": "🥤",
}


def _single_line(kind, value, from_unit, to_unit, result):
    if kind == "length":
        return f"\n📏 {value} {from_unit} = [bold green]{result} {to_unit}[/bold green]"
    if kind == "weight":
        return f"\n⚖️  {value} {from_unit} = [bold green]{result} {to_unit}[/bold green]"
    if kind == "temp":
        return (
            f"\n🌡️  {value}°{from_unit.upper()} = "
            f"[bold green]{result}°{to_unit.upper()}[/bold green]"
        )
    return f"\n🥤 {value} {from_unit} = [bold green]{result} {to_unit}[/bold green]"


def _print_all(kind, value, from_unit, results):
    table = Table(title=f"{_EMOJI[kind]} {value} {from_unit}")
    table.add_column("Unit")
    table.add_column("Value")
    for unit, result in results.items():
        label = f"°{unit.upper()}" if kind == "temp" else unit
        table.add_row(label, str(result))
    console.print()
    console.print(table)


def _convert(kind, value, from_unit, to_unit, to_all):
    if to_all and to_unit is not None:
        raise click.UsageError("Use either --to or --all, not both.")
    if not to_all and to_unit is None:
        raise click.UsageError("Missing option '--to'.")

    conv = UnitConverter()
    category = "temperature" if kind == "temp" else kind
    try:
        if to_all:
            results = conv.convert_all(value, from_unit, category)
        else:
            result = getattr(conv, _METHODS[kind])(value, from_unit, to_unit)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    if to_all:
        _print_all(kind, value, from_unit, results)
        return
    console.print(_single_line(kind, value, from_unit, to_unit, result))


def _value_options(function):
    # Click reverses parameter order, so the last decorator applied is shown first.
    function = click.option(
        "--all",
        "to_all",
        is_flag=True,
        help="Convert to every unit in this category instead of --to.",
    )(function)
    function = click.option(
        "--to",
        "to_unit",
        help="Target unit. Required unless --all is set.",
    )(function)
    function = click.option("--from", "from_unit", required=True, help="Source unit.")(function)
    function = click.argument("value", type=float)(function)
    return function


@click.group(cls=_ConverterGroup)
@click.version_option(version=__version__)
def main():
    """Unit Converter - Convert between different units of measurement."""


@main.command()
@_value_options
def length(value, from_unit, to_unit, to_all):
    """Convert length units."""
    _convert("length", value, from_unit, to_unit, to_all)


@main.command()
@_value_options
def weight(value, from_unit, to_unit, to_all):
    """Convert weight units."""
    _convert("weight", value, from_unit, to_unit, to_all)


@main.command()
@_value_options
def temp(value, from_unit, to_unit, to_all):
    """Convert temperature units."""
    _convert("temp", value, from_unit, to_unit, to_all)


@main.command()
@_value_options
def volume(value, from_unit, to_unit, to_all):
    """Convert volume units."""
    _convert("volume", value, from_unit, to_unit, to_all)


@main.command()
@click.argument(
    "category",
    type=click.Choice(
        ["length", "weight", "mass", "volume", "temperature", "temp"],
        case_sensitive=False,
    ),
)
def units(category):
    """List available units for a category."""
    conv = UnitConverter()
    try:
        available = conv.list_units(category)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print(f"\n📋 Available units for [bold]{category}[/bold]:")
    for unit in available:
        console.print(f"  • {unit}")


if __name__ == "__main__":
    main()
