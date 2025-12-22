def get_auto_reply(category):
    templates = {
        "booking": (
            "Thank you for contacting us regarding your tour booking.\n\n"
            "We are pleased to offer customized travel packages across Sri Lanka. "
            "Our team will review your request and share package details, pricing, "
            "and availability shortly.\n\n"
            "Best regards,\n"
            "Travel Support Team"
        ),

        "visa": (
            "Thank you for your inquiry regarding visa requirements.\n\n"
            "Please let us know your nationality and travel dates so we can "
            "provide accurate visa guidance and required documentation.\n\n"
            "Best regards,\n"
            "Visa Assistance Team"
        ),

        "general": (
            "Thank you for reaching out to us.\n\n"
            "We have received your inquiry and our support team will get back "
            "to you with the requested information as soon as possible.\n\n"
            "Best regards,\n"
            "Customer Support Team"
        ),

        "complaint": (
            "Thank you for bringing this matter to our attention.\n\n"
            "We sincerely apologize for the inconvenience caused. "
            "Your concern has been escalated to our support manager, "
            "and we will get back to you with a resolution shortly.\n\n"
            "Kind regards,\n"
            "Customer Care Team"
        ),

        "spam": None
    }

    return templates.get(category)
