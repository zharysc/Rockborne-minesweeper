
# ========= score_loading.py ============= # 
"""
 This script includes functions involving the loading and storing
of scores and players

To keep a record of score history we will be using a file called 
    scores_history.csv.
"""
## === Imports
import os
import csv
import datetime

## ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scores_csv = os.path.join(BASE_DIR, "scores_history.csv")

def load_scores(top_n=3):
    """
    function loads scores_csv, and will take the top 3 score on this local device

    Parameters:
        top_n - int, N number of top scores we want to grab
    Returns:
        formatted - array, list of the top scorers and scores, in appropriate formatting
    """
    records = []
    try:
        with open(scores_csv, newline="", encoding="utf‑8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    s = int(row["score"])
                except (KeyError, ValueError):
                    continue
                name = row.get("player_name", "")
                # Formatting
                records.append((name, s))
        # sort descending by score
        records.sort(key=lambda ns: ns[1], reverse=True)

        # Formatted here for proper display
        formatted = [f"{name}-{score}" for (name, score) in records[:top_n]]
        return formatted

    except FileNotFoundError:
        # If no file found an empty list is created
        records = []
    except Exception as e:
        print(f"Score load error - Could not load scores file: {e}")
        records = []


def save_scores(name, score):
    """
    When called saves the name of player and score
    Parameters:
        name - str, name of player
        score - int, score of player
    Returns:
    
    """
    try:
        file_exists = os.path.exists(scores_csv)
        with open(scores_csv, "a", newline="", encoding="utf‑8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["player_name", "score", "date"])
            writer.writerow([name, score, datetime.datetime.now().isoformat()])
    except FileNotFoundError as e:
        # File path is invalid
        print(f"Error: scores file not found: {e}")
    except PermissionError as e:
        # No permission to write to file
        print(f"Error: cannot write to scores file (permission denied): {e}")
    except Exception as e:
        # Catch all other exceptions
        print(f"Unexpected error when saving scores: {e}")

## ======= load_scores debugging
if __name__ == "__main__":
    print(f"Path to csv:{scores_csv}")
    print(f"load_score returned list: {load_scores()}")