import os, smtplib, sqlite3, time
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()
FROM_NAME=os.getenv('SMTP_FROM_NAME','Outreach')
FROM_EMAIL=os.getenv('SMTP_FROM_EMAIL')
HOST=os.getenv('SMTP_HOST'); PORT=int(os.getenv('SMTP_PORT','587'))
USER=os.getenv('SMTP_USERNAME'); PASS=os.getenv('SMTP_PASSWORD')
RATE_PER_MIN=int(os.getenv('RATE_PER_MIN','12'))

con = sqlite3.connect('db/salesrep.sqlite')
cur = con.cursor()
cur.execute("SELECT id, lead_id, subject, body FROM outreach WHERE status='queued' LIMIT 1000")
jobs = cur.fetchall()

if not FROM_EMAIL or not HOST:
    raise SystemExit("SMTP not configured. Check your .env.")

sent=0
with smtplib.SMTP(HOST, PORT) as s:
    s.starttls(); s.login(USER, PASS)
    for oid, lead_id, subject, body in jobs:
        email_row = con.execute("SELECT email, first_name, last_name FROM leads WHERE lead_id=?", (lead_id,)).fetchone()
        if not email_row or not email_row[0]:
            continue
        to = email_row[0]
        msg = EmailMessage()
        msg['From'] = formataddr((FROM_NAME, FROM_EMAIL))
        msg['To'] = to
        msg['Subject'] = subject
        msg.set_content(body + "\n\nIf this isn’t relevant, reply ‘stop’ and I’ll remove you immediately.")

        try:
            s.send_message(msg)
            cur.execute("UPDATE outreach SET status='sent', sent_at=datetime('now') WHERE id=?", (oid,))
            con.commit(); sent+=1
            if sent % RATE_PER_MIN == 0:
                time.sleep(60)
        except Exception:
            cur.execute("UPDATE outreach SET status='bounced' WHERE id=?", (oid,))
            con.commit()
print(f"Sent {sent} emails ✅")
