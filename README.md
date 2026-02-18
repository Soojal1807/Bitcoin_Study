# Bitcoin Study Analysis

This folder contains a Python script for analyzing historical Bitcoin data.

## `BTC study.py`

This script fetches historical Bitcoin (BTC-USD) data using `yfinance`, calculates volatility, identifies peak prices and best profit dates, and outlines bear and bull market timelines.

When executed, it generates a `report.txt` file within this directory, summarizing the analysis.

## Setup

To run `BTC study.py`, you need Python and the following libraries:
- `yfinance`
- `pandas`
- `numpy`

Install them using pip:

```bash
pip install yfinance pandas numpy
```

## Usage

Run the script from your terminal:

```bash
python "BTC study.py"
```

This will generate or update the `report.txt` file in this directory.

## License

This project (and its contents) is licensed under the MIT License. See the main project's `LICENSE` file for details.
