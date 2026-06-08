Tracks divergence between price movement and news sentiment for NASDAQ stocks based on user input.

When a stock's price is climbing but every headline is bearish or tanking while news stays positive.
Fetches daily OHLCV data for NASDAQ tickers via yfinance
Scrapes financial headlines per ticker from NewsAPI (~~will add it soon~~  ( **DONE :)** )
Scores headline sentiment using VADER (with FinBERT as a drop-in upgrade) (*will add it soon*)
Computes a divergence score normalized price change minus normalized sentiment (~~*will add it soon*~~)

A high positive divergence means price rose but sentiment was negative.
A high negative divergence means price fell but sentiment was positive.

Stack:
  yfinance
  NewsAPI
  SQLite (Storage)
  Streamlit (Dashboard)


```text
NEWS_API_KEY=your_api_key_here
```
