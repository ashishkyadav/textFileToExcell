import streamlit as st
import pandas as pd
import re
import io

def extract_and_save_scores(file):
    # Initialize lists to store the extracted information
    file_names = []
    scores = []

    # Read the file
    lines = file.readlines()
    lines = [line.decode("utf-8") for line in lines]  # Convert bytes to string

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

    # Save the DataFrame to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    return output

# Streamlit UI
st.title("Text File to Excel Converter")
st.write("Upload a text file, and the corresponding Excel file will be generated and downloaded.")

uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file is not None:
    # Process the file
    output = extract_and_save_scores(uploaded_file)

    # Generate the download link for the Excel file
    output_file_name = uploaded_file.name.replace(".txt", ".xlsx")
    st.download_button(label="Download Excel file", data=output, file_name=output_file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
