import streamlit as st
import datetime

st.title("Daten Forward eingeben")

# Session State initialisieren
if "valuation_date" not in st.session_state:
    st.session_state.valuation_date = datetime.date(2025, 12, 31)
if "maturity_date" not in st.session_state:
    st.session_state.maturity_date = datetime.date(2026, 12, 31)
if "nominal_sold" not in st.session_state:
    st.session_state.nominal_sold = 1000000.0
if "contract_rate" not in st.session_state:
    st.session_state.contract_rate = 1.0
if "spot_rate" not in st.session_state:
    st.session_state.spot_rate = 1.0
if "foreign_country_name" not in st.session_state:
    st.session_state.foreign_country_name = "US Dollar"

# Widgets mit key-Parameter - Werte werden automatisch gespeichert
valuation_date = st.date_input(
    "Bewertungsstichtag", 
    value=st.session_state.valuation_date,
    key="valuation_date"
)
maturity_date = st.date_input(
    "Fälligkeitstermin",
    value=st.session_state.maturity_date,
    key="maturity_date"
)
nominal_sold = st.number_input(
    "Verkaufte Summe (EUR)", 
    min_value=0.0, 
    value=st.session_state.nominal_sold,
    key="nominal_sold"
)
contract_rate = st.number_input(
    "Contract Rate (Wechselkurs)", 
    min_value=0.0, 
    value=st.session_state.contract_rate,
    format="%.4f",
    help="z.B. 1.1200 für EUR/USD",
    key="contract_rate"
)
spot_rate = st.number_input(
    "Aktueller Spot Rate (Wechselkurs)", 
    min_value=0.0, 
    value=st.session_state.spot_rate,
    format="%.4f",
    help="z.B. 1.1050 für EUR/USD",
    key="spot_rate"
)

dataframe_foreign_1 = st.file_uploader(
    "CSV-Datei mit historischen Zinsdaten hochladen", 
    type=["csv"],
    key="dataframe_foreign_1"
)
dataframe_foreign_2 = st.file_uploader(
    "CSV-Datei mit historischen Zinsdaten hochladen", 
    type=["csv"], 
    help="Für US Dollar sind je nach Szenario 2 CSV nötig.",
    key="dataframe_foreign_2"
)
foreign_country_name = st.selectbox(
    "Partnerwährung", 
    options=["US Dollar", "Schweizer Franken", "Britisches Pfund"], 
    index=["US Dollar", "Schweizer Franken", "Britisches Pfund"].index(st.session_state.foreign_country_name),
    key="foreign_country_name"
)

if st.button("Berechnung vorbereiten", type="primary"):
    st.session_state.input_data = {
        "valuation_date": st.session_state.valuation_date,
        "maturity_date": st.session_state.maturity_date,
        "nominal": st.session_state.nominal_sold,
        "contract_rate": st.session_state.contract_rate,
        "spot_rate": st.session_state.spot_rate,
        "dataframe_foreign_1": st.session_state.dataframe_foreign_1,
        "dataframe_foreign_2": st.session_state.dataframe_foreign_2,
        "foreign_country_name": st.session_state.foreign_country_name
    }
    st.success("Daten gespeichert! Zu Result wechseln.")
