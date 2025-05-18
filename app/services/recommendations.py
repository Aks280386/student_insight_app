def recommend_actions(causes):
    actions = []
    if "Low Attendance" in causes:
        actions.append("Schedule a meeting with parents")
    if "Weak in Math" in causes:
        actions.append("Assign student to math remedial sessions")
    if "Weak in Science" in causes:
        actions.append("Offer extra science classes")
    if "Needs Behavioral Support" in causes:
        actions.append("Refer to school counselor")
    return actions