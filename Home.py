import streamlit as st

st.set_page_config(page_title="FX-Forward Calculator", layout="centered")

st.title("FX-Forward Calculator")
st.write("""Bewerte Devisentermingeschäfte zum Stichtag mit aktuellen Zinsstrukturkurven.

- EUR-Kurve via Bundesbank-API


- Für USA Fremdwährungszinsstrukturkuve wird mithilfe von CSV ermittelt. Abrufbar unter: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2025

- Schweiz vie API
         
- UK Datenquelle der Excel nicht mehr aufrufbar. Ich habe leider keine Alternative gefunden. Daher ist die Zinsstrukturkurve für GBP aktuell nicht implementiert.
""")

st.warning("Beim CSV Upload bitte darauf achten, dass die Daten auch den gewünschten Zeitraum abdecken.")