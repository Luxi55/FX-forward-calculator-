import requests
import gzip
import pandas as pd
from io import BytesIO, StringIO

def fetch_eurostat_curve(url: str = None) -> pd.DataFrame:
    """
    Lädt die Eurostat-Zinskurve (CSV, gzip) und gibt ein DataFrame zurück.
    Default-URL entspricht der Abfrage in test.py.
    """
    if url is None:
        url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/irt_euryld_d/1.0/*.*.*.*.*?c[freq]=D&c[yld_curv]=SPOT_RT&c[maturity]=M3,M4,M5,M6,M7,M8,M9,Y1,Y1_M1,Y1_M2,Y1_M3,Y1_M4,Y1_M5,Y1_M6,Y1_M7,Y1_M8,Y1_M9,Y1_M10,Y1_M11,Y2,Y2_M1,Y2_M2,Y2_M3,Y2_M4,Y2_M5,Y2_M6,Y2_M7,Y2_M8,Y2_M9,Y2_M10,Y2_M11,Y3,Y3_M1,Y3_M2,Y3_M3,Y3_M4,Y3_M5,Y3_M6,Y3_M7,Y3_M8,Y3_M9,Y3_M10,Y3_M11,Y4,Y4_M1,Y4_M2,Y4_M3,Y4_M4,Y4_M5,Y4_M6,Y4_M7,Y4_M8,Y4_M9,Y4_M10,Y4_M11,Y5,Y5_M1,Y5_M2,Y5_M3,Y5_M4,Y5_M5,Y5_M6,Y5_M7,Y5_M8,Y5_M9,Y5_M10,Y5_M11,Y6,Y6_M1,Y6_M2,Y6_M3,Y6_M4,Y6_M5,Y6_M6,Y6_M7,Y6_M8,Y6_M9,Y6_M10,Y6_M11,Y7,Y7_M1,Y7_M2,Y7_M3,Y7_M4,Y7_M5,Y7_M6,Y7_M7,Y7_M8,Y7_M9,Y7_M10,Y7_M11,Y8,Y8_M1,Y8_M2,Y8_M3,Y8_M4,Y8_M5,Y8_M6,Y8_M7,Y8_M8,Y8_M9,Y8_M10,Y8_M11,Y9,Y9_M1,Y9_M2,Y9_M3,Y9_M4,Y9_M5,Y9_M6,Y9_M7,Y9_M8,Y9_M9,Y9_M10,Y9_M11&c[bonds]=CGB_EA_AAA&c[geo]=EA&compress=true&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"

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