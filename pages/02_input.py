import streamlit as st
import datetime

st.title("Geschäftsdaten eingeben")

valuation_date = st.date_input("Bewertungsstichtag", value=datetime.date.today())
maturity_date = st.date_input("Fälligkeitstermin")
nominal_sold = st.number_input("Verkaufte Summe (EUR)", min_value=0.0)
contract_rate = st.number_input("Contract Rate (fixiert)", min_value=0.0)
spot_rate = st.number_input("Aktueller Spot Rate", min_value=0.0)
contract_rate = st.number_input("Contract Rate aus Vertrag", min_value=0.0) # Flat-Rate

if st.button("Berechnung vorbereiten"):
    st.session_state.input_data = {
        "valuation_date": valuation_date,
        "maturity_date": maturity_date,
        "nominal": nominal_sold,
        "contract_rate": contract_rate,
        "spot_rate": spot_rate
    }
    st.success("Daten gespeichert! Zur Berechnung wechseln.")
