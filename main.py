import yfinance as yf
import sqlite3
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()

apikey = os.getenv("NEWS_API_KEY")

def get_val():
    open_price=(ticker.info['regularMarketOpen'])
    day_high=(ticker.info['regularMarketDayHigh'])
    day_low=(ticker.info['regularMarketDayLow'])
    prev_close=(ticker.info['previousClose'])
    volume=(ticker.info['averageDailyVolume10Day'])

    return (open_price,day_high,day_low,prev_close,volume)

#connection
connection=sqlite3.connect('Sentiment_Analysis.db')
cursor=connection.cursor()

n=int(input("Enter number of tickers:"))

#HEADLINES FOR A TICKER
ticker_list=[]

for i in range (n):
    #GET VALUE
    _=str(input("Enter ticker:"))
    ticker=yf.Ticker(f'{_}')
    ticker_list.append(ticker)

    #update table
    table_name="BOOM1234"

    list_val=get_val()

    cursor.execute(f"create table IF NOT EXISTS {table_name}(Ticker VARCHAR(10) NOT NULL,Open FLOAT, High FLOAT, Low FLOAT, Close FLOAT, Volume FLOAT)")
    cursor.execute(f"insert into {table_name} (Ticker,Open,High,Low,Close,Volume) VALUES ('{_}',{list_val[0]},{list_val[1]},{list_val[2]},{list_val[3]},{list_val[4]})")

#analyser
analyser=SentimentIntensityAnalyzer()
title={}
sentiment_score={}
def headlines(ticker_name):
    url=('https://newsapi.org/v2/everything?'
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
    
    title[ticker_name]=title_list

#CALCULATES SENTIMENT SCORE USING VADER
#Will add FinBERT for accurate result

def VADER():
    cursor.execute('CREATE TABLE IF NOT EXISTS Sentiment_Scores (Ticker VARCHAR(10) PRIMARY KEY,"Sentiment Score (VADER)" FLOAT)')
    for k,v in title.items():
        j=0
        SUM=0
        for i in v:
            j+=1
            vs=analyser.polarity_scores(i)
            SUM+=vs['compound']
        avg=SUM/j
        sentiment_score[k]=avg
        cursor.execute(f'INSERT INTO Sentiment_Scores (Ticker,"Sentiment Score (VADER)") VALUES ("{k}",{avg})')
    connection.commit()

VADER()

cursor.execute("SELECT * FROM Sentiment_Scores")
rows=cursor.fetchall()
for row in rows:
    print(row)
cursor.close()
connection.close()
