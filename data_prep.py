# """
# Loading and prepareing the dataset

# The data is cached so Streamlit does not reload and process the CSV every time the application reruns.

# The code is otherwise the same as in the jupyter notebook
# """

# import pandas as pd
# import streamlit as st
# import requests


# @st.cache_data
# def load_data():
#     # Download reservoir statistics directly from NVE
#     url = "https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData"

#     response = requests.get(url)
#     response.raise_for_status()

#     # Convert JSON data into a DataFrame
#     df = pd.json_normalize(response.json())

#     # Rename Norwegian column names to understandable English names
#     df = df.rename(columns={
#         "dato_Id": "date_id",
#         "omrType": "area_type",
#         "omrnr": "area_number",
#         "iso_aar": "iso_year",
#         "iso_uke": "iso_week",
#         "fyllingsgrad": "fill_level",
#         "kapasitet_TWh": "capacity_TWh",
#         "fylling_TWh": "stored_energy_TWh",
#         "neste_Publiseringsdato": "next_publication_date",
#         "fyllingsgrad_forrige_uke": "fill_level_previous_week",
#         "endring_fyllingsgrad": "change_in_fill_level"
#     })

#     # Convert observation date to datetime
#     df["date_id"] = pd.to_datetime(df["date_id"])

#     # Sort the dataset chronologically
#     df = df.sort_values("date_id")

#     return df


"""Download reservoir data from NVE, and give columns easy names."""
import pandas as pd
import requests
import streamlit as st

@st.cache_data(ttl=3600)
def load_data():
    # NVE provides all published observations from this endpoint.
    url = "https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    df = pd.json_normalize(response.json())
    df = df.rename(columns={
        "dato_Id": "date_id", "omrType": "area_type", "omrnr": "area_number",
        "iso_aar": "iso_year", "iso_uke": "iso_week",
        "fyllingsgrad": "fill_level", "kapasitet_TWh": "capacity_TWh",
        "fylling_TWh": "stored_energy_TWh",
        "fyllingsgrad_forrige_uke": "fill_level_previous_week",
        "endring_fyllingsgrad": "change_in_fill_level"
    })
    df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    return df.dropna(subset=["date_id"]).sort_values("date_id")
