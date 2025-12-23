import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText

from automation_engine import decide_action

processed_emails = []

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"

EMAIL_ACCOUNT = "servsyncservicesynchronization@gmail.com"
EMAIL_PASSWORD = "kksuvjkgyikqznqc"

def fetch_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    
    print(f"Found {len(email_ids)} unread emails")  # Debug line

    emails = []

    for e_id in email_ids:
        _, msg_data = mail.fetch(e_id, "(BODY.PEEK[])")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject

        sender = msg.get("From")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        emails.append({
            "email_id": e_id.decode(),  # Store email ID
            "sender": sender,
            "subject": subject,
            "body": body.strip()
        })

    mail.logout()
    return emails

def fetch_all_emails(limit=50):
    """Fetch all emails (read and unread) from inbox"""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    
    # Get the most recent emails (limit)
    email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
    email_ids.reverse()  # Most recent first

    emails = []

    for e_id in email_ids:
        try:
            _, msg_data = mail.fetch(e_id, "(BODY.PEEK[])")
            msg = email.message_from_bytes(msg_data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject

            sender = msg.get("From")
            date = msg.get("Date")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            emails.append({
                "sender": sender,
                "subject": subject,
                "body": body.strip(),
                "date": date
            })
        except Exception as e:
            print(f"Error fetching email {e_id}: {e}")
            continue

    mail.logout()
    return emails

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to_email
    msg["Subject"] = subject

    server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
    server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

def process_emails():
    emails = fetch_unread_emails()
    print(f"Processing {len(emails)} emails")  # Debug line
    
    # Get list of already processed email IDs
    already_processed = {email["email_id"] for email in processed_emails}

    for mail in emails:
        # Skip if already processed
        if mail["email_id"] in already_processed:
            continue
            
        decision = decide_action(mail["body"])

        record = {
            "id": len(processed_emails),
            "email_id": mail["email_id"],  # Track email ID
            "sender": mail["sender"],
            "subject": mail["subject"],
            "body": mail["body"],
            "category": decision["category"],
            "priority": decision["priority"],
            "status": "Auto-replied" if decision["auto_reply"] else "Manual action required",
            "marked_done": False  # Track if user marked as done
        }

        if decision["auto_reply"]:
            sender_email = mail["sender"].split("<")[-1].replace(">", "")
            send_email(
                sender_email,
                "Re: " + mail["subject"],
                decision["reply_text"]
            )
            record["status"] = "Auto-replied"
        else:
            record["status"] = "Manual action required"

        processed_emails.insert(0, record)  # Insert at the beginning for newest first
        
        # Re-index all emails
        for idx, email in enumerate(processed_emails):
            email["id"] = idx


if __name__ == "__main__":
    process_emails()
