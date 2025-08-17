from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using VADER
    Returns a dictionary with sentiment scores
    """
    try:
        # Initialize VADER sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()
        
        # Get sentiment scores for the actual text
        sentiment_scores = analyzer.polarity_scores(text)
        
        # Determine the overall sentiment based on compound score
        compound_score = sentiment_scores['compound']
        
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'compound': compound_score,
            'positive': sentiment_scores['pos'],
            'negative': sentiment_scores['neg'],
            'neutral': sentiment_scores['neu']
        }
        
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        # Return neutral as fallback
        return {
            'sentiment': 'neutral',
            'compound': 0.0,
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 1.0
        }
    