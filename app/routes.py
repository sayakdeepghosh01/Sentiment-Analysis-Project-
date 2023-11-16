# app/routes.py
from flask import render_template, request, jsonify, flash
from app import app
from app.utils import perform_sentiment_analysis, scrape_data
print(app.config['SECRET_KEY'])


base_sentiment_score = 0.5  # Initial sentiment score

@app.route('/')
def index():
    global base_sentiment_score
    return render_template('index.html', sentiment_score=base_sentiment_score)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    global base_sentiment_score
    data = request.get_json()
    sentiment_score, sentiment_label = perform_sentiment_analysis(data['text'])
    
    # Check if the entered text is a valid URL
    if data['text'].startswith(('http://', 'https://')):
        # Perform web scraping and analyze sentiment of the scraped content
        scraped_data = scrape_data(data['text'])
        scraped_score, _ = perform_sentiment_analysis(scraped_data)
        sentiment_score += scraped_score
        flash('Scraped Content Sentiment Analyzed.')

    # Check for other reasons to modify the sentiment score
    if "bad comment" in data['text'].lower():
        base_sentiment_score -= 0.1  # Decrease score for bad comments
        flash('Alert: Someone has put a bad comment on Facebook! Sentiment Score Decreased.')
    
    if "followers increased" in data['text'].lower():
        base_sentiment_score += 0.05  # Increase score for followers increase
        flash('Good News: Number of followers increased on LinkedIn! Sentiment Score Increased.')
    
    if "new article" in data['text'].lower() and "20 likes" in data['text'].lower():
        base_sentiment_score += 0.1  # Increase score for liked articles
        flash('Exciting News: New article published on LinkedIn got 20 likes! Sentiment Score Increased.')
    
    if "youtube followers increased" in data['text'].lower():
        base_sentiment_score += 0.08  # Increase score for YouTube followers increase
        flash('Amazing: YouTube followers of the product/brand increased! Sentiment Score Increased.')
    
    # You can add more conditions based on your specific requirements
    
    return jsonify({'sentiment_score': base_sentiment_score + sentiment_score, 'sentiment_label': sentiment_label})
