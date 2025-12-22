import pickle
from reply_templates import get_auto_reply

# Load trained model
with open("models/email_classifier.pkl", "rb") as f:
    model = pickle.load(f)

def decide_action(email_text):
    prediction = model.predict([email_text])[0]

    if prediction == "booking":
        return {
            "category": prediction,
            "priority": "medium",
            "auto_reply": True,
            "reply_text": get_auto_reply("booking"),
            "route_to": "sales_team"
        }

    elif prediction == "complaint":
        return {
            "category": prediction,
            "priority": "high",
            "auto_reply": False,
            "reply_text": get_auto_reply("complaint"),
            "route_to": "support_manager"
        }

    elif prediction == "visa":
        return {
            "category": prediction,
            "priority": "medium",
            "auto_reply": True,
            "reply_text": get_auto_reply("visa"),
            "route_to": "visa_department"
        }

    elif prediction == "general":
        return {
            "category": prediction,
            "priority": "low",
            "auto_reply": True,
            "reply_text": get_auto_reply("general"),
            "route_to": "support_team"
        }

    else:  # spam
        return {
            "category": prediction,
            "priority": "low",
            "auto_reply": False,
            "reply_text": None,
            "route_to": "ignore"
        }
