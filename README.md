# Sentiment Analysis Tool

:smile: :no_mouth: :rage: Determine the emotional tone expressed in a piece of text by using this Python-based tool :rage: :no_mouth: :smile: 


## Features

- **Multiple Analysis Methods**:
  - VADER: Rule-based sentiment analysis specifically attuned to social media text
  - TextBlob: Machine learning-based sentiment analysis
  - (Coming Soon) Google Cloud Natural Language API: Advanced sentiment analysis using Google's AI

- **File Support**:
  - Accepts both .txt and .csv files
  - Processes one review per line
  - Handles various text formats and punctuation

- **Analysis Results**:
  - Sentiment scores (-1 to 1)
  - Classification (Positive, Negative, Neutral)
  - Detailed statistics and percentages
  - Results saved in CSV format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/sentiment-analysis.git
cd sentiment-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Quick Setup

1. Create a `data` folder in the project directory (if not exists)
2. Place your review files in the `data` folder
3. Run the program:
```bash
python main.py
```

## Usage Instructions

1. **Select a File**:
   - Choose option 1 from the menu
   - Select a file from the data folder by number

2. **Analyze Reviews**:
   - Choose option 2 from the menu
   - Select analysis method (VADER or TextBlob)
   - Results will be saved in the `results` folder

3. **View Statistics**:
   - Choose option 3 from the menu
   - Select an analysis result file
   - View detailed statistics and percentages

## Data File Format

The program accepts both .txt and .csv files. Each line should contain one complete review, e.g.:
```
This is a great product, I love it!
Not bad, but could be better.
Terrible experience, would not recommend anyone.
```
Important notes:
- One review per line
- No headers needed
- Can include commas, spaces, and other punctuation
- Empty lines will be ignored
- Files should be placed in the "data" folder

## Dependencies

- pandas (>=2.0.0): Data manipulation and CSV handling
- textblob (>=0.17.1): TextBlob sentiment analysis
- vaderSentiment (>=3.3.2): VADER sentiment analysis
- google-cloud-language (>=2.11.0): Optional, for future Google Cloud analysis (in the works)

## Example Output
```
=== Sentiment Statistics ===
Total Reviews: 100
POSITIVE Reviews: 45 (45.00%)
NEGATIVE Reviews: 30 (30.00%)
NEUTRAL Reviews: 25 (25.00%)
SENTIMENT SCORE: 0.15 (Positive)
```
## Project Structure
```
sentiment-analysis/
├── src/                    # Source code
│   ├── __init__.py        # Package marker
│   ├── analyzer.py        # Sentiment analysis functions
│   ├── file_handler.py    # File operations
│   └── statistics.py      # Statistics calculations
├── tests/                  # Test suite
│   ├── __init__.py        # Package marker
│   ├── test_analyzer.py   # Tests for sentiment analysis
│   ├── test_file_handler.py # Tests for file operations
│   └── test_statistics.py # Tests for statistics
├── data/                  # User data directory (ignored by git)
├── results/              # Analysis results (ignored by git)
├── main.py              # Main program
├── requirements.txt     # Dependencies
└── .gitignore          # Git ignore rules
```

