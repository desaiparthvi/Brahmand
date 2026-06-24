def health_score(event):

    # =========================
    # Feedback Score (30)
    # =========================
    feedback_score = (
        event["Feedback"] / 5
    ) * 30

    # =========================
    # Sponsorship Score (20)
    # 40% sponsorship coverage = full marks
    # =========================
    sponsor_score = min(
        (event["SponsorRatio"] / 0.40) * 20,
        20
    )

    # =========================
    # Budget Utilization Score (20)
    # Ideal = 90% to 100%
    # =========================
    utilization = event["BudgetUtilization"]

    if 0.90 <= utilization <= 1.00:
        budget_score = 20

    elif 0.75 <= utilization < 0.90:
        budget_score = 15

    elif 0.60 <= utilization < 0.75:
        budget_score = 10

    else:
        budget_score = 5

    # =========================
    # Participation Score (15)
    # 600 participants = full marks
    # =========================
    participant_score = min(
        (event["Participants"] / 600) * 15,
        15
    )

    # =========================
    # Participant Efficiency (15)
    # Measures participants per ₹ budget
    # =========================
    efficiency_score = min(
        (event["ParticipantEfficiency"] / 0.01) * 15,
        15
    )

    # =========================
    # Final Score
    # =========================
    score = (
        feedback_score
        + sponsor_score
        + budget_score
        + participant_score
        + efficiency_score
    )

    return round(score, 1)