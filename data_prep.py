"""
Loading and prepareing the dataset

The data is cached so Streamlit does not reload and process the CSV every time the application reruns.

The code is otherwise the same as in the jupyter notebook
"""

import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_data():
    # Read data
    df = pd.read_csv("reservoirs.csv")

    # Rename Norwegian column names to understandable English names
    df = df.rename(columns={
        "dato_Id": "date_id",
        "omrType": "area_type",
        "omrnr": "area_number",
        "iso_aar": "iso_year",
        "iso_uke": "iso_week",
        "fyllingsgrad": "fill_level",
        "kapasitet_TWh": "capacity_TWh",
        "fylling_TWh": "stored_energy_TWh",
        "neste_Publiseringsdato": "next_publication_date",
        "fyllingsgrad_forrige_uke": "fill_level_previous_week",
        "endring_fyllingsgrad": "change_in_fill_level"
    })

    # Convert observation date to datetime
    df["date_id"] = pd.to_datetime(df["date_id"])

    # Sort the dataset chronologically
    df = df.sort_values("date_id")

    return df