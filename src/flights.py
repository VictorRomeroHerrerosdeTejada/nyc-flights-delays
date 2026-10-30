"""Data loading, feature engineering and plotting helpers for the NYC flights analysis."""
import urllib.request
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

BASE = "https://raw.githubusercontent.com/machow/nycflights13-py/master/nycflights13/data/"
DATA = Path(__file__).resolve().parent.parent / "data"   # carpeta data/ en la raíz del repo
C1, C2, GRAY = "#2a78d6", "#eb6834", "#9a9893"


def load(name):
    """Download (first time only) and read one nycflights13 table as a DataFrame."""
    DATA.mkdir(exist_ok=True)
    path = DATA / name
    if not path.exists():
        urllib.request.urlretrieve(BASE + name, path)
    return pd.read_csv(path)

def add_features(df):
    """
    Returns a copy of the dataframe df with new columns: date, weekday, cancelled & gain. 
    #   date       -> date from columns "year", "month" and "day"
    #   weekday    -> nameod the day of the week
    #   cancelled  -> True if dep_time is NaN
    #   gain       -> dep_delay - arr_delay
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    df["weekday"] = df["date"].dt.day_name()
    df["cancelled"] = df["dep_time"].isna()
    df["gain"] = df["dep_delay"] - df["arr_delay"]
    return df

def mean_by(df, by, col, min_n=1):
    """
    Number of rows (n) y mean value of `col` by groups of `by`, only with groups with n >= min_n,
    sorted in descending order.
    """
    n = len(df[col])
    groups = df.groupby(by).agg(n=(col, "size"), media=(col, "mean"))
    return (groups[groups["n"] >= min_n]).sort_values(by="media", ascending=False)

def plot_ranking(series, title, xlabel, highlight=3, ax=None):
    """
    Sorted horizontal bars from a Series (index = labels), highlighting the 
    first `highlight` entries in C2 y and the rest in GRAY. Returns ax.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 0.35 * len(series) + 1))
        colors = [C2 if i < 3 else GRAY for i in range(len(series))]
        bars = ax.barh(series.index, series.values, color=colors)
        ax.bar_label(bars, fmt="%.1f", padding=3)                 
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(False)
        ax.invert_yaxis()
        ax.set(title=title, xlabel=xlabel)
        plt.tight_layout()
    return ax