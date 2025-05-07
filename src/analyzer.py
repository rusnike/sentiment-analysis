from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from google.cloud import language_v1

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_blob(review):
    if not review.strip():
        return 0.0
    return TextBlob(review).sentiment.polarity

def analyze_sentiment_vader(review):
    if not review.strip():
        return 0.0
    return analyzer.polarity_scores(review)["compound"]

def analyze_sentiment_google(review):
    if not review.strip():
        return 0.0
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=review, type=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return sentiment.score

def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    return "Neutral"