import pandas as pd

def add_features(df):

    df = df.copy()

    # How much of allocated budget was actually used
    df["BudgetUtilization"] = (
        df["ActualExpense"] / df["Budget"]
    )

    # Percentage of budget covered by sponsors
    df["SponsorRatio"] = (
        df["Sponsorship"] / df["Budget"]
    )

    # Actual spending per participant
    df["CostPerParticipant"] = (
        df["ActualExpense"] / df["Participants"]
    )

    # Surplus / deficit
    df["ProfitLoss"] = (
        df["Sponsorship"] - df["ActualExpense"]
    )

    # Participants generated per rupee budgeted
    df["ParticipantEfficiency"] = (
        df["Participants"] / df["Budget"]
    )

    return df