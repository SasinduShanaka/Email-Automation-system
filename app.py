from flask import Flask, render_template, request, redirect, url_for
from email_handler import process_emails, processed_emails, send_email, fetch_all_emails

app = Flask(__name__)

@app.route("/")
def dashboard():
    process_emails()
    # Filter out emails that are marked as done
    active_emails = [email for email in processed_emails if not email.get("marked_done", False)]
    return render_template("dashboard.html", emails=active_emails)

@app.route("/mark-done/<int:email_id>", methods=["POST"])
def mark_done(email_id):
    # Find and mark the email as done
    for email in processed_emails:
        if email["id"] == email_id:
            email["marked_done"] = True
            break
    return redirect(url_for("dashboard"))

@app.route("/analytics")
def analytics():
    return render_template("analytics.html", emails=processed_emails)

@app.route("/past-emails")
def past_emails():
    all_emails = fetch_all_emails(limit=100)
    return render_template("past_emails.html", emails=all_emails)

@app.route("/reply/<int:email_id>", methods=["GET", "POST"])
def manual_reply(email_id):
    email_data = processed_emails[email_id]

    if request.method == "POST":
        reply_text = request.form["reply"]

        sender_email = email_data["sender"].split("<")[-1].replace(">", "")
        send_email(
            sender_email,
            "Re: " + email_data["subject"],
            reply_text
        )

        email_data["status"] = "Replied manually"
        return redirect(url_for("dashboard"))

    return render_template("reply.html", email=email_data)

if __name__ == "__main__":
    app.run(debug=True)
