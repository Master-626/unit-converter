# Unit Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Cross-Platform](https://img.shields.io/badge/cross-platform-lightgrey.svg)]()

A unit conversion CLI tool for length, weight, temperature, and volume. Used by developers, engineers, and students worldwide.

## 🌟 Features

- 📏 **Length** - Convert between metric and imperial units (m, km, ft, mi, etc.)
- ⚖️ **Weight** - Convert between grams, kilograms, pounds, ounces, etc.
- 🌡️ **Temperature** - Convert between Celsius, Fahrenheit, and Kelvin
- 🥤 **Volume** - Convert between liters, gallons, cups, etc.
- 🎨 **Rich Output** - Beautiful colored terminal output
- 🐍 **Python API** - Use as a library in your code

## 📦 Installation

```bash
git clone https://github.com/Master-626/unit-converter.git
cd unit-converter
pip install .
```

## 🚀 Usage

### Length Conversion
```bash
# Convert miles to kilometers
uconv length 10 --from mi --to km

# Convert feet to meters
uconv length 6 --from ft --to m
```

### Weight Conversion
```bash
# Convert pounds to kilograms
uconv weight 150 --from lb --to kg

# Convert ounces to grams
uconv weight 8 --from oz --to g
```

### Temperature Conversion
```bash
# Convert Celsius to Fahrenheit
uconv temp 25 --from c --to f

# Convert Fahrenheit to Celsius
uconv temp 72 --from f --to c
```

### Volume Conversion
```bash
# Convert gallons to liters
uconv volume 5 --from gal --to l

# Convert cups to milliliters
uconv volume 2 --from cup --to ml
```

### List Available Units
```bash
uconv units length
uconv units weight
uconv units temperature
```

## 🐍 Python API

```python
from unit_converter import UnitConverter

conv = UnitConverter()

# Length
print(conv.convert_length(10, "km", "mi"))

# Weight
print(conv.convert_weight(150, "lb", "kg"))

# Temperature
print(conv.convert_temperature(25, "c", "f"))

# Volume
print(conv.convert_volume(5, "gal", "l"))
```

## 🧪 Testing

```bash
pip install -e ".[dev]"
pytest
```

## 📄 License

MIT License
