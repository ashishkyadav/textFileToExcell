import re
import pandas as pd

def extract_and_save_scores(input_file_path, output_file_path):
    # Initialize lists to store the extracted information
    file_names = []
    scores = []

    # Read the file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Regular expressions to match the filename and score lines
    filename_pattern = re.compile(r"==> (.+\.pdbqt_log\.log) <==")
    score_pattern = re.compile(r"^\s*1\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)")

    # Iterate through lines and extract the needed information
    for line in lines:
        filename_match = filename_pattern.match(line)
        if filename_match:
            current_filename = filename_match.group(1)

        score_match = score_pattern.match(line)
        if score_match:
            score = f"{score_match.group(1)} {score_match.group(2)} {score_match.group(3)}"
            file_names.append(current_filename)
            scores.append(score)

    # Create a DataFrame to hold the extracted information
    data = {
        "Filename": file_names,
        "Score": scores
    }
    df = pd.DataFrame(data)

    # Export the DataFrame to an Excel file
    df.to_excel(output_file_path, index=False)

    print(f"Data extracted and saved to {output_file_path}")

# Example usage
input_file_path = "C:\\Users\\ashis\\Downloads\\ULK1_results_2.txt"
output_file_path = "C:\\Users\\ashis\\Downloads\\Reshmi\\ULK1_results_2.xlsx"

extract_and_save_scores(input_file_path, output_file_path)
