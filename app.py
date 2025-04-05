import streamlit as st
import pandas as pd
from profile_step import profile_step

st.set_page_config(layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>🧪 DataAssure: A Data Validation App</h1>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    try:
        df.drop(columns = ['Unnamed: 0'], inplace=True)
    except:
        pass
    st.success("✅ File uploaded successfully!")

    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    expectations = {}
    col_list = df.columns.tolist()

    st.subheader("⚙️ Configure Your Expectations")

    if st.checkbox("✅ expect_no_nulls"):
        selected = st.multiselect("Columns that should not have nulls", col_list)
        expectations["expect_no_nulls"] = selected

    if st.checkbox("✅ expect_column_values_to_be_in_set"):
        col = st.selectbox("Column", col_list, key="in_set_col")
        values = st.text_input("Allowed values (comma separated)", value="yes,no")
        if col and values:
            expectations["expect_column_values_to_be_in_set"] = {col: [v.strip() for v in values.split(",")]}

    if st.checkbox("✅ expect_column_values_to_be_unique"):
        selected = st.multiselect("Columns that must be unique", col_list, key="unique_cols")
        expectations["expect_column_values_to_be_unique"] = selected

    if st.checkbox("✅ expect_column_values_to_be_between"):
        col = st.selectbox("Column", col_list, key="between_col")
        min_val = st.number_input("Min Value", key="min_val")
        max_val = st.number_input("Max Value", key="max_val")
        expectations["expect_column_values_to_be_between"] = {col: (min_val, max_val)}

    if st.checkbox("✅ expect_column_dtype_to_be"):
        col = st.selectbox("Column", col_list, key="dtype_col")
        dtype = st.text_input("Expected dtype (e.g., int64, float64, object)", value="int64")
        expectations["expect_column_dtype_to_be"] = {col: dtype}

    if st.checkbox("✅ expect_column_mean_to_be_between"):
        col = st.selectbox("Column", col_list, key="mean_col")
        min_val = st.number_input("Min Mean", key="min_mean")
        max_val = st.number_input("Max Mean", key="max_mean")
        expectations["expect_column_mean_to_be_between"] = {col: (min_val, max_val)}

    if st.checkbox("✅ expect_column_median_to_be_between"):
        col = st.selectbox("Column", col_list, key="median_col")
        min_val = st.number_input("Min Median", key="min_median")
        max_val = st.number_input("Max Median", key="max_median")
        expectations["expect_column_median_to_be_between"] = {col: (min_val, max_val)}

    if st.checkbox("✅ expect_column_max_to_be_between"):
        col = st.selectbox("Column", col_list, key="max_col")
        min_val = st.number_input("Min Max", key="min_max_val")
        max_val = st.number_input("Max Max", key="max_max_val")
        expectations["expect_column_max_to_be_between"] = {col: (min_val, max_val)}

    if st.checkbox("✅ expect_column_min_to_be_between"):
        col = st.selectbox("Column", col_list, key="min_col")
        min_val = st.number_input("Min Min", key="min_min_val")
        max_val = st.number_input("Max Min", key="max_min_val")
        expectations["expect_column_min_to_be_between"] = {col: (min_val, max_val)}

    if st.checkbox("✅ expect_column_std_to_be_less_than"):
        col = st.selectbox("Column", col_list, key="std_col")
        threshold = st.number_input("Max Std Dev", key="std_val")
        expectations["expect_column_std_to_be_less_than"] = {col: threshold}

    if st.checkbox("✅ expect_column_value_lengths_to_be_between"):
        col = st.selectbox("Column", col_list, key="len_col")
        min_len = st.number_input("Min Length", key="min_len")
        max_len = st.number_input("Max Length", key="max_len")
        expectations["expect_column_value_lengths_to_be_between"] = {col: (min_len, max_len)}

    if st.checkbox("✅ expect_table_row_count_to_be_between"):
        min_rows = st.number_input("Min Row Count", key="min_rows", value=1)
        max_rows = st.number_input("Max Row Count", key="max_rows", value=100000)
        expectations["expect_table_row_count_to_be_between"] = (min_rows, max_rows)

    if st.checkbox("✅ expect_column_proportion_of_unique_values_to_be_between"):
        col = st.selectbox("Column", col_list, key="uniq_ratio_col")
        low = st.number_input("Min Ratio", key="min_ratio", min_value=0.0, max_value=1.0, value=0.0)
        high = st.number_input("Max Ratio", key="max_ratio", min_value=0.0, max_value=1.0, value=1.0)
        expectations["expect_column_proportion_of_unique_values_to_be_between"] = {col: (low, high)}

    if st.checkbox("✅ expect_column_pair_values_to_be_unique"):
        col1 = st.selectbox("Column 1", col_list, key="pair_col1")
        col2 = st.selectbox("Column 2", col_list, key="pair_col2")
        expectations["expect_column_pair_values_to_be_unique"] = [(col1, col2)]

    if st.checkbox("✅ expect_column_values_to_not_match_regex"):
        col = st.selectbox("Column", col_list, key="not_regex_col")
        pattern = st.text_input("Forbidden Regex Pattern", value=r"\d", key="not_regex_pattern")
        expectations["expect_column_values_to_not_match_regex"] = {col: pattern}

    if st.checkbox("✅ expect_column_values_to_match_regex"):
        col = st.selectbox("Column", col_list, key="match_regex_col")
        pattern = st.text_input("Required Regex Pattern", value=r"^[a-zA-Z]+$", key="match_regex_pattern")
        expectations["expect_column_values_to_match_regex"] = {col: pattern}

    if st.checkbox("✅ expect_column_values_to_not_be_in_set"):
        col = st.selectbox("Column", col_list, key="notin_col")
        bad_vals = st.text_input("Forbidden values (comma separated)", value="none,unknown")
        expectations["expect_column_values_to_not_be_in_set"] = {col: [v.strip() for v in bad_vals.split(",")]}

    if st.checkbox("✅ expect_column_most_common_value_to_be"):
        col = st.selectbox("Column", col_list, key="mode_col")
        expected_mode = st.text_input("Expected Most Common Value")
        expectations["expect_column_most_common_value_to_be"] = {col: expected_mode}

    if st.checkbox("✅ expect_table_columns_to_match_ordered_list"):
        expected_order = st.text_input("Expected column order (comma separated)", value=",".join(col_list))
        ordered_list = [col.strip() for col in expected_order.split(",")]
        expectations["expect_table_columns_to_match_ordered_list"] = ordered_list

    # Submit button
    if st.button("🚀 Run Validation"):
        st.subheader("📋 Validation Report")

        @profile_step(**expectations)
        def validate_uploaded_data():
            return df

        validate_uploaded_data()

        with open("validation_report.txt", "r", encoding="utf-8") as f:
            report_content = f.read()

        st.text_area("📄 Validation Summary", value=report_content, height=300)

        st.download_button(
            label="⬇️ Download Full Validation Report",
            data=report_content,
            file_name="validation_report.txt",
            mime="text/plain"
        )
