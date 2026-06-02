import yfinance as yf
import sqlite3

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

for i in range (n):
    _=str(input("Enter ticker:"))
    #GET VALUE
    ticker=yf.Ticker(f'{_}')

    #update table
    table_name="BOOM1234"

    list_val=get_val()

    #(UNCOMMENT THIS IF RUNNING FOR FIRST TIME)cursor.execute(f"create table {table_name}(Ticker VARCHAR(10) NOT NULL,Open FLOAT, High FLOAT, Low FLOAT, Close FLOAT, Volume FLOAT)")
    cursor.execute(f"insert into {table_name} (Ticker,Open,High,Low,Close,Volume) VALUES ('{_}',{list_val[0]},{list_val[1]},{list_val[2]},{list_val[3]},{list_val[4]})")
    connection.commit()
    
cursor.execute(f"select * from {table_name}")
rows=cursor.fetchall()

for row in rows:
    print(row)
connection.close()