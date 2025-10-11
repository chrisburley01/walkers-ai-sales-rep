import os, re, sqlite3
from dotenv import load_dotenv
from imapclient import IMAPClient
from email import message_from_bytes

load_dotenv()
HOST=os.getenv('IMAP_HOST'); USER=os.getenv('IMAP_USERNAME'); PASS=os.getenv('IMAP_PASSWORD'); FOLDER=os.getenv('IMAP_FOLDER','INBOX')

con = sqlite3.connect('db/salesrep.sqlite')
cur = con.cursor()

with IMAPClient(HOST) as server:
    server.login(USER, PASS)
    server.select_folder(FOLDER)
    messages = server.search(['UNSEEN'])
    if not messages:
        print('No new messages.')
    fetched = server.fetch(messages, ['RFC822'])
    for uid, data in fetched.items():
        msg = message_from_bytes(data[b'RFC822'])
        sender = msg['From'] or ''
        subj = msg.get('Subject','')
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type()=='text/plain':
                    try: body += part.get_payload(decode=True).decode(errors='ignore')
                    except: pass
        else:
            try: body = msg.get_payload(decode=True).decode(errors='ignore')
            except: body = str(msg.get_payload())

        txt = (subj+'\n'+body).lower()
        intent = 'replied'
        if re.search(r'not\s+interested|no thanks|unsubscribe|stop', txt): intent = 'do_not_contact'
        if re.search(r'call|meeting|book|schedule|teams|zoom|next week|tomorrow', txt): intent = 'book_meeting'

        m = re.search(r'<([^>]+)>', sender) or re.search(r'([\w\.-]+@[\w\.-]+)', sender)
        lead_email = m.group(1) if m else None
        if lead_email:
            row = con.execute("SELECT lead_id FROM leads WHERE email=?", (lead_email,)).fetchone()
            if row:
                lead_id = row[0]
                cur.execute("UPDATE outreach SET status=? WHERE lead_id=? AND status='sent'", (intent, lead_id))
                con.commit()
print('Reply tracking pass complete ✅')
