import pandas as pd

def load_events():
    return pd.read_csv("data/events.csv")

def load_expenses():
    return pd.read_csv("data/expenses.csv")

def load_sponsors():
    return pd.read_csv("data/sponsors.csv")