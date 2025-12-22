from automation_engine import decide_action

emails = [
    "I want to book a family tour in Sri Lanka",
    "Your service was very bad and I want a refund",
    "What documents are required for visa",
    "Can you tell me your office hours",
    "Congratulations you have won free tickets"
]

for email in emails:
    result = decide_action(email)
    print("\nEmail:", email)
    print("Category:", result["category"])
    print("Priority:", result["priority"])
    print("Auto Reply:", result["auto_reply"])
    print("Reply Text:\n", result["reply_text"])
