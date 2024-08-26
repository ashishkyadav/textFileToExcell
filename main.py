import streamlit as st
import pandas as pd
import re
import io


def extract_and_save_scores(file):
    # Initialize lists to store the extracted information
    file_names = []
    scores = []

    # Read the uploaded file
    content = file.read().decode("utf-8")
    lines = content.splitlines()

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
            score = score_match.group(1)  # Only take the first score
            file_names.append(current_filename)
            scores.append(score)

    # Create a DataFrame to hold the extracted information
    data = {
        "Filename": file_names,
        "Score": scores
    }
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file in memory
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output


# Streamlit UI
st.title("Extracting Drugs and Score")

# Note
st.markdown("""
**Note:**
- Only text files can be uploaded which should be less than 200MB.
- The uploaded file will be downloadable with the same filename.
- Every month, provide a treat as a token of appreciation; otherwise, I have the right to terminate this web application.
""")

# File uploader widget
uploaded_file = st.file_uploader("Upload a text file", type="txt")

if uploaded_file:
    # Extract original filename without extension
    original_filename = uploaded_file.name
    base_filename = original_filename.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.xlsx"

    # Process the file and get the output
    output = extract_and_save_scores(uploaded_file)

    # Provide download link for the processed file
    st.download_button(
        label="Download Processed File",
        data=output,
        file_name=output_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
