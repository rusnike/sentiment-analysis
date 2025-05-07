import os
import pandas as pd

def load_reviews(filename):
    try:
        if filename.endswith((".csv", ".txt")):
            with open(filename, "r", encoding="utf-8") as file:
                reviews = [line.strip() for line in file if line.strip()]
            return reviews
        else:
            print("Unsupported format. Please use .txt or .csv file formats")
            return []
    except Exception as e:
        print("Error loading file:", e)
        return []

def save_analysis_results(filename, reviews, scores, classifications, analysis_method):
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    base_filename = os.path.basename(filename)
    output_filename = f"{os.path.splitext(base_filename)[0]}_sentiment_{analysis_method}.csv"
    output_path = os.path.join(results_dir, output_filename)

    if not reviews:
        print("No reviews to save. The file is empty or could not be loaded.")
        return

    try:
        data = {
            "Review": reviews,
            "Sentiment Score": scores,
            "Sentiment Classification": classifications,
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"\nSentiment Analysis results saved to '{output_path}'")
    except Exception as e:
        print(f"Error while saving: {e}")

def get_available_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]        