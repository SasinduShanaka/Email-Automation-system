from flask import Flask, render_template
from email_handler import process_emails, processed_emails

app = Flask(__name__)

@app.route("/")
def dashboard():
    # fetch & process emails
    process_emails()
    return render_template(
        "dashboard.html",
        emails=processed_emails
    )

if __name__ == "__main__":
    app.run(debug=True)
