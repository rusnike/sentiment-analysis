import pandas as pd
from src.analyzer import classify_sentiment

def calculate_statistics(file_path):
    df = pd.read_csv(file_path)
    
    total_reviews = len(df)
    positive_count = len(df[df["Sentiment Classification"] == "Positive"])
    negative_count = len(df[df["Sentiment Classification"] == "Negative"])
    neutral_count = len(df[df["Sentiment Classification"] == "Neutral"])
    sentiment_score = df["Sentiment Score"].mean()
    
    return {
        "total": total_reviews,
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count,
        "score": sentiment_score,
        "classification": classify_sentiment(sentiment_score)
    }

def display_statistics(stats):
    print(f"\nTotal Reviews: {stats['total']}")
    print(f"\nPOSITIVE Reviews: {stats['positive']} ({(stats['positive']/stats['total']*100):.2f}%)")
    print(f"NEGATIVE Reviews: {stats['negative']} ({(stats['negative']/stats['total']*100):.2f}%)")
    print(f"NEUTRAL Reviews: {stats['neutral']} ({(stats['neutral']/stats['total']*100):.2f}%)")
    print(f"\nSENTIMENT SCORE: {stats['score']:.2f} ({stats['classification']})")