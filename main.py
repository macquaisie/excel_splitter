import streamlit as st
import pandas as pd
import numpy as np
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

        output_files = {}  # Dictionary to store output files

        for i in range(num_files):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size
            chunk_df = df[start_idx:end_idx]

            output_file_name = f"{output_prefix}_{i + 1}.csv"
            output_files[output_file_name] = chunk_df.to_csv(index=False)

        st.success("CSV split successfully!")

        # Provide a download button for each split file
        st.subheader("Download Split Files")
        for output_file_name, output_file_data in output_files.items():
            b64 = base64.b64encode(output_file_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{output_file_name}">Download {output_file_name}</a>'
            st.markdown(href, unsafe_allow_html=True)

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
    "Upload your CSV file, specify the output prefix, and chunk size, then click the 'Split CSV' button. The split files can be downloaded individually."
)
