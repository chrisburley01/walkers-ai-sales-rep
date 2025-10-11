# AI Sales Rep – Walkers Transport (Pallet Distribution & Storage)

A practical, modular AI assistant for outbound sales: ingest leads → personalise → send → track → export.

## Quick start
```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env with SMTP/IMAP + OPENAI_API_KEY
python scripts/init_db.py
python scripts/ingest_csv.py
python scripts/score_leads.py
python scripts/compose_emails.py
python scripts/send_sequence.py
# later / periodically
python scripts/track_replies.py
python scripts/export_crm.py
```

## Folders
- `config/` – ICP, tone/style, sequence & templates
- `data/` – input/output CSVs and drafts
- `db/` – SQLite state
- `scripts/` – operations
