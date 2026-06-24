def get_recommendation(goal, budget):

    if goal == "Max Participation":

        return {
            "Technical": int(budget * 0.25),
            "Publicity": int(budget * 0.30),
            "Logistics": int(budget * 0.20),
            "Hospitality": int(budget * 0.15),
            "Reserve": int(budget * 0.10),
            "Reason": "Higher publicity improves reach and registrations."
        }

    elif goal == "Max Feedback":

        return {
            "Technical": int(budget * 0.35),
            "Publicity": int(budget * 0.15),
            "Logistics": int(budget * 0.25),
            "Hospitality": int(budget * 0.15),
            "Reserve": int(budget * 0.10),
            "Reason": "Technical quality and logistics strongly influence feedback."
        }

    else:

        return {
            "Technical": int(budget * 0.20),
            "Publicity": int(budget * 0.20),
            "Logistics": int(budget * 0.15),
            "Hospitality": int(budget * 0.10),
            "Reserve": int(budget * 0.05),
            "Sponsorship Outreach": int(budget * 0.30),
            "Reason": "More effort allocated to sponsor acquisition."
        }