import pandas as pd
import yaml, uuid
from pathlib import Path

raw = pd.read_csv('data/leads_raw.csv')
map_cfg = yaml.safe_load(Path('config/fields_map.yaml').read_text())

colmap = map_cfg['incoming_to_canonical']
df = raw.rename(columns=colmap)

for col in ['company','website','domain','first_name','last_name','job_title','email','linkedin_url','company_size','country','industry']:
    if col not in df.columns: df[col] = None

if 'full_name' not in df.columns:
    df['full_name'] = (df['first_name'].fillna('') + ' ' + df['last_name'].fillna('')).str.strip()

def mkid(row):
    key = (str(row.get('email')) or (str(row.get('company'))+str(row.get('full_name')))).lower()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

df['lead_id'] = df.apply(mkid, axis=1)

if 'email' in df:
    df = df.sort_values('email').drop_duplicates('email', keep='first')

df.to_csv('data/leads_enriched.csv', index=False)
print(f"Ingested {len(df)} leads → data/leads_enriched.csv ✅")
