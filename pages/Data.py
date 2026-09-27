import streamlit as st
import pandas as pd
# From my own file data_prep.py
from data_prep import load_data


st.title("Reservoir Data")

# Load the prepared data
df = load_data()

# Show some of the original data
st.subheader("Imported data")
st.dataframe(df.head(20))


# Keep only the national data
df_no = df[
    (df["area_type"] == "NO") &
    (df["area_number"] == 0)
].copy()


# Create a month column
df_no["month"] = df_no["date_id"].dt.to_period("M")

# Find the first month
first_month = df_no["month"].min()

# Keep only rows from the first month
first_month_df = df_no[
    df_no["month"] == first_month
]


st.subheader(f"First month: {first_month}")


# Choose the columns that make sense to show as mini line charts
columns = [
    "fill_level",
    "capacity_TWh",
    "stored_energy_TWh",
    "fill_level_previous_week",
    "change_in_fill_level"
]


# Make a small table
table = pd.DataFrame({
    "Column": columns,
    "First month": [
        first_month_df[column].tolist()
        for column in columns
    ]
})


# Show mini line charts inside the table
st.dataframe(
    table,
    hide_index=True,
    column_config={
        "First month": st.column_config.LineChartColumn(
            "First month"
        )
    }
)
