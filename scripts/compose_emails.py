import os, yaml, pandas as pd
from pathlib import Path
from openai import OpenAI
from jinja2 import Template
from tqdm import tqdm

# Load OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
OPENAI_MODEL = os.getenv('OPENAI_MODEL','gpt-4o-mini')

style = yaml.safe_load(Path('config/style.yaml').read_text())
seq_cfg = yaml.safe_load(Path('config/sequence.yaml').read_text())
sequence = seq_cfg['sequence']
templates_raw = seq_cfg.get('templates', {})
T = {k: Template(v) for k,v in templates_raw.items()}

leads = pd.read_csv('data/leads_enriched.csv')
Path('data/outbox').mkdir(parents=True, exist_ok=True)

def make_hook(row):
    if isinstance(row.get('industry'), str) and 'Retail' in row['industry']:
        return "Noticed retail peaks; late cut‑off and x‑dock help reduce splits."
    cs = str(row.get('company_size',''))
    if cs.isdigit() and int(cs)>500:
        return "Larger ops often gain from direct trunks on top lanes."
    return style['personalisation']['fallback'].replace('{{company}}', str(row.get('company',''))).replace('{{industry}}', str(row.get('industry','')))

records = []
for _, r in tqdm(leads.iterrows(), total=len(leads)):
    ctx = {**r.to_dict()}
    ctx['hook'] = make_hook(r)
    # First step only for MVP
    body = T['walkers_intro'].render(**ctx)
    subject = [s for s in sequence['steps'] if s['id']=='s1'][0]['subject']
    outpath = Path('data/outbox')/f"{r['lead_id']}_s1.txt"
    outpath.write_text(body)
    records.append({'lead_id': r['lead_id'], 'step_id':'s1', 'subject':subject, 'body':body})

import sqlite3
con = sqlite3.connect('db/salesrep.sqlite')
con.executemany('INSERT INTO outreach(lead_id, step_id, subject, body, status) VALUES (?,?,?,?,?)',
                [(x['lead_id'], x['step_id'], x['subject'], x['body'], 'queued') for x in records])
con.commit(); con.close()
print(f"Queued {len(records)} emails in DB and wrote drafts to data/outbox ✅")
