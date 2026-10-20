import streamlit as st
import pandas as pd
from data_prep import load_data

st.title("Reservoir Data")

try:
    df = load_data()
except Exception as error:
    st.error(f"NVE download failed: {error}")
    st.stop()

# Switch between Norway, electricity price areas, and drainage regions.
area_type = st.radio("Choose area type", ["NO", "EL", "VASS"], horizontal=True)
selected = df[df["area_type"] == area_type].copy()

if selected.empty:
    st.warning("No data for this area type")
    st.stop()

# All areas are displayed, each with its own small line graph.
st.subheader("Small graphs for every area number")
rows = []
for number, group in selected.groupby("area_number"):
    group = group.sort_values("date_id")
    rows.append({"Area number": number, "Filling level history": group["fill_level"].dropna().tolist()})

st.dataframe(
    pd.DataFrame(rows),
    hide_index=True,
    column_config={"Filling level history": st.column_config.LineChartColumn("Filling level")},
    use_container_width=True
)

# Give users a way to inspect the underlying observations.
st.subheader("Data table")
st.dataframe(selected, use_container_width=True)
