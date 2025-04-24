from threading import Lock

lock = Lock()

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    with lock:
        # Normalize email to avoid duplicates due to case sensitivity or extra spaces
        normalized_email = email.strip().lower()

        # Check if the student is already registered
        if normalized_email in map(str.lower, map(str.strip, activity["participants"])):
            raise HTTPException(status_code=400, detail="Student already registered for this activity")

        # Add student
        activity["participants"].append(normalized_email)

    return {"message": f"Signed up {email} for {activity_name}"}