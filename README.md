Stock Screener with Yahoo Finance API
This script fetches live stock data for a list of tickers using Yahoo Finance (yfinance library) and screens stocks based on a modified version of the BNF strategy. It periodically checks stock prices and calculates technical indicators such as the 25-day moving average (MA), Average True Range (ATR), volatility, and average volume.

Features
Fetch live stock data at 1-minute intervals for real-time market monitoring.
Calculate key technical indicators for each stock:
25-day Moving Average (MA)
Average True Range (ATR)
Volatility (14-day standard deviation of returns)
14-day average volume
Screen stocks based on the following criteria:
Current price is less than 90% of the 25-day MA.
Average trading volume exceeds 50,000.
Volatility is greater than 1%.
Run the screener periodically at a configurable interval (default: 60 seconds).
Runs as a background process, updating and printing results in real-time.
