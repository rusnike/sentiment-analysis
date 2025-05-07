import pytest
import pandas as pd
import os
import tempfile
from src.statistics import calculate_statistics, display_statistics

def test_calculate_statistics():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp:
        temp.write("Review,Sentiment Score,Sentiment Classification\n")
        temp.write("Great!,0.8,Positive\n")
        temp.write("Bad!,-0.8,Negative\n")
        temp.write("Okay,0.0,Neutral\n")
        temp_path = temp.name

    try:
        stats = calculate_statistics(temp_path)
        
        assert stats['total'] == 3
        assert stats['positive'] == 1
        assert stats['negative'] == 1
        assert stats['neutral'] == 1
        assert abs(stats['score']) < 0.01
        assert stats['classification'] == "Neutral"

    finally:
        os.unlink(temp_path)

def test_display_statistics(capsys):
    stats = {
        'total': 100,
        'positive': 45,
        'negative': 30,
        'neutral': 25,
        'score': 0.15,
        'classification': 'Positive'
    }
    
    display_statistics(stats)
    
    # capture output
    captured = capsys.readouterr()
    
    # check if output contains info
    assert "Total Reviews: 100" in captured.out
    assert "POSITIVE Reviews: 45 (45.00%)" in captured.out
    assert "NEGATIVE Reviews: 30 (30.00%)" in captured.out
    assert "NEUTRAL Reviews: 25 (25.00%)" in captured.out
    assert "SENTIMENT SCORE: 0.15 (Positive)" in captured.out 