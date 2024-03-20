import streamlit as st
import requests
from textblob import TextBlob

st.title("Stock Guru Chatbot")

# Function to fetch news data from the API
def fetch_news():
    url = "https://api.marketaux.com/v1/news/all"
    params = {
        "symbols": "AAPL,IBM",
        "filter_entities": True,
        "api_token": "WOirwkrrIROs8TFhQcuzyurRdBaxeXrAcDCxuppp"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        st.error("Failed to fetch news data.")
        return []

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

# Fetch news data from the API
news_data = fetch_news()

# Display news data and sentiment analysis in the Streamlit app
if news_data:
    for news_item in news_data:
        st.write(f"Title: {news_item['title']}")
        st.write(f"Description: {news_item['description']}")
        st.write(f"URL: {news_item['url']}")
        st.image(news_item['image_url'], caption="Image", use_column_width=True)
        
        # Perform sentiment analysis
        sentiment = analyze_sentiment(news_item['description'])
        st.write(f"Sentiment: {sentiment}")
        
        st.write("---")
else:
    st.write("No news data available.")

# Continue with the rest of your Streamlit app code...
