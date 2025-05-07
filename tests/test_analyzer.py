import pytest
from src.analyzer import analyze_sentiment_vader, analyze_sentiment_blob, classify_sentiment

def test_analyze_sentiment_vader():
    assert analyze_sentiment_vader("I love this product! It's amazing!") > 0
    assert analyze_sentiment_vader("This is terrible, I hate it.") < 0
    assert -0.05 <= analyze_sentiment_vader("This is a product.") <= 0.05
    assert analyze_sentiment_vader("") == 0.0

def test_analyze_sentiment_blob():
    assert analyze_sentiment_blob("I love this product! It's amazing!") > 0
    assert analyze_sentiment_blob("This is terrible, I hate it.") < 0
    assert -0.05 <= analyze_sentiment_blob("This is a product.") <= 0.05
    assert analyze_sentiment_blob("") == 0.0

def test_classify_sentiment():
    assert classify_sentiment(0.8) == "Positive"
    assert classify_sentiment(0.1) == "Positive"
    assert classify_sentiment(-0.8) == "Negative"
    assert classify_sentiment(-0.1) == "Negative"
    assert classify_sentiment(0.0) == "Neutral"
    assert classify_sentiment(0.04) == "Neutral"
    assert classify_sentiment(-0.04) == "Neutral" 