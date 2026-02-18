import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_bitcoin_data(end_date_str='2026-02-17'):
    """Fetches historical Bitcoin data."""
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    btc_data = yf.download("BTC-USD", start="2010-07-18", end=end_date)
    return btc_data

def calculate_volatility_index(data, window=30):
    """Calculates rolling volatility."""
    data['Daily Return'] = data['Close'].iloc[:, 0].pct_change()
    data['Volatility'] = data['Daily Return'].rolling(window=window).std() * np.sqrt(252)
    return data

def find_peak_time(data):
    """Finds peak price."""
    if data.empty:
        return None, None
    peak_price = data['Close'].iloc[:, 0].max()
    peak_date = data['Close'].iloc[:, 0].idxmax()
    return peak_date.strftime('%Y-%m-%d'), peak_price

def find_best_profit_date(data):
    """Finds best profit date."""
    if data.empty:
        return None, None
    data['Daily Gain'] = data['Close'].iloc[:, 0].pct_change()
    best_gain_date = data['Daily Gain'].idxmax()
    best_gain_percentage = data['Daily Gain'].max() * 100
    return best_gain_date.strftime('%Y-%m-%d'), f"{best_gain_percentage:.2f}%"

def identify_bear_bull_timelines(data, window=7, threshold=0.03):
    """Identifies market timelines."""
    if data.empty:
        return [], []

    data['Price Change'] = data['Close'].iloc[:, 0].pct_change()

    bear_timelines = []
    bull_timelines = []
    current_bear_start = None
    current_bull_start = None

    for i in range(1, len(data) - window + 1):
        window_data = data['Price Change'].iloc[i : i + window]
        avg_change = window_data.mean()

        if avg_change < -threshold:
            if current_bear_start is None:
                current_bear_start = data.index[i]
        else:
            if current_bear_start is not None:
                bear_timelines.append((current_bear_start.strftime('%Y-%m-%d'), data.index[i-1].strftime('%Y-%m-%d')))
                current_bear_start = None

        if avg_change > threshold:
            if current_bull_start is None:
                current_bull_start = data.index[i]
        else:
            if current_bull_start is not None:
                bull_timelines.append((current_bull_start.strftime('%Y-%m-%d'), data.index[i-1].strftime('%Y-%m-%d')))
                current_bull_start = None
    
    if current_bear_start is not None:
        bear_timelines.append((current_bear_start.strftime('%Y-%m-%d'), data.index[-1].strftime('%Y-%m-%d')))
    if current_bull_start is not None:
        bull_timelines.append((current_bull_start.strftime('%Y-%m-%d'), data.index[-1].strftime('%Y-%m-%d')))

    return bear_timelines, bull_timelines


def get_volatility_interpretation(volatility_value):
    """Interprets volatility value."""
    if volatility_value is None:
        return "N/A"
    elif volatility_value < 0.30:
        return "Low Volatility"
    elif 0.30 <= volatility_value < 0.60:
        return "Moderate Volatility"
    else:
        return "High Volatility"


def generate_report(data, peak_date, peak_price, best_profit_date, best_profit_percentage, bear_timelines, bull_timelines, report_file_path="report.txt"):
    """Generates a report."""
    with open(report_file_path, "w") as f:
        f.write("Bitcoin Historical Data Analysis Report\n")
        f.write("=========================================\n\n")

        f.write(f"Data Range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}\n\n")

        f.write(f"1. Peak Time of Bitcoin:\n")
        f.write(f"   Date: {peak_date}\n")
        f.write(f"   Peak Price (Adj Close): {peak_price:.2f} USD\n\n")

        f.write(f"2. Best Possible Date for Single-Day Profit:\n")
        f.write(f"   Date: {best_profit_date}\n")
        f.write(f"   Highest Single-Day Gain: {best_profit_percentage}\n\n")

        f.write("3. Volatility Index (Last 30 days annualized):\n")
        if not data['Volatility'].empty:
            current_volatility = data['Volatility'].iloc[-1]
            f.write(f"   Value: {current_volatility:.2f}\n")
            f.write(f"   Interpretation: {get_volatility_interpretation(current_volatility)}\n\n")
        else:
            f.write("   N/A (not enough data for calculation)\n")
            f.write(f"   Interpretation: {get_volatility_interpretation(None)}\n\n")

        f.write("4. Bear Timelines (Average daily price drop > 3% over 7 days):\n")
        if bear_timelines:
            for start, end in bear_timelines:
                f.write(f"   - From {start} to {end}\n")
        else:
            f.write("   No significant bear timelines identified based on criteria.\n")
        f.write("\n")

        f.write("5. Bull Timelines (Average daily price rise > 3% over 7 days):\n")
        if bull_timelines:
            for start, end in bull_timelines:
                f.write(f"   - From {start} to {end}\n")
        else:
            f.write("   No significant bull timelines identified based on criteria.\n")
        f.write("\n")

def main():
    print("Starting Bitcoin historical data analysis...")
    
    end_date_for_data = '2026-02-17'
    btc_data = get_bitcoin_data(end_date_for_data)
    
    if btc_data.empty:
        print("Could not fetch Bitcoin data. Exiting.")
        return

    print(f"Fetched data from {btc_data.index.min().strftime('%Y-%m-%d')} to {btc_data.index.max().strftime('%Y-%m-%d')}")

    btc_data = calculate_volatility_index(btc_data)
    
    peak_date, peak_price = find_peak_time(btc_data)
    best_profit_date, best_profit_percentage = find_best_profit_date(btc_data)
    bear_timelines, bull_timelines = identify_bear_bull_timelines(btc_data)

    generate_report(btc_data, peak_date, peak_price, best_profit_date, best_profit_percentage, bear_timelines, bull_timelines, "D:/Work/DATA/BTC_Study/report.txt")
    print("Analysis complete. Report generated at D:/Work/DATA/BTC_Study/report.txt")

if __name__ == "__main__":
    main()
