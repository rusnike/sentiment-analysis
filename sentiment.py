from textblob import TextBlob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("this is gonna be an epic program")
def display_menu():
    print("=== Sentiment Analyzer ===")
    print("1. Upload/Select file")
    print("2. Analyze file (choose mode)")
    print("3. Statistics")
    print("0. Exit")
    print("==========================")

def load_reviews(filename):
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
            return df["Comment"].tolist()
        
        elif filename.endswith(".txt"):
            with open(filename, 'r', encoding="utf-8") as file:
                reviews = []
                for line in file:
                    cleaned_line = line.strip()
                    if cleaned_line:  # only add if line not empty
                        reviews.append(cleaned_line)
            return reviews

        else:
            print("Unsupported format. Please use .txt or .csv file formats")
            return []

    except Exception as e:
        print("Error loading file:", e)
        return []

def analyze_sentiment_blob(review):
    if not review.strip():
        return 0.0
    
    results = TextBlob(review).sentiment.polarity
    return results

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(review):
    if not review.strip():
        return 0.0
    results = analyzer.polarity_scores(review)
    return results["compound"]

def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def save_analysis_results(filename, reviews, scores, classifications):
    try:
        output_filename = f"{filename.split(".")[0]}_sentiment.csv"

        data = {
            "Review": reviews,
            "Sentiment Score": scores,
            "Sentiment Classification": classifications
        }
        df = pd.DataFrame(data)

        df.to_csv(output_filename, index=False, encoding="utf-8")
        print(f"Sentiment Analysis results saved to '{output_filename}'")
    
    except Exception as e:
        print(f"Error while saving: {e}")


def main():
    filename = None

    while True:
        display_menu()
        choice = input("Enter your choice (0-3): ")

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            print("\n==OPLOAD/SELECT FILE MODE(UNDER CONSTRUCTION)==")
            filename = input("Enter the filename (e.g. example.txt): ")
            print(f"\nFile '{filename}' selected.")
            ... # REGEX here? to validate filename input?

        elif choice == "2":
            if not filename:
                print("Please select a file you want to analyze first (Option 1 in menu)")
                return
            print("\n===Analyze Mode===")
            print("\nChoose Sentiment Analysis Method:\n1. VADER\n2. TextBlob")
        
            try:
                choice = int(input("Enter your choice (1 or 2): "))
                if choice in [1, 2]:
                    reviews = load_reviews(filename)
                    scores = []
                    classifications = []

                    for review in reviews:
                        if choice == 1:
                            score = analyze_sentiment_vader(review)
                        elif choice == 2:
                            score = analyze_sentiment_blob(review)

                        sentiment = classify_sentiment(score)
                        scores.append(score)
                        classifications.append(sentiment)
                        # print(f"Score: {score:.3f} -> {sentiment}")

                    save_analysis_results(filename, reviews, scores, classifications)
                else:
                    print("\nInvalid number. Please type 1 or 2")
            except ValueError:
                print("\nInvalid choice. Please type 1 or 2")

        elif choice == "3":
            print("\n===Sentiment Statistics===")
            ...

        else:
            print("\nInvalid choice. Please type a number from the menu")

if __name__ == "__main__":
    main()