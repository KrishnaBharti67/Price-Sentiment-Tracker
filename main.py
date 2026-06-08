import yfinance as yf
import sqlite3
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()

apikey = os.getenv("NEWS_API_KEY")

analyser = SentimentIntensityAnalyzer()

def get_val(ticker):
    open_price = ticker.info['regularMarketOpen']
    day_high = ticker.info['regularMarketDayHigh']
    day_low = ticker.info['regularMarketDayLow']
    prev_close = ticker.info['previousClose']
    volume = ticker.info['averageDailyVolume10Day']
    return (open_price, day_high, day_low, prev_close, volume)

def headlines(ticker_name):
    url = ('https://newsapi.org/v2/everything?'
           f'q={ticker_name}&'
           'language=en&'
           'from=2026-06-02&'
           'sortBy=publishedAt&'
           f'apiKey={apikey}')

    response=requests.get(url)
    data=response.json()
    title_list=[]

    for article in data["articles"]:
        temp=article['title']
        if ticker_name.lower() not in temp.lower():
            continue
        title_list.append(temp)

    return title_list

def VADER(title, sentiment_score):
    with sqlite3.connect('Sentiment_Analysis.db') as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Sentiment_Scores (Ticker VARCHAR(10) PRIMARY KEY,"Sentiment Score (VADER)" FLOAT)')
        for k,v in title.items():
            j=0
            SUM=0
            for i in v:
                j+= 1
                vs=analyser.polarity_scores(i)
                SUM+=vs['compound']

            if j==0:
                continue

            avg=SUM/j
            sentiment_score[k]=avg
            cursor.execute('INSERT OR REPLACE INTO Sentiment_Scores (Ticker,"Sentiment Score (VADER)") VALUES (?,?)', (k, avg))
        connection.commit()

def run_pipeline(ticker_symbols):
    title={}
    sentiment_score={}

    for symbol in ticker_symbols:
        title[symbol]=headlines(symbol)

    VADER(title,sentiment_score)

    return sentiment_score
