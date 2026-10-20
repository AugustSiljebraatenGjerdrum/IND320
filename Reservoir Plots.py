import streamlit as st
import pandas as pd
from data_prep import load_data

st.title("Reservoir Plots")
try:
    df = load_data()
except Exception as error:
    st.error(f"NVE download failed: {error}")
    st.stop()

area_type = st.radio("Choose area type", ["NO", "EL", "VASS"], horizontal=True)
measurement = st.selectbox("Choose measurement", ["fill_level", "capacity_TWh", "stored_energy_TWh"])

# Choose time interval. NVE's HentOffentligData endpoint does NOT accept dates:
# this filters the API result, rather than changing the server download.
min_date = df["date_id"].min().date()
max_date = df["date_id"].max().date()
if min_date == max_date:
    st.warning("Only one observation date was returned")
    start_date = end_date = min_date
else:
    start_date, end_date = st.slider(
        "Choose date interval", min_value=min_date, max_value=max_date,
        value=(min_date, max_date)
    )

selected = df[
    (df["area_type"] == area_type)
    & (df["date_id"].dt.date >= start_date)
    & (df["date_id"].dt.date <= end_date)
].copy()

if selected.empty:
    st.warning("No observations for this selection")
    st.stop()

# Rows are dates, columns are area numbers, values are filling measurements.
chart = selected.pivot_table(index="date_id", columns="area_number", values=measurement)
chart.columns = [f"Area {number}" for number in chart.columns]
st.line_chart(chart)
st.caption("Each line represents an area number. The selection filters data already downloaded from NVE.")

with st.expander("How the date selection works"):
    st.write("NVE's HentOffentligData API endpoint returns the dataset without date request parameters. The app downloads the dataset (with caching), then limits the displayed data to your selected dates.")
