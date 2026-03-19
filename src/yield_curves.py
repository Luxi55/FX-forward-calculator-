import requests
import gzip
import pandas as pd
from io import BytesIO, StringIO
import re
import numpy as np

def maturity_to_days_EUR(s):
    if pd.isna(s):
        return None
    s = str(s).lower()
    years = 0
    months = 0
    y = re.search(r'(\d+)\s*year', s)
    m = re.search(r'(\d+)\s*month', s)
    if y:
        years = int(y.group(1))
    if m:
        months = int(m.group(1))
    return years * 365 + months * 30

def maturity_to_days_USD(s):
    if pd.isna(s):
        return None
    s = str(s).strip().lower()
    years = 0.0
    months = 0.0
    y = re.search(r'(\d+(?:\.\d+)?)\s*(yr|year)s?\b', s)
    m = re.search(r'(\d+(?:\.\d+)?)\s*(mo|month)s?\b', s)
    if y:
        years = float(y.group(1))
    if m:
        months = float(m.group(1))
    if years == 0 and months == 0:
        return None
    return int(round(years * 365 + months * 30))

def fetch_eurostat_curve() -> pd.DataFrame:
    """
    Lädt die Eurostat-Zinskurve (CSV, gzip) und gibt ein DataFrame zurück.
    """

    url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/irt_euryld_d/1.0/*.*.*.*.*?c[freq]=D&c[yld_curv]=SPOT_RT&c[maturity]=M3,M4,M5,M6,M7,M8,M9,Y1,Y1_M1,Y1_M2,Y1_M3,Y1_M4,Y1_M5,Y1_M6,Y1_M7,Y1_M8,Y1_M9,Y1_M10,Y1_M11,Y2,Y2_M1,Y2_M2,Y2_M3,Y2_M4,Y2_M5,Y2_M6,Y2_M7,Y2_M8,Y2_M9,Y2_M10,Y2_M11,Y3,Y3_M1,Y3_M2,Y3_M3,Y3_M4,Y3_M5,Y3_M6,Y3_M7,Y3_M8,Y3_M9,Y3_M10,Y3_M11,Y4,Y4_M1,Y4_M2,Y4_M3,Y4_M4,Y4_M5,Y4_M6,Y4_M7,Y4_M8,Y4_M9,Y4_M10,Y4_M11,Y5,Y5_M1,Y5_M2,Y5_M3,Y5_M4,Y5_M5,Y5_M6,Y5_M7,Y5_M8,Y5_M9,Y5_M10,Y5_M11,Y6,Y6_M1,Y6_M2,Y6_M3,Y6_M4,Y6_M5,Y6_M6,Y6_M7,Y6_M8,Y6_M9,Y6_M10,Y6_M11,Y7,Y7_M1,Y7_M2,Y7_M3,Y7_M4,Y7_M5,Y7_M6,Y7_M7,Y7_M8,Y7_M9,Y7_M10,Y7_M11,Y8,Y8_M1,Y8_M2,Y8_M3,Y8_M4,Y8_M5,Y8_M6,Y8_M7,Y8_M8,Y8_M9,Y8_M10,Y8_M11,Y9,Y9_M1,Y9_M2,Y9_M3,Y9_M4,Y9_M5,Y9_M6,Y9_M7,Y9_M8,Y9_M9,Y9_M10,Y9_M11&c[bonds]=CGB_EA_AAA&c[geo]=EA&c[TIME_PERIOD]=ge:2020-01-02&compress=true&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"
    resp = requests.get(url)
    resp.raise_for_status()

    compressed = BytesIO(resp.content)
    with gzip.GzipFile(fileobj=compressed) as f:
        csv_bytes = f.read()

    csv_text = csv_bytes.decode("utf-8")
    df = pd.read_csv(StringIO(csv_text))

    # Drop unneeded cols (wie in test.py)
    df = df.drop(columns=["DATAFLOW", "LAST UPDATE", "freq", "yld_curv",
                          "bonds", "geo", "OBS_FLAG", "CONF_STATUS"], errors="ignore")

    df["TIME_PERIOD"] = pd.to_datetime(df["TIME_PERIOD"])

    return df

def get_bundesbank_interest_rate(valuation_date, maturity_date):
    """
    Linear interpolation:
    X = maturity_days (aus maturity_to_days)
    Y = OBS_VALUE (in Dezimal, d.h. 2.5% -> 0.025)
    Returns interpolated rate (float) or None wenn keine Daten.
    """
    df = fetch_eurostat_curve()
    # print(df.tail())  # Debug-Ausgabe, um Struktur zu prüfen

    # ensure valuation_date is a Timestamp
    vdate = pd.to_datetime(valuation_date)
    mdate = pd.to_datetime(maturity_date)

    # Filtere die Daten für den Bewertungsstichtag
    df_date = df[df['TIME_PERIOD'] == vdate].copy()
    if df_date.empty:
        raise ValueError(f"No yield curve data for valuation date {valuation_date}")

    df_date['maturity_days'] = df_date['maturity'].apply(maturity_to_days_EUR)
      #  convert maturity from x years and y months to days
    df_date['obs'] = pd.to_numeric(df_date['OBS_VALUE'], errors='coerce') / 100.0
      #  convert percentage to decimal
    df_date = df_date.dropna(subset=['maturity_days', 'obs'])

    # calculate target maturity in days
    target_days = int((mdate - vdate).days)

    # use only the two neighbouring maturities (no duplicates guaranteed)
    df_date = df_date.sort_values('maturity_days')
    x = df_date['maturity_days'].to_numpy(dtype=float)
    y = df_date['obs'].to_numpy(dtype=float)

    # find neighbours and interpolate linearly
    idx = np.searchsorted(x, target_days, side='left')
    left, right = idx - 1, idx
    x0, x1 = x[left], x[right]
    y0, y1 = y[left], y[right]
    if x1 == x0:
        return float(y0)
    t = (target_days - x0) / (x1 - x0)
    return float(y0 + t * (y1 - y0))

def get_foreign_rate(foreign_country_name, dataframe_foreign_1, dataframe_foreign_2, valuation_date, maturity_date):
    """
    """
    if foreign_country_name == "US Dollar":
        df_1 = pd.read_csv(dataframe_foreign_1)
        df_2 = pd.read_csv(dataframe_foreign_2)
        df = pd.concat([df_1, df_2], ignore_index=True)
        df['Date'] = pd.to_datetime(df['Date'])

        vdate = pd.to_datetime(valuation_date)
        mdate = pd.to_datetime(maturity_date)

        # Use the selected valuation date row from the Treasury curve table.
        df_date = df[df['Date'] == vdate]
        if df_date.empty:
            raise ValueError(f"No USD yield curve data for valuation date {valuation_date}")

        row = df_date.iloc[0]
        points = []
        for col in df.columns:
            if col == 'Date':
                continue
            days = maturity_to_days_USD(col)
            obs = pd.to_numeric(row[col], errors='coerce')
            if days is not None and pd.notna(obs):
                points.append((days, obs / 100.0))

        if not points:
            raise ValueError("No valid USD maturity points found in input CSV")

        points.sort(key=lambda p: p[0])
        x = np.array([p[0] for p in points], dtype=float)
        y = np.array([p[1] for p in points], dtype=float)

        # Interpolate to the required tenor (days between valuation and maturity).
        target_days = int((mdate - vdate).days)
        return float(np.interp(target_days, x, y))

    elif foreign_country_name == "Schweizer Franken":
        raise NotImplementedError("Die Zinsstrukturkurve für CHF ist noch nicht implementiert.")
    elif foreign_country_name == "Britisches Pfund":
        raise NotImplementedError("Die Zinsstrukturkurve für GBP ist noch nicht implementiert.")
    else:
        raise ValueError(f"Unbekannte Partnerwährung: {foreign_country_name}")

if __name__ == "__main__":
    # Testaufruf
    val_date = "2025-12-31"
    mat_date = "2026-11-10"
    rate = get_bundesbank_interest_rate(val_date, mat_date)
    print(f"Interpolierter Zinssatz für {val_date} bis {mat_date}: {rate:.4%}")