# app/utils.py
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup

def perform_sentiment_analysis(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)['compound']
    
    # Define sentiment labels based on the compound score
    if sentiment_score >= 0.05:
        sentiment_label = 'Positive'
    elif sentiment_score <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    
    return sentiment_score, sentiment_label

def scrape_data(url):
    # Implement web scraping logic here using BeautifulSoup and requests
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extract text from paragraphs
        paragraphs = soup.find_all('p')
        scraped_data = '\n'.join([p.get_text() for p in paragraphs])
        
        return scraped_data
    
    return "Error: Unable to fetch data from the website."
