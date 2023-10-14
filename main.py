import streamlit as st
import pandas as pd
import numpy as np
import os
import shutil
import zipfile
import time

np.bool_ = bool  # Correct the assignment

def split_csv(input_file, output_prefix, chunk_size=200):
    output_directory = None
    try:
        # Create a unique output directory based on the timestamp
        timestamp = int(time.time())
        output_directory = f"output_data_{timestamp}"
        os.makedirs(output_directory, exist_ok=True)

        # Read the CSV file, explicitly specifying the 'dtype' parameter for columns
        df = pd.read_csv(input_file, dtype=str)

        # Replace empty cells with an empty string
        df = df.fillna('')

        total_rows = len(df)
        num_files = total_rows // chunk_size + 1

        output_files = []  # List to store output files

        for i in range(num_files):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size
            chunk_df = df[start_idx:end_idx]

            output_file_name = f"{output_prefix}_{i + 1}.csv"
            output_files.append(output_file_name)  # Store the output file name in the list

            output_file = os.path.join(output_directory, output_file_name)
            chunk_df.to_csv(output_file, index=False)

        # Create a ZIP archive containing the split files
        zip_filename = f"{output_prefix}_split_files.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_name in output_files:
                file_path = os.path.join(output_directory, file_name)
                zipf.write(file_path, os.path.basename(file_path))

        st.success("CSV split successfully!")

        # Provide a download link for the ZIP file
        st.subheader("Download Split Files")
        st.markdown(f"Download: [ZIP File]({zip_filename})")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    finally:
        
        # Cleanup: Remove the output directory and ZIP file after processing
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory, ignore_errors=True)
        if os.path.exists(zip_filename):
            os.remove(zip_filename)


st.set_page_config(
    page_title="CSV Splitter App",
    page_icon="✂️",
    layout="wide"
)

st.title("CSV Splitter App")

main_csv_file = st.file_uploader("Upload the main CSV file", type=["csv"])
if main_csv_file is not None:
    st.markdown("---")
    output_prefix = st.text_input("Output File Prefix", "chunked_data")
    chunk_size = st.number_input("Chunk Size", min_value=1, value=200)

    if st.button("Split CSV"):
        if output_prefix and chunk_size:
            split_csv(main_csv_file, output_prefix, chunk_size)

st.sidebar.title("About")
st.sidebar.info(
    "This is a Python app for splitting a large CSV file into smaller chunks. "
    "Upload your CSV file, specify the output prefix, and chunk size, then click the 'Split CSV' button. The output directory is cleaned up after processing."
)
