"""
CLI interface for unit-converter.
"""

import click
from rich.console import Console
from rich.table import Table

from .converter import UnitConverter

console = Console()


@click.group()
@click.version_option()
def main():
    """Unit Converter - Convert between different units of measurement."""
    pass


@main.command()
@click.argument("value", type=float)
@click.option("--from", "from_unit", required=True, help="Source unit")
@click.option("--to", "to_unit", required=True, help="Target unit")
def length(value, from_unit, to_unit):
    """Convert length units."""
    conv = UnitConverter()
    result = conv.convert_length(value, from_unit, to_unit)
    console.print(f"\n📏 {value} {from_unit} = [bold green]{result} {to_unit}[/bold green]")


@main.command()
@click.argument("value", type=float)
@click.option("--from", "from_unit", required=True, help="Source unit")
@click.option("--to", "to_unit", required=True, help="Target unit")
def weight(value, from_unit, to_unit):
    """Convert weight units."""
    conv = UnitConverter()
    result = conv.convert_weight(value, from_unit, to_unit)
    console.print(f"\n⚖️  {value} {from_unit} = [bold green]{result} {to_unit}[/bold green]")


@main.command()
@click.argument("value", type=float)
@click.option("--from", "from_unit", required=True, help="Source unit (c/f/k)")
@click.option("--to", "to_unit", required=True, help="Target unit (c/f/k)")
def temp(value, from_unit, to_unit):
    """Convert temperature units."""
    conv = UnitConverter()
    result = conv.convert_temperature(value, from_unit, to_unit)
    console.print(f"\n🌡️  {value}°{from_unit.upper()} = [bold green]{result}°{to_unit.upper()}[/bold green]")


@main.command()
@click.argument("value", type=float)
@click.option("--from", "from_unit", required=True, help="Source unit")
@click.option("--to", "to_unit", required=True, help="Target unit")
def volume(value, from_unit, to_unit):
    """Convert volume units."""
    conv = UnitConverter()
    result = conv.convert_volume(value, from_unit, to_unit)
    console.print(f"\n🥤 {value} {from_unit} = [bold green]{result} {to_unit}[/bold green]")


@main.command()
@click.argument("category", type=click.Choice(["length", "weight", "volume", "temperature"]))
def units(category):
    """List available units for a category."""
    conv = UnitConverter()
    units = conv.list_units(category)
    console.print(f"\n📋 Available units for [bold]{category}[/bold]:")
    for u in units:
        console.print(f"  • {u}")


if __name__ == "__main__":
    main()
