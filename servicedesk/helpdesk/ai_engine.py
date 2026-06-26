import ollama


def get_ai_response(issue):

    prompt = f"""
You are an IT Service Desk Assistant.

User Issue:
{issue}

Give response in this format:

Issue Summary:
Possible Causes:
1.
2.
3.

Troubleshooting Steps:
1.
2.
3.

When To Escalate:
1.
2.

Be concise and practical.
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]



def analyze_issue(issue):
    return get_ai_response(issue)



def categorize_incident(issue):

    text = issue.lower()

    if any(word in text for word in [
        "screen",
        "display",
        "phone",
        "laptop",
        "battery",
        "charger",
        "keyboard",
        "mouse",
        "hardware",
        "broken",
        "damaged"
    ]):
        return "Hardware"


    if any(word in text for word in [
        "wifi",
        "internet",
        "network",
        "connection",
        "router"
    ]):
        return "Network"


    if any(word in text for word in [
        "app",
        "software",
        "error",
        "crash",
        "install"
    ]):
        return "Software"


    if any(word in text for word in [
        "password",
        "login",
        "account",
        "username"
    ]):
        return "Account"


    if any(word in text for word in [
        "virus",
        "malware",
        "hack",
        "security"
    ]):
        return "Security"


    return "Other"