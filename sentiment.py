from textblob import TextBlob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from google.cloud import language_v1
import re
import os

def display_menu():
    print("\n=== Sentiment Analyzer ===")
    print("1. Upload/Select file")
    print("2. Analyze file (choose mode)")
    print("3. Statistics")
    print("0. Exit")
    print("==========================")

def load_reviews(filename):
    try:
        if filename.endswith((".csv", ".txt")):
            with open(filename, 'r', encoding="utf-8") as file:
                reviews = [line.strip() for line in file if line.strip()]
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
    else:
        return "Neutral"

def save_analysis_results(filename, reviews, scores, classifications, analysis_method):
    # ensure results dir exists
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # extract the base filename (w/out folder path)
    base_filename = os.path.basename(filename)
    output_filename = f"{os.path.splitext(base_filename)[0]}_sentiment_{analysis_method}.csv"
    output_path = os.path.join(results_dir, output_filename)

    #optional? not sure if happens
    if not reviews:
        print("No reviews to save. The file is empty or could not be loaded.")
        return

    try:
        data = {
            "Review": reviews,
            "Sentiment Score": scores,
            "Sentiment Classification": classifications
        }
        df = pd.DataFrame(data)

        print(f"[DEBUG] Saving analysis results to: {output_path}")
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"\nSentiment Analysis results saved to '{output_path}'")
    
    except Exception as e:
        print(f"Error while saving: {e}")

def valid_filename(filename):
    pattern = r"^[\w\-. ]+\.(txt|csv)$"
    forbidden = r"[\/:*?\"<>\|]"
    if re.search(forbidden, filename):
        return False
    return re.match(pattern, filename) is not None

def main():
    filename = None
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    while True:
        display_menu()
        choice = input("Enter your choice (0-3): ")

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            print("\n==UPLOAD/SELECT FILE MODE==")
            data_files = [f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))]
            if data_files:
                print("Files available in /data folder:")
                for i, f in enumerate(data_files, 1):
                    print(f"{i}. {f}")
            else:
                print("No files in /data. Please upload your file there first.")
                continue

            while True:
                try:
                    file_choice = input("Enter the number of the file you want to select (or 0 to exit): ")
                    if file_choice == "0":
                        break
                    
                    file_index = int(file_choice) - 1
                    if 0 <= file_index < len(data_files):
                        selected_file = data_files[file_index]
                        full_path = os.path.join("data", selected_file)
                        print(f"\nFile '{selected_file}' selected.")
                        filename = full_path
                        break
                    else:
                        print("Invalid file number. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "2":
            if not filename:
                print("\nPlease select a file you want to analyze first (Option 1 in menu)")
                continue

            print("\n===Analyze Mode===")
            print("\nChoose Sentiment Analysis Method:\n1. VADER\n2. TextBlob\n3. Google Cloud")
        
            try:
                choice = int(input("Enter your choice (1, 2 or 3): "))
                if choice in [1, 2]:
                    print(f"\n[DEBUG] Analyzing file: {filename} using {'VADER' if choice == 1 else 'TextBlob'}")
                    reviews = load_reviews(filename)
                    scores = []
                    classifications = []
                    analysis_method = "vader" if choice == 1 else "textblob"

                    for review in reviews:
                        if choice == 1:
                            score = analyze_sentiment_vader(review)
                        elif choice == 2:
                            score = analyze_sentiment_blob(review)

                        sentiment = classify_sentiment(score)
                        scores.append(score)
                        classifications.append(sentiment)
                        # print(f"Score: {score:.3f} -> {sentiment}")

                    save_analysis_results(filename, reviews, scores, classifications, analysis_method)
                else:
                    print("\nInvalid number. Please type 1 or 2")
            except ValueError:
                print("\nInvalid choice. Please type 1 or 2")

        elif choice == "3":
            print("\n===Sentiment Statistics===")
            # Look for analysis files
            results_dir = "results"
            if not os.path.exists(results_dir):
                print("\nNo analysis results found. Please analyze a file first (Option 2 in menu)")
                continue
                
            # Get all analysis files
            analysis_files = [f for f in os.listdir(results_dir) if f.endswith('_sentiment_vader.csv') or f.endswith('_sentiment_textblob.csv')]
            if not analysis_files:
                print("\nNo analysis results found. Please analyze a file first (Option 2 in menu)")
                continue
            
            # Display available analysis files
            print("\nAvailable analysis results:")
            for i, f in enumerate(analysis_files, 1):
                print(f"{i}. {f}")
            
            # Let user choose which file to view statistics for
            while True:
                try:
                    file_choice = input("\nEnter the number of the analysis result to view (or 0 to exit): ")
                    if file_choice == "0":
                        break
                    
                    file_index = int(file_choice) - 1
                    if 0 <= file_index < len(analysis_files):
                        selected_file = analysis_files[file_index]
                        file_path = os.path.join(results_dir, selected_file)
                        print(f"\n[DEBUG] Reading statistics from: {file_path}")
                        df = pd.read_csv(file_path)
                        
                        # Count classifications
                        total_reviews = len(df)
                        positive_count = len(df[df['Sentiment Classification'] == 'Positive'])
                        negative_count = len(df[df['Sentiment Classification'] == 'Negative'])
                        neutral_count = len(df[df['Sentiment Classification'] == 'Neutral'])
                        sentiment_score = df['Sentiment Score'].mean()

                        sentiment_score_classification = classify_sentiment(sentiment_score)
                        
                        positive_percentage = (positive_count / total_reviews) * 100    
                        negative_percentage = (negative_count / total_reviews) * 100
                        neutral_percentage = (neutral_count / total_reviews) * 100

                        print(f"\nTotal Reviews: {total_reviews}")
                        print(f"\nPOSITIVE Reviews: {positive_count} ({positive_percentage:.2f}%)")
                        print(f"NEGATIVE Reviews: {negative_count} ({negative_percentage:.2f}%)")
                        print(f"NEUTRAL Reviews: {neutral_count} ({neutral_percentage:.2f}%)")
                        print(f"\nSENTIMENT SCORE: {sentiment_score:.2f} ({sentiment_score_classification})")
                        break
                    else:
                        print("Invalid file number. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

        else:
            print("\nInvalid choice. Please type a number from the menu")

if __name__ == "__main__":
    main()
