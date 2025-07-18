from flask import Blueprint, request, jsonify
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime

api = Blueprint('api', __name__)  # ✅ Blueprint instance

@api.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "🧠 Flask API is working and responding!"})

@api.route('/api/fetch-emails', methods=['POST'])
def fetch_emails():
    try:
        data = request.get_json()
        email_user = data.get('email')
        app_password = data.get('password')
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, app_password)
        mail.select("inbox")

        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        fetched = []

        for eid in reversed(email_ids[-50:]):  # Fetch last 50
            status, msg_data = mail.fetch(eid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    subject = subject.strip() or "No_Subject"

                    date_obj = parsedate_to_datetime(msg["Date"]).replace(tzinfo=None)
                    date_str = date_obj.strftime("%Y-%m-%d")

                    # Filter by date
                    if date_from and date_to:
                        from_dt = datetime.strptime(date_from, "%Y-%m-%d")
                        to_dt = datetime.strptime(date_to, "%Y-%m-%d")
                        if not (from_dt <= date_obj <= to_dt):
                            continue

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    fetched.append({
                        "subject": subject,
                        "date": date_str,
                        "body": body[:200]  # Only a preview
                    })

        mail.logout()
        return jsonify({"success": True, "emails": fetched})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
