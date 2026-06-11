from main import run_pipeline
import streamlit as st

st.title("Sentiment Tracker")
x=st.multiselect("Ticker",["NVDA", "AAPL", "GOOG", "GOOGL", "MSFT", "AMZN", "AVGO", "META", "TSLA", "BRK.B",
 "LLY", "WMT", "JPM", "V", "UNH", "XOM", "ORCL", "MA", "COST", "HD",
 "PG", "NFLX", "JNJ", "BAC", "ABBV", "KO", "CRM", "CVX", "MRK", "AMD",
 "TMO", "ACN", "PEP", "LIN", "MCD", "CSCO", "IBM", "GE", "ADBE", "TXN",
 "PM", "CAT", "INTU", "DHR", "GS", "ISRG", "NOW", "AMGN", "SPGI", "BKNG"])

if st.button("Analyse"):
   score=run_pipeline(x)
   st.bar_chart(score)
