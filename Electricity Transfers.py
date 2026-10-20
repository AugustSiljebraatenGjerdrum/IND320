import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

st.title("Electricity Transfers")
st.write("Electricity imports and exports from the ENTSO-E API, prepared in Jupyter and stored in MongoDB.")

# This page expects two curated MongoDB collections:
# annual: connection, direction, year, total_mwh
# daily: connection, direction, year, month, date, mean_mw
# The MongoDB upload step has not been completed yet.
if "MONGODB_URI" not in st.secrets:
    st.warning("MongoDB has not been configured yet. Add MONGODB_URI to Streamlit secrets.")
    st.stop()

try:
    client = MongoClient(st.secrets["MONGODB_URI"], serverSelectionTimeoutMS=8000)
    client.admin.command("ping")
    database = client["ind320"]
    annual = pd.DataFrame(list(database["annual"].find({}, {"_id": 0})))
    daily = pd.DataFrame(list(database["daily"].find({}, {"_id": 0})))
except Exception as error:
    st.error(f"Unable to read MongoDB: {error}")
    st.stop()

if annual.empty or daily.empty:
    st.warning("MongoDB is connected, but the annual/daily collections are empty. Upload prepared data from the notebook first.")
    st.stop()

needed_annual = {"connection", "direction", "year", "total_mwh"}
needed_daily = {"connection", "direction", "year", "month", "date", "mean_mw"}
if not needed_annual.issubset(annual.columns) or not needed_daily.issubset(daily.columns):
    st.error("MongoDB field names do not match the expected annual/daily tables; check the upload code.")
    st.stop()

connections = sorted(annual["connection"].dropna().unique().tolist())
left, right = st.columns(2)
with left:
    st.subheader("Annual import vs export")
    connection = st.radio("Choose connection", connections)
    years = sorted(annual.loc[annual["connection"] == connection, "year"].dropna().astype(int).unique())
    year = st.selectbox("Choose year", years)
    pie = annual[(annual["connection"] == connection) & (annual["year"].astype(int) == year)]
    totals = pie.groupby("direction")["total_mwh"].sum()
    if len(totals) < 2 or (totals < 0).any() or totals.sum() <= 0:
        st.warning("Both directions need valid energy totals for a pie chart")
    else:
        fig, ax = plt.subplots()
        ax.pie(totals.values, labels=totals.index, autopct="%1.1f%%")
        ax.set_title(f"{connection}, {year}")
        st.pyplot(fig)
        plt.close(fig)

with right:
    st.subheader("Daily electricity flow")
    choices = list(range(1, 13))
    months = st.pills("Choose months", choices, selection_mode="multi", default=[1])
    # Show ALL connections and both directions, as in the notebook.
    subset = daily[
        (daily["year"].astype(int) == year)
        & (daily["month"].astype(int).isin(months or []))
    ].copy()
    if subset.empty:
        st.info("No data for this selection")
    else:
        subset["date"] = pd.to_datetime(subset["date"])
        subset["line"] = subset["connection"] + " - " + subset["direction"]
        chart = subset.pivot_table(index="date", columns="line", values="mean_mw")
        st.line_chart(chart)

with st.expander("Where does this data come from?"):
    st.write("Source: ENTSO-E Transparency Platform cross-border physical electricity flows. Data should be downloaded for Norwegian connections, checked for missing periods, converted from MW to MWh using observation durations, and prepared in Jupyter before upload to MongoDB.")
