import streamlit as st
import datetime

st.title("Daten Forward eingeben")
st.subheader("Verkauf Fremdwährung")

# Session State initialisieren (eigene Keys fuer dieses Szenario)
if "valuation_date_fx" not in st.session_state:
    st.session_state.valuation_date_fx = datetime.date(2025, 12, 31)
if "maturity_date_fx" not in st.session_state:
    st.session_state.maturity_date_fx = datetime.date(2026, 12, 31)
if "nominal_sold_fx" not in st.session_state:
    st.session_state.nominal_sold_fx = 1000000.0
if "contract_rate_fx" not in st.session_state:
    st.session_state.contract_rate_fx = 1.0
if "spot_rate_fx" not in st.session_state:
    st.session_state.spot_rate_fx = 1.0
if "foreign_country_name_fx" not in st.session_state:
    st.session_state.foreign_country_name_fx = "US Dollar"

# Widgets mit key-Parameter - Werte werden automatisch gespeichert
st.date_input(
    "Bewertungsstichtag",
    key="valuation_date_fx"
)
st.date_input(
    "Faelligkeitstermin",
    key="maturity_date_fx"
)
st.number_input(
    "Verkaufte Summe (Fremdwaehrung)",
    min_value=0.0,
    key="nominal_sold_fx"
)
st.number_input(
    "Contract Rate (Wechselkurs)",
    min_value=0.0,
    format="%.4f",
    help="z.B. 0.8929 fuer USD/EUR",
    key="contract_rate_fx"
)
st.number_input(
    "Aktueller Spot Rate (Wechselkurs)",
    min_value=0.0,
    format="%.4f",
    help="z.B. 0.9050 fuer USD/EUR",
    key="spot_rate_fx"
)

st.selectbox(
    "Partnerwaehrung",
    options=["US Dollar", "Schweizer Franken", "Britisches Pfund"],
    key="foreign_country_name_fx"
)

if st.session_state.foreign_country_name_fx == "US Dollar":
    dataframe_foreign_1 = st.file_uploader(
        "CSV-Datei mit historischen Zinsdaten hochladen",
        type=["csv"],
        key="dataframe_foreign_1_fx"
    )
    dataframe_foreign_2 = st.file_uploader(
        "CSV-Datei mit historischen Zinsdaten hochladen",
        type=["csv"],
        help="Fuer US Dollar sind je nach Szenario 2 CSV noetig.",
        key="dataframe_foreign_2_fx"
    )
else:
    dataframe_foreign_1 = None
    dataframe_foreign_2 = None

if st.session_state.foreign_country_name_fx == "Schweizer Franken":
    st.info("Zinsstrukturkurve fuer Schweizer Franken wird automatisch ueber API bezogen.")

if st.session_state.foreign_country_name_fx == "Britisches Pfund":
    st.warning("Britisches Pfund ist noch nicht implementiert.")

if st.button("Berechnung vorbereiten", type="primary"):
    st.session_state.input_data = {
        "valuation_date": st.session_state.valuation_date_fx,
        "maturity_date": st.session_state.maturity_date_fx,
        "nominal": st.session_state.nominal_sold_fx,
        "contract_rate": st.session_state.contract_rate_fx,
        "spot_rate": st.session_state.spot_rate_fx,
        "dataframe_foreign_1": dataframe_foreign_1,
        "dataframe_foreign_2": dataframe_foreign_2,
        "foreign_country_name": st.session_state.foreign_country_name_fx,
        "trade_direction": "sell_foreign_buy_eur"
    }
    st.success("Daten gespeichert! Zu Result wechseln.")
