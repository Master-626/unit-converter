# Unit Converter

## 中文摘要

`unit-converter`（命令 `uconv`）是一个轻量的长度、重量、温度、体积换算工具，可在命令行使用，也可作为 Python 库调用。单位符号不区分大小写，也接受 `meter`、`celsius` 这类常见名称。负数可以直接写在命令里，例如 `-40`。`ton` 表示公吨（1000 kg）。体积使用美制液量，并保证 1 加仑 = 4 夸脱 = 8 品脱 = 16 杯 = 128 液盎司。低于绝对零度的温度会报错。安装、选项和测试见下方英文说明。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Master-626/unit-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/Master-626/unit-converter/actions/workflows/ci.yml)

Convert length, weight, temperature, and volume from the command line or from Python. Results for length, weight, and volume are rounded to 6 decimal places. Temperatures are rounded to 2 decimal places.

## Installation

Requires Python 3.8 or newer.

```bash
git clone https://github.com/Master-626/unit-converter.git
cd unit-converter
python -m pip install .
```

This installs two commands, `uconv` and `unit-converter`. Both run the same program.

For development, including tests and lint:

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
uconv length 10 --from mi --to km
uconv weight 150 --from lb --to kg
uconv temp 25 --from c --to f
uconv temp -40 --from c --to f
uconv volume 1 --from gal --to qt
```

Show the same value in every unit of one category:

```bash
uconv length 1 --from m --all
uconv temp 0 --from c --all
```

List the canonical symbols for a category (`length`, `weight`, `mass`, `volume`, `temperature`, or `temp`):

```bash
uconv units length
uconv units temperature
```

`--help` and `--version` work on the main command and on each subcommand.

### Options

| Command | Argument | Options |
| --- | --- | --- |
| `length`, `weight`, `temp`, `volume` | `VALUE` (a finite number) | `--from UNIT` (required), `--to UNIT`, `--all` |
| `units` | `CATEGORY` | none |

`--to` and `--all` cannot be used together. If neither is given, the command exits with status 2 and reports that `--to` is missing. Unknown units, non-finite numbers, and temperatures below absolute zero exit with status 1 and a one-line error. No traceback is printed for those cases.

Negative values can be written directly, before or after the options: `uconv temp -40 --from c --to f`. Scientific notation such as `-1e-3` works the same way.

Unit tokens are case-insensitive. Surrounding space, `_`, `-`, `.`, and a leading degree sign are ignored, so `M`, `°C`, and `fl oz` are accepted. Common names work too: `meter`/`metre`, `inch`/`foot`/`mile`, `pound`/`ounce`, `liter`/`gallon`/`quart`, `celsius`/`fahrenheit`/`kelvin`.

### Units

| Category | Canonical symbols | Notes |
| --- | --- | --- |
| Length | `mm`, `cm`, `m`, `km`, `in`, `ft`, `yd`, `mi` | International inch, 1 in = 0.0254 m |
| Weight | `mg`, `g`, `kg`, `oz`, `lb`, `ton` | `lb` is the international pound, 0.45359237 kg. `ton` is the metric tonne, 1000 kg, not the US short ton |
| Volume | `ml`, `l`, `gal`, `qt`, `pt`, `cup`, `floz` | US liquid measure. 1 gal = 4 qt = 8 pt = 16 cup = 128 fl oz |
| Temperature | `c`, `f`, `k` | Absolute temperatures. Values below 0 K are rejected |

Negative length, weight, and volume values are kept as signed quantities. `0` stays `0`.

## Python API

```python
from unit_converter import UnitConverter

conv = UnitConverter()

conv.convert_length(10, "km", "mi")
conv.convert_weight(150, "lb", "kg")
conv.convert_temperature(25, "c", "f")
conv.convert_volume(1, "gal", "qt")

# Every unit in the category, in list_units order.
conv.convert_all(1, "m", "length")
conv.list_units("temp")
```

Unknown units and unknown categories raise `ValueError`. The same is true for non-finite values and temperatures below absolute zero.

`UnitConverter.length_units`, `weight_units`, and `volume_units` are the factor tables. Keys are the canonical symbols. Values are the size of one unit in meters, kilograms, or liters.

## Running tests

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
```

GitHub Actions runs that lint and test suite on Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13.

## License

MIT License. See [LICENSE](LICENSE).
