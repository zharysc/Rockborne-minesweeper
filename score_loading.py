''' This script includes functions involving the loading and storing
of scores and players'''
## === Imports
import os
import csv
import datetime

## ==== Score History ==== ##
""" To keep a record of score history we will be using a file called 
    scores_history.csv.
    This will keep the top 3 scores on the local device and will include:
    Name
    Score
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scores_csv = os.path.join(BASE_DIR, "scores_history.csv")

def load_scores(top_n=3):

    records = []
    if os.path.exists(scores_csv):
        print()
        with open(scores_csv, newline="", encoding="utf‑8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    s = int(row["score"])
                except (KeyError, ValueError):
                    continue
                name = row.get("player_name", "")
                # Formatting
                records.append(f"{name}-{s}")
    # sort descending by score
    records.sort(key=lambda ns: ns[1], reverse=True)
    return records[:top_n]

def save_scores(name, score):
    file_exists = os.path.exists(scores_csv)
    with open(scores_csv, "a", newline="", encoding="utf‑8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["player_name", "score", "date"])
        writer.writerow([name, score, datetime.datetime.now().isoformat()])

## ======= load_scores debugging
if __name__ == "__main__":
    print(f"Path to csv:{scores_csv}")
    print(f"load_score returned list: {load_scores()}")