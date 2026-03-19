import streamlit as st
import numpy as np
from src.yield_curves import get_bundesbank_interest_rate, get_foreign_rate

st.title("Bewertung & Ergebnis")

st.write("""Bitte Geduld, die Berechnung kann je nach Datenmenge und Internetverbindung einige Sekunden dauern.""")
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
    dom_rate = get_bundesbank_interest_rate(valuation_date, maturity_date)

    foreign_country_name = data.get("foreign_country_name")
    if foreign_country_name is None:
        st.error("Partnerwährung fehlt in den Eingabedaten. Bitte Eingabeseite neu ausfüllen.")
        st.stop()

    foreign_rate = get_foreign_rate(
        foreign_country_name,
        data["dataframe_foreign_1"],
        data["dataframe_foreign_2"],
        valuation_date,
        maturity_date,
    )

    # Discount Factors
    df_dom = discount_factor(dom_rate, maturity_date, valuation_date)
    df_for = discount_factor(foreign_rate, maturity_date, valuation_date)

    st.metric("Inländischer Zinssatz (EUR)", f"{dom_rate:.4%}")
    st.metric(f"Fremdwährungszinssatz ({foreign_country_name})", f"{foreign_rate:.4%}")

    forward_rate = data["spot_rate"] * df_dom / df_for
    st.metric("Forward Rate", f"{forward_rate:.4f}")

    # Nominalbetrag in Fremdwährung
    bought_amount = data["nominal"] * data["contract_rate"]
    
    # Marktwert = (F_aktuell - F_Kontrakt) × Nominal_FW × DF_Fremdwährung
    # konvertiert in EUR-Basis
    market_value = (forward_rate - data["contract_rate"]) * bought_amount * df_for / forward_rate
    st.metric("Marktwert des Forwards (EUR)", f"{market_value:.2f}")
else:
    st.warning("Bitte zuerst Geschäftsdaten eingeben!")
