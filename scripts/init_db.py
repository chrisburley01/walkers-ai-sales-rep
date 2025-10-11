    import sqlite3
    from pathlib import Path

    schema = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS leads (
  lead_id TEXT PRIMARY KEY,
  company TEXT, website TEXT, domain TEXT,
  first_name TEXT, last_name TEXT, full_name TEXT,
  job_title TEXT, seniority TEXT, department TEXT,
  email TEXT, email_status TEXT,
  linkedin_url TEXT, company_size TEXT, industry TEXT,
  location TEXT, country TEXT,
  tech_stack TEXT, notes TEXT, source TEXT, list_name TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS outreach (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id TEXT,
  step_id TEXT,
  subject TEXT,
  body TEXT,
  sent_at TEXT,
  sender_email TEXT,
  status TEXT,
  thread_id TEXT,
  FOREIGN KEY(lead_id) REFERENCES leads(lead_id)
);
CREATE INDEX IF NOT EXISTS idx_outreach_lead ON outreach(lead_id);
"""

    Path('db').mkdir(exist_ok=True)
    con = sqlite3.connect('db/salesrep.sqlite')
    con.executescript(schema)
    con.close()
    print("DB ready ✅")
