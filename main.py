from src.file_handler import load_reviews, save_analysis_results, get_available_files
from src.analyzer import analyze_sentiment_vader, analyze_sentiment_blob, classify_sentiment
from src.statistics import calculate_statistics, display_statistics
import os

def display_menu():
    print("\n=== Sentiment Analyzer ===")
    print("1. Select file")
    print("2. Analyze file (choose mode)")
    print("3. Statistics")
    print("0. Exit")
    print("==========================")

def handle_file_selection():
    print("\n=== Selecting File for Sentiment Analysis ===")
    print("\nMake sure your file is in the /data folder.")
    print("Note: each line in your file should contain one review.")
    print("The program will read each line as a separate review, regardless of commas or spaces.")

    data_files = get_available_files("data")
    if not data_files:
        print("No files in /data. Please upload your file there first.")
        return None

    print("\nFiles available in /data folder:")
    for i, f in enumerate(data_files, 1):
        print(f"{i}. {f}")

    while True:
        try:
            file_choice = input("Enter the number of the file you want to select (or 0 to exit): ")
            if file_choice == "0":
                return None
            
            file_index = int(file_choice) - 1
            if 0 <= file_index < len(data_files):
                selected_file = data_files[file_index]
                return os.path.join("data", selected_file)
            print("Invalid file number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def handle_analysis(filename):
    if not filename:
        print("\nPlease select a file you want to analyze first (Option 1 in menu)")
        return

    print("\n=== Analyze Mode ===")
    print("Selected file: ", filename)
    print("\nChoose Sentiment Analysis Method:\n1. VADER (better for social media, informal language, emojis)\n2. TextBlob (better for formal text, reviews, articles, documents)")
    try:
        choice = int(input("Enter your choice (1 or 2): "))
        if choice not in [1, 2]:
            print("\nInvalid number. Please type 1 or 2")
            return

        reviews = load_reviews(filename)
        scores = []
        classifications = []
        analysis_method = "vader" if choice == 1 else "textblob"

        for review in reviews:
            score = analyze_sentiment_vader(review) if choice == 1 else analyze_sentiment_blob(review)
            sentiment = classify_sentiment(score)
            scores.append(score)
            classifications.append(sentiment)

        save_analysis_results(filename, reviews, scores, classifications, analysis_method)
    except ValueError:
        print("\nInvalid choice. Please type 1 or 2")

def handle_statistics():
    results_dir = "results"
    if not os.path.exists(results_dir):
        print("\nNo analysis results found. Please analyze a file first (Option 2 in menu)")
        return

    analysis_files = [f for f in os.listdir(results_dir) 
                     if f.endswith(("_sentiment_vader.csv", "_sentiment_textblob.csv"))]
    if not analysis_files:
        print("\nNo analysis results found. Please analyze a file first (Option 2 in menu)")
        return

    print("\nAvailable analysis results:")
    for i, f in enumerate(analysis_files, 1):
        print(f"{i}. {f}")

    while True:
        try:
            file_choice = input("\nEnter the number of the analysis result to view (or 0 to exit): ")
            if file_choice == "0":
                break
            
            file_index = int(file_choice) - 1
            if 0 <= file_index < len(analysis_files):
                file_path = os.path.join(results_dir, analysis_files[file_index])
                stats = calculate_statistics(file_path)
                display_statistics(stats)
                break
            print("Invalid file number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = None
    while True:
        display_menu()
        choice = input("Enter your choice (0-3): ")

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            filename = handle_file_selection()
        elif choice == "2":
            handle_analysis(filename)
        elif choice == "3":
            handle_statistics()
        else:
            print("\nInvalid choice. Please type a number from the menu")

if __name__ == "__main__":
    main()