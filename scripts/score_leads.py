import pandas as pd
from pathlib import Path

leads = pd.read_csv('data/leads_enriched.csv')

def score(row):
    s=0
    if str(row.get('country','')).lower()=='united kingdom': s+=2
    if str(row.get('industry','')) in ['Retail','Ecommerce','FMCG','Manufacturing','Home & DIY','Building Materials','Automotive Aftermarket','Food & Drink (ambient)']: s+=2
    title = str(row.get('job_title','')).lower()
    if any(t in title for t in ['head of logistics','operations director','supply chain manager']): s+=3
    try:
        emp=int(row.get('company_size',0))
        if 50<=emp<=2000: s+=2
    except: pass
    return s

leads['score']=leads.apply(score, axis=1)
leads.sort_values('score', ascending=False).to_csv('data/leads_enriched.csv', index=False)
print('Scored and re‑saved leads ✅')
