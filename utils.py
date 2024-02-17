import os

def save_high_score(full_file_path: str, score: int):
    """
    Check if current score is greater than the current score

    Parameters:
        - full_file_path - the full file path where the file is stored
        - score - the score of the game that just finished
    """

    # Get the highest score of all time (from the file)
    current_high_score = load_high_socre(full_file_path)
    # Convert None to 0 so the game doesn't break
    current_high_score = 0 if isinstance(current_high_score, type(None)) else current_high_score
    
    # Do not save the current score if it's not a "new highest record"
    if score < current_high_score: return

    binary_data = str(score).encode("utf-8")

    with open(full_file_path, "wb") as f:
        f.write(binary_data)
    

    
def load_high_socre(full_file_path: str) -> int:
    """
    Load the  high score data if it exists

    Parameters:
        - full_file_path - the full file path where the file is stored

    Output:
        - if the file exists the highest score is returned.
          if the file does not exist then None is returned.
    """
    # Check if file exists
    if not os.path.exists(full_file_path):
        return None
    
    # Read previous high score
    with open(full_file_path, "rb") as f:
        return int(f.read().decode())