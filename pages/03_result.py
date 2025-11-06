import streamlit as st
import requests
from datetime import datetime
import numpy as np

st.title("Bewertung & Ergebnis")

def get_bundesbank_zero_rate(valuation_date, maturity_date):
    # MVP: Dummy-API-Call – es wird erst einmal ein fixer Zinssatz eingesetzt
    # Später: API-Call zur echten Curve der Bundesbank
    # Return annual rate
    # Für Demo: 1% p.a.
    return 0.01

def get_foreign_rate():
    # MVP: Fester Zinssatz für Fremdwährung
    # Später: API-Call zu einem Zinsanbieter
    # Return annual rate
    # Für Demo: 2% p.a.
    return 0.02

def discount_factor(rate, maturity_date, valuation_date):
    """
    Berechnet den Discount Factor basierend auf dem Zinssatz und der Zeit bis zur Fälligkeit.
    """
    
    days = (maturity_date - valuation_date).days / 360
      #  use ACT/360 convention
    return np.exp(-rate * days)

if "input_data" in st.session_state:
    data = st.session_state.input_data
    valuation_date = data["valuation_date"]
    maturity_date = data["maturity_date"]
    dom_rate = get_bundesbank_zero_rate(valuation_date, maturity_date)
    foreign_rate = get_foreign_rate()

    # Discount Factors
    df_dom = discount_factor(dom_rate, valuation_date, maturity_date)
    df_for = discount_factor(foreign_rate, valuation_date, maturity_date)

    forward_rate = data["spot_rate"] * df_dom / df_for
    st.metric("Forward Rate", f"{forward_rate:.4f}")

    bought_amount = data["nominal"] * data["contract_rate"]
    
    market_value = (bought_amount/forward_rate - data["nominal"])/(1+df_for*(maturity_date - valuation_date).days/360)
    st.metric("Marktwert des Forwards (EUR)", f"{market_value:.2f}")
else:
    st.warning("Bitte zuerst Geschäftsdaten eingeben!")
