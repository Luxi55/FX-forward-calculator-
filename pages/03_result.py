import streamlit as st
import requests
from datetime import datetime

st.title("Bewertung & Ergebnis")

def get_bundesbank_zero_rate(valuation_date, maturity_date):
    # MVP: Dummy-API-Call – es wird erst einmal ein fixer Zinssatz eingesetzt
    # Später: API-Call zur echten Curve der Bundesbank
    # Return annual rate
    # Für Demo: 1% p.a.
    return 0.01

def discount_factor(rate, start_date, end_date):
    days = (end_date - start_date).days / 365
    return 1 / (1 + rate * days)

if "input_data" in st.session_state:
    data = st.session_state.input_data
    start = data["valuation_date"]
    end = data["maturity_date"]
    dom_rate = get_bundesbank_zero_rate(start, end)
    foreign_rate = data["foreign_rate"]

    # Discount Factors
    df_dom = discount_factor(dom_rate, start, end)
    df_for = discount_factor(foreign_rate, start, end)

    forward_rate = data["spot_rate"] * df_for / df_dom
    st.metric("Forward Rate", f"{forward_rate:.4f}")

    market_value = (forward_rate - data["contract_rate"]) * data["nominal"] * df_dom
    st.metric("Marktwert des Forwards (EUR)", f"{market_value:.2f}")
else:
    st.warning("Bitte zuerst Geschäftsdaten eingeben!")
