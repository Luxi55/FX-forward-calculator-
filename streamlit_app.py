import streamlit as st

st.set_page_config(page_title="FX-Forward Calculator", layout="centered")

st.title("FX-Forward Calculator")
st.write("""Bewerte Devisentermingeschäfte zum Stichtag mit aktuellen Zinsstrukturkurven.
- EUR-Kurve via Bundesbank-API

Fremdwährungszinsstrukturkuve wird mithilfe von CSV ermittelt.
- Für USA https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2025

- Schweiz und UK noch nicht implementiert
""")
