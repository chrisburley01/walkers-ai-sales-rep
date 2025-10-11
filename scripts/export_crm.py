import pandas as pd
cols = ['company','first_name','last_name','email','job_title','linkedin_url','industry','company_size','country']

(pd.read_csv('data/leads_enriched.csv')[cols]
  .to_csv('data/hubspot_import.csv', index=False))

print('Exported → data/hubspot_import.csv ✅')
