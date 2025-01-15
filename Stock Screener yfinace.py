import yfinance as yf
import pandas as pd
import time
import threading  # For parallel data fetching
from datetime import datetime


def fetch_live_data(tickers):
    """
    Fetch the latest live data for a list of tickers.
    """
    live_data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            # Fetch live data using the "1-minute" interval for today
            hist = stock.history(period="1d", interval="1m")  # Live prices (1-minute granularity)
            if not hist.empty:
                live_data[ticker] = hist
        except Exception as e:
            print(f"Error fetching live data for {ticker}: {e}")
    return live_data


def calculate_indicators(stock_data):
    """
    Calculate key indicators: 25-day MA, ATR, and volatility.
    """
    screened_stocks = []
    for ticker, hist in stock_data.items():
        if hist.empty or len(hist) < 25:  # Skip if not enough data
            print(f"Not enough data for {ticker}")
            continue

        # Calculate indicators
        hist['25_MA'] = hist['Close'].rolling(window=25).mean()
        hist['ATR'] = (hist['High'] - hist['Low']).rolling(window=14).mean()  # Simplified ATR
        hist['Volatility'] = hist['Close'].pct_change().rolling(window=14).std()

        # Extract latest values
        current_price = hist['Close'].iloc[-1]
        ma_25 = hist['25_MA'].iloc[-1]
        atr = hist['ATR'].iloc[-1]
        volatility = hist['Volatility'].iloc[-1]
        avg_volume = hist['Volume'].rolling(window=14).mean().iloc[-1]

        # Debugging: Print calculated metrics for each stock
        print(
            f"Ticker: {ticker}, Current Price: {current_price}, 25_MA: {ma_25}, ATR: {atr}, Volatility: {volatility}, Avg Volume: {avg_volume}")

        # Screening criteria
        if current_price < 0.9 * ma_25 and avg_volume > 50000 and volatility > 0.01:  # Looser filters for testing
            screened_stocks.append({
                'Ticker': ticker,
                'Current Price': current_price,
                '25-day MA': ma_25,
                'ATR': atr,
                'Volatility': volatility,
                'Avg Volume': avg_volume
            })
    return pd.DataFrame(screened_stocks)


def fetch_and_screen(tickers):
   
    stock_data = fetch_live_data(tickers)
    return calculate_indicators(stock_data)


def periodic_update(tickers, interval=60):
    """
    Fetch stock data and run the screener at periodic intervals.
    """
    while True:
        print(f"\nFetching live data... {datetime.now()}")
        result = fetch_and_screen(tickers)
        if not result.empty:
            print("\nStocks aligning with BNF strategy:")
            print(result)
        else:
            print("\nNo stocks matching the criteria at this moment.")
        time.sleep(interval)  # Wait for the next fetch cycle


# Example tickers
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'TM', 'BABA', 'TCEHY', 'SONY', 'MS', 'OXY']

# Run the screener in a separate thread for continuous fetching
thread = threading.Thread(target=periodic_update, args=(tickers, 5))  # Run every 5 seconds
thread.daemon = True  # Exit the thread when the main program ends
thread.start()

# Main program execution can continue here without blocking.
try:
    while True:
        # Optionally, you can add any other tasks or checks here
        time.sleep(1)  # Main program does nothing but keeps the script running
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
