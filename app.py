import streamlit as st
import pandas as pd
import requests
import json
from datetime import date
import yfinance as yf
from transformers import pipeline

# Sentiment Analysis API
sentiment_analysis = pipeline('sentiment-analysis')

# Set up Streamlit app
st.set_page_config(page_title="Stock Guru", layout="wide")

# Landing page
st.title("Stock Guru - Conversational Recommender System")
st.write("Welcome to Stock Guru, your personal investment assistant!")

# Get user input
user_input = st.text_input("How can I assist you today?", "")

if user_input:
    # Sentiment analysis on user input
    sentiment_score = sentiment_analysis(user_input)[0]['score']
    sentiment_label = sentiment_analysis(user_input)[0]['label']

    # Call financial news API
    news_api_url = "https://api.marketaux.com/v1/news/all?symbols=AAPL,TSLA&filter_entities=true&api_token=WOirwkrrIROs8TFhQcuzyurRdBaxeXrAcDCxuppp"  # Replace with your API URL
    news_response = requests.get(news_api_url)
    news_data = json.loads(news_response.text)

    # Extract news articles from the API response
    news_articles = news_data["data"]

    # Sentiment analysis on news articles
    news_sentiments = []
    for article in news_articles:
        description = article['description']
        news_sentiments.append(sentiment_analysis(description)[0])

    # Get stock data from Yahoo Finance API
    today = date.today()
    start_date = today.replace(year=today.year - 1)
    stock_tickers = [entity['symbol'] for article in news_articles for entity in article['entities']]
    stock_data = {}
    for ticker in stock_tickers:
        stock_data[ticker] = yf.download(ticker, start=start_date, end=today)

    # Display user input sentiment
    st.write(f"Sentiment: {sentiment_label.capitalize()} ({sentiment_score:.2f})")

    # Display news sentiments
    st.subheader("Market Sentiment Analysis")
    for sentiment, article in zip(news_sentiments, news_articles):
        st.write(f"Article Sentiment: {sentiment['label'].capitalize()} ({sentiment['score']:.2f})")
        st.write(f"Article Description: {article['description']}")

    # Display stock data and recommendations
    for ticker, data in stock_data.items():
        st.subheader(f"{ticker} Stock Data")
        st.line_chart(data["Close"])

        # Implement your recommendation logic here
        # ...

        # Display recommendations
        st.subheader("Recommendations")
        st.write(f"Based on your input and market data, we recommend for {ticker}...")