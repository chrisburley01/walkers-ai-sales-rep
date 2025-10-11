# Walkers AI Sales Rep Pro

An AI-powered **sales outreach assistant** designed for **Walkers Transport** to automate lead research, cold emails, and follow-ups across pallet distribution and storage services.

---

## 🚀 Features
- **Lead ingestion** (CSV → normalised schema)
- **AI personalisation** (OpenAI-powered cold email drafts)
- **Multi-inbox rotation** (daily caps, time windows, random jitter)
- **Sequence management** (5-touch Walkers-specific cadence)
- **Reply tracking** (IMAP, detects interest / meeting requests / unsubscribes)
- **Web UI** (FastAPI + simple HTML dashboard for draft approval & batch sends)
- **CRM export** (HubSpot-compatible CSV)

---

## 📦 Getting Started
```bash
git clone https://github.com/chrisburley01/walkers-ai-sales-rep.git
cd walkers-ai-sales-rep
pip install -r requirements.txt
cp .env.example .env