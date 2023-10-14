import streamlit as st
import pandas as pd
import numpy as np
import os
import zipfile
import io
import base64
import time

np.bool_ = bool  # Correct the assignment

def split_csv(input_file, output_prefix, chunk_size=200):
    try:
        # Read the CSV file, explicitly specifying the 'dtype' parameter for columns
        df = pd.read_csv(input_file, dtype=str)

        # Replace empty cells with an empty string
        df = df.fillna('')

        total_rows = len(df)
        num_files = total_rows // chunk_size + 1

        zip_buffer = io.BytesIO()  # Create an in-memory zip file

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i in range(num_files):
                start_idx = i * chunk_size
                end_idx = (i + 1) * chunk_size
                chunk_df = df[start_idx:end_idx]

                output_file_name = f"{output_prefix}_{i + 1}.csv"
                csv_data = chunk_df.to_csv(index=False, encoding='utf-8')

                # Add the CSV data as a file to the zip
                zipf.writestr(output_file_name, csv_data)

        st.success("CSV split successfully!")

        # Provide a download link for the ZIP file
        st.subheader("Download Split Files")
        zip_data = zip_buffer.getvalue()
        b64 = base64.b64encode(zip_data).decode()
        st.markdown(f"Download: [ZIP File]({b64})")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

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
    "Upload your CSV file, specify the output prefix, and chunk size, then click the 'Split CSV' button. The output files are stored in a ZIP file and can be downloaded without being physically saved."
)
