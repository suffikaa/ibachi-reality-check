# Hibachi Reality Check

Anti-rekt calculator for Hibachi airdrop: real FDV math, share card, compare with other drops.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

## Deploy to Streamlit Community Cloud (free)

1. **Create a GitHub repo** and push this folder:
   - `app.py`
   - `hibachi.png`
   - `requirements.txt`
   - `.streamlit/config.toml` (optional)

2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.

3. **New app** → choose your repo, branch `main`, main file path: `app.py`.

4. Click **Deploy**. In a couple of minutes you get a public URL like `https://your-app-name.streamlit.app`.

5. Share the link (e.g. use `hibachi.xyz` or a short link that redirects to it).

No server to maintain, no credit card. Streamlit Cloud runs the app for free (with their limits).
