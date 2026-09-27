import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# From my own file data_prep.py
from data_prep import load_data


st.title("Reservoir Plots")

# Load data
df = load_data()

# Keep only the national data
df_no = df[
    (df["area_type"] == "NO") &
    (df["area_number"] == 0)
].copy()

# Sort by date
df_no = df_no.sort_values("date_id")


# Columns we want to plot
columns = [
    "fill_level",
    "capacity_TWh",
    "stored_energy_TWh",
    "fill_level_previous_week",
    "change_in_fill_level"
]


# Dropdown menu
selected_column = st.selectbox(
    "Choose a column",
    ["All columns"] + columns
)


# Create month values
df_no["month"] = df_no["date_id"].dt.to_period("M").astype(str)
months = df_no["month"].unique()


# Month slider
start_month, end_month = st.select_slider(
    "Choose month range",
    options=months,
    value=(months[0], months[0])
)


# Keep only the selected months
filtered_df = df_no[
    (df_no["month"] >= start_month) &
    (df_no["month"] <= end_month)
]



# Create plot
plt.figure(figsize=(12, 6))

if selected_column == "All columns":
    # Normalize so columns with different scales can be compared
    normalized = (
        filtered_df[columns] - filtered_df[columns].min()
    ) / (
        filtered_df[columns].max() - filtered_df[columns].min()
    )

    for column in columns:
        plt.plot(
            filtered_df["date_id"],
            normalized[column],
            label=column
        )

    plt.ylabel("Normalized value")
    plt.legend()

else:
    plt.plot(
        filtered_df["date_id"],
        filtered_df[selected_column]
    )

    plt.ylabel(selected_column)

plt.title("Norwegian Reservoir Data")
plt.xlabel("Date")
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)