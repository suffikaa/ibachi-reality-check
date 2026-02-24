import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import urllib.parse

BASELINE_FDV = 80000000

FDV_PRESETS = {
    "$50M — Dead on Arrival": 50000000,
    "$100M — Bearish": 100000000,
    "$200M — Conservative": 200000000,
    "$300M — Moderate": 300000000,
    "$500M — Optimistic": 500000000,
    "$750M — Strong Launch": 750000000,
    "$1B — Bullish": 1000000000,
    "$1.5B — Very Bullish": 1500000000,
    "$2B — Mega Bull": 2000000000,
    "$3B — Euphoria": 3000000000,
    "$5B — Full Degen": 5000000000,
    "$10B — Hyperliquid Territory": 10000000000,
}

COMPARABLE_PROTOCOLS = [
    ("Hyperliquid", "$25B"),
    ("Drift", "$800M"),
    ("dYdX", "$600M"),
    ("Vertex", "$120M"),
    ("Aevo", "$100M"),
]


def fmt(value: float, short: bool = False) -> str:
    sign = "-" if value < 0 else ""
    v = abs(value)
    if v >= 1000000000:
        return f"{sign}${v / 1000000000:,.2f}B"
    if v >= 1000000:
        return f"{sign}${v / 1000000:,.1f}M"
    if v >= 1000:
        return f"{sign}${v:,.0f}"
    if v >= 1:
        return f"{sign}${v:,.2f}"
    if v == 0:
        return "$0.00"
    digits = 2
    tmp = v
    while tmp < 1 and digits < 6:
        tmp *= 10
        digits += 1
    return f"{sign}${v:,.{digits}f}"


def fmt_card(value: float) -> str:
    """Compact formatting optimized for the share card."""
    sign = "-" if value < 0 else ""
    v = abs(value)
    if v >= 1000000000:
        return f"{sign}${v / 1000000000:,.1f}B"
    if v >= 1000000:
        return f"{sign}${v / 1000000:,.1f}M"
    if v >= 1000:
        return f"{sign}${v:,.0f}"
    if v >= 1:
        return f"{sign}${v:,.2f}"
    if v == 0:
        return "$0"
    return f"{sign}${v:.4f}"


def get_b64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


st.set_page_config(page_title="Hibachi — Reality Check", page_icon="🔥", layout="centered")

logo = get_b64(os.path.join(os.path.dirname(__file__), "hibachi.png"))
logo_tag = f'<img src="data:image/png;base64,{logo}" class="logo" />' if logo else ""

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {{
  --black: #000000;
  --card: rgba(255,255,255,0.025);
  --border: rgba(255,255,255,0.06);
  --border-focus: rgba(212,165,116,0.35);
  --t1: #f0f0f0;
  --t2: #a0a0a0;
  --t3: #5a5a5a;
  --warm: #c9956a;
  --warm2: #a87b5a;
  --green: #34d399;
  --red: #ef4444;
}}

html, body, .stApp {{
  background: var(--black) !important;
  color: var(--t1) !important;
  font-family: 'Inter', sans-serif !important;
}}

.block-container {{
  max-width: 680px !important;
  padding: 1.5rem 1rem 4rem !important;
}}

header[data-testid="stHeader"],
.stDeployButton,
#MainMenu,
footer,
[data-testid="stSidebar"] {{
  display: none !important;
}}

/* header */
.hdr {{
  text-align: center;
  padding: 1.5rem 0 2rem;
}}
.logo {{
  width: 56px;
  height: 56px;
  border-radius: 14px;
  margin-bottom: 0.8rem;
  filter: drop-shadow(0 0 20px rgba(200,140,80,0.2));
}}
.hdr h1 {{
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: var(--t1);
  margin: 0 0 0.2rem;
}}
.hdr p {{
  color: var(--t3);
  font-size: 0.78rem;
  margin: 0;
  font-weight: 400;
}}

/* card */
.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem 1.3rem;
  margin-bottom: 0.8rem;
}}
.card-title {{
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--t3);
  margin-bottom: 0.8rem;
}}

/* rows */
.row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}}
.row:last-child {{ border-bottom: none; }}
.row .k {{ font-size: 0.82rem; color: var(--t2); }}
.row .v {{
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--t1);
  font-variant-numeric: tabular-nums;
}}
.row .v.warm {{
  color: var(--warm);
}}
.row .v.green {{ color: var(--green); }}
.row .v.red {{ color: var(--red); }}

/* comparable pills */
.comps {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.5rem;
}}
.pill {{
  font-size: 0.72rem;
  padding: 0.3rem 0.7rem;
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  color: var(--t2);
  font-weight: 500;
}}

/* table */
.sc-table {{
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  margin-top: 0.6rem;
}}
.sc-table th {{
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--t3);
  text-align: left;
  padding: 0.5rem 0.4rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.sc-table th:nth-child(1) {{ width: 30%; }}
.sc-table th:nth-child(2) {{ width: 35%; }}
.sc-table th:nth-child(3) {{ width: 35%; text-align: right; }}
.sc-table td {{
  font-size: 0.82rem;
  color: var(--t2);
  padding: 0.5rem 0.4rem;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  font-variant-numeric: tabular-nums;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.sc-table td:last-child {{
  text-align: right;
  font-weight: 600;
  color: var(--t1);
}}
.sc-table tr.active td {{
  color: var(--warm);
  font-weight: 600;
}}
.sc-table tr.active td:last-child {{
  color: var(--warm);
}}

/* streamlit inputs */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {{
  color: var(--t2) !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
}}
div[data-testid="stNumberInput"] input {{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--t1) !important;
  font-weight: 600 !important;
  font-family: 'Inter', sans-serif !important;
}}
div[data-testid="stNumberInput"] input:focus {{
  border-color: var(--border-focus) !important;
  box-shadow: 0 0 0 1px rgba(212,165,116,0.1) !important;
}}
div[data-testid="stSelectbox"] > div > div {{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--t1) !important;
}}

.sep {{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  margin: 1.2rem 0;
}}

/* ── mobile ── */
@media (max-width: 640px) {{
  .block-container {{
    padding: 1rem 0.5rem 3rem !important;
  }}
  .sc-table td, .sc-table th {{
    font-size: 0.72rem;
    padding: 0.4rem 0.3rem;
  }}
}}
</style>

<div class="hdr">
  {logo_tag}
  <h1>HIBACHI REALITY CHECK</h1>
  <p>No hype, no copium. Just your real airdrop math.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── INPUTS ──
c1, c2 = st.columns(2)
with c1:
    total_points = st.number_input(
        "Your Points / Tokens",
        min_value=0.0,
        value=170000.0,
        step=1000.0,
    )
with c2:
    avg_cost = st.number_input(
        "Avg Cost per Point ($)",
        min_value=0.0,
        value=0.19,
        step=0.0001,
        format="%.4f",
    )

c3, c4 = st.columns(2)
with c3:
    total_supply = st.number_input(
        "Total Token Supply",
        min_value=1.0,
        value=1000000000.0,
        step=100000000.0,
    )
with c4:
    fdv_choice = st.selectbox(
        "Expected FDV at Listing",
        options=list(FDV_PRESETS.keys()),
        index=1,
    )
target_fdv = FDV_PRESETS[fdv_choice]

goal = st.number_input(
    "Target Net Profit — how much $ you need to walk away happy?",
    min_value=0.0,
    value=150000.0,
    step=5000.0,
)

# comparable protocols
comps_html = "".join(f'<span class="pill">{n} · {v}</span>' for n, v in COMPARABLE_PROTOCOLS)
st.markdown(
    f'<div class="card"><div class="card-title">Comparable Perp DEX FDVs</div>'
    f'<div class="comps">{comps_html}</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

# ── MATH ──
token_price = target_fdv / total_supply
total_spent = total_points * avg_cost
gross_value = total_points * token_price
net_profit = gross_value - total_spent
roi = (net_profit / total_spent * 100) if total_spent > 0 else 0
venture_x = target_fdv / BASELINE_FDV

if total_points > 0:
    required_fdv = ((goal + total_spent) / total_points) * total_supply
else:
    required_fdv = float("inf")

# ── BREAKDOWN ──
pnl_class = "green" if net_profit >= 0 else "red"

st.markdown(f"""
<div class="card">
  <div class="card-title">Breakdown</div>
  <div class="row"><span class="k">Token Price (FDV / Supply)</span><span class="v warm">{fmt(token_price)}</span></div>
  <div class="row"><span class="k">You Spent ({total_points:,.0f} pts x {avg_cost:.4f})</span><span class="v">{fmt(total_spent)}</span></div>
  <div class="row"><span class="k">Gross Value ({total_points:,.0f} pts x {token_price:.4f})</span><span class="v">{fmt(gross_value)}</span></div>
  <div class="row"><span class="k">Venture Multiplier (vs $80M seed)</span><span class="v">{venture_x:.1f}x</span></div>
</div>
""", unsafe_allow_html=True)

# ── RESULT CARD (Net Profit + Stats + Verdict + Share) ──
fdv_label = fdv_choice.split(chr(8212))[0].strip()

if net_profit >= goal and total_points > 0:
    emoji = "🎯"
elif net_profit >= 0:
    emoji = "📈"
else:
    emoji = "💀"

tweet_lines = [
    f"{emoji} My @hibachi_xyz reality check is in.",
    f"",
    f"Are you cooked or cooking? Find out 👇",
    f"https://hibachi.streamlit.app/",
]
tweet_text = urllib.parse.quote("\n".join(tweet_lines))
tweet_url = f"https://twitter.com/intent/tweet?text={tweet_text}"

roi_class = "green" if roi > 0 else "red"

if total_points > 0 and net_profit >= goal:
    badge_cls = "ok"
    badge_txt = "GOAL HIT"
elif total_points > 0 and net_profit >= 0:
    badge_cls = "ok"
    badge_txt = "PROFIT"
elif total_points > 0:
    badge_cls = "no"
    badge_txt = "REKT"
else:
    badge_cls = "no"
    badge_txt = "NO DATA"

logo_src = f"data:image/png;base64,{logo}" if logo else ""
tweet_url_escaped = tweet_url.replace("'", "\\'")

share_component = f"""
<html>
<head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; font-family:'Inter',sans-serif; }}

  #card {{
    width: 580px;
    background: linear-gradient(160deg, #0c0806 0%, #1a0f08 30%, #12080e 70%, #0a0508 100%);
    border: 1px solid rgba(201,149,106,0.2);
    border-radius: 20px;
    padding: 28px 28px 20px;
    position: relative;
    overflow: hidden;
    margin: 0 auto;
  }}
  #card::before {{
    content:'';
    position:absolute;
    top:0;left:0;right:0;bottom:0;
    background:
      radial-gradient(ellipse at 15% 20%, rgba(201,149,106,0.08) 0%, transparent 50%),
      radial-gradient(ellipse at 85% 80%, rgba(180,80,140,0.06) 0%, transparent 50%);
    pointer-events:none;
  }}
  #card > * {{ position:relative; z-index:1; }}

  .top {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }}
  .brand {{ display:flex; align-items:center; gap:10px; }}
  .brand img {{ width:32px; height:32px; border-radius:9px; }}
  .brand-text .name {{ font-size:14px; font-weight:700; color:#f0f0f0; display:block; }}
  .brand-text .tag {{ font-size:10px; color:#5a5a5a; font-weight:500; display:block; }}
  .badge {{
    padding:5px 14px; border-radius:20px;
    font-size:11px; font-weight:700; letter-spacing:0.5px; text-transform:uppercase;
  }}
  .badge.ok {{ background:rgba(52,211,153,0.12); color:#34d399; }}
  .badge.no {{ background:rgba(239,68,68,0.12); color:#ef4444; }}

  .hero {{ text-align:center; padding:10px 0 18px; }}
  .hero .lbl {{
    font-size:10px; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:#5a5a5a; margin-bottom:6px;
  }}
  .hero .num {{
    font-size:52px; font-weight:800; letter-spacing:-3px;
    font-variant-numeric:tabular-nums; line-height:1;
  }}
  .hero .num.green {{ color:#34d399; }}
  .hero .num.red {{ color:#ef4444; }}

  .grid {{
    display:grid; grid-template-columns:repeat(4,1fr);
    padding:14px 0;
    border-top:1px solid rgba(255,255,255,0.05);
    border-bottom:1px solid rgba(255,255,255,0.05);
    margin:4px 0 14px;
  }}
  .cell {{ text-align:center; padding:4px 0; }}
  .cell:not(:last-child) {{ border-right:1px solid rgba(255,255,255,0.04); }}
  .cell .cl {{ font-size:9px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; color:#5a5a5a; margin-bottom:4px; }}
  .cell .cv {{ font-size:15px; font-weight:700; color:#f0f0f0; font-variant-numeric:tabular-nums; }}
  .cell .cv.warm {{ color:#c9956a; }}
  .cell .cv.green {{ color:#34d399; }}
  .cell .cv.red {{ color:#ef4444; }}

  .bottom {{ display:flex; justify-content:space-between; align-items:center; }}
  .bottom .hint {{ font-size:11px; color:#5a5a5a; font-weight:500; }}
  .bottom .url {{ font-size:11px; color:#c9956a; font-weight:600; }}

  @media (max-width: 620px) {{
    #card {{ width:100%; padding:20px 16px 16px; border-radius:14px; }}
    .hero .num {{ font-size:36px; letter-spacing:-2px; }}
    .grid {{ grid-template-columns: repeat(2,1fr); }}
    .cell:nth-child(2) {{ border-right:none; }}
    .cell {{ padding:6px 0; }}
    .top {{ flex-direction:column; gap:8px; align-items:flex-start; }}
    .actions {{ flex-direction:column; gap:6px; }}
    .btn {{ width:100%; justify-content:center; }}
  }}

  .actions {{
    display:flex; align-items:center; justify-content:center;
    gap:10px; margin-top:14px;
  }}
  .btn {{
    display:inline-flex; align-items:center; gap:6px;
    padding:10px 22px;
    background:rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:10px;
    color:#f0f0f0;
    font-size:13px; font-weight:600;
    cursor:pointer;
    font-family:'Inter',sans-serif;
    transition: all 0.2s;
  }}
  .btn:hover {{
    background:rgba(255,255,255,0.1);
    border-color:rgba(201,149,106,0.3);
    color:#c9956a;
  }}
  .btn.primary {{
    background:rgba(201,149,106,0.15);
    border-color:rgba(201,149,106,0.3);
    color:#c9956a;
  }}
  .btn.primary:hover {{
    background:rgba(201,149,106,0.25);
  }}
  #status {{
    text-align:center;
    margin-top:8px;
    font-size:12px;
    color:#34d399;
    font-weight:500;
    min-height:18px;
  }}
</style>
</head>
<body>

<div id="card">
  <div class="top">
    <div class="brand">
      <img src="{logo_src}" alt="">
      <div class="brand-text">
        <span class="name">Hibachi Reality Check</span>
        <span class="tag">@hibachi_xyz</span>
      </div>
    </div>
    <span class="badge {badge_cls}">{badge_txt}</span>
  </div>
  <div class="hero">
    <div class="lbl">Net Profit</div>
    <div class="num {pnl_class}">{fmt_card(net_profit)}</div>
  </div>
  <div class="grid">
    <div class="cell"><div class="cl">Invested</div><div class="cv">{fmt_card(total_spent)}</div></div>
    <div class="cell"><div class="cl">Gross</div><div class="cv">{fmt_card(gross_value)}</div></div>
    <div class="cell"><div class="cl">ROI</div><div class="cv {roi_class}">{roi:+,.1f}%</div></div>
    <div class="cell"><div class="cl">FDV</div><div class="cv warm">{fdv_label}</div></div>
  </div>
  <div class="bottom">
    <span class="hint">Are you cooked or cooking?</span>
    <span class="url">hibachi.streamlit.app</span>
  </div>
</div>

<div class="actions">
  <button class="btn primary" onclick="copyAndTweet()">📋 Copy & Post on 𝕏</button>
  <button class="btn" onclick="downloadCard()">📥 Download</button>
</div>
<div id="status"></div>

<script>
async function captureCard() {{
  const card = document.getElementById('card');
  return html2canvas(card, {{
    backgroundColor: null,
    scale: 2,
    useCORS: true,
    logging: false
  }});
}}

async function copyAndTweet() {{
  const statusEl = document.getElementById('status');
  statusEl.textContent = 'Capturing...';
  try {{
    const canvas = await captureCard();
    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
    await navigator.clipboard.write([
      new ClipboardItem({{ 'image/png': blob }})
    ]);
    statusEl.textContent = '✅ Copied! Paste (Cmd+V) in the tweet window';
    setTimeout(() => {{
      window.open('{tweet_url_escaped}', '_blank');
    }}, 600);
  }} catch(e) {{
    statusEl.textContent = '⚠️ Clipboard blocked — downloading instead...';
    downloadCard();
    setTimeout(() => {{
      window.open('{tweet_url_escaped}', '_blank');
    }}, 800);
  }}
}}

async function downloadCard() {{
  const statusEl = document.getElementById('status');
  statusEl.textContent = 'Capturing...';
  const canvas = await captureCard();
  const link = document.createElement('a');
  link.download = 'hibachi-reality-check.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
  statusEl.textContent = '✅ Downloaded! Attach it to your tweet';
}}
</script>
</body></html>
"""

components.html(share_component, height=380)

# Share on X — always visible (especially on mobile)
st.markdown(
    '<p style="text-align:center; margin:0.5rem 0 1rem; font-size:0.8rem; color:#71717a;">'
    "Screenshot the card above, then open the tweet and paste the image (or use Download).</p>",
    unsafe_allow_html=True,
)
st.link_button(
    "Share on X (open tweet)",
    tweet_url,
    type="primary",
    use_container_width=True,
)

# ── SCENARIO TABLE ──
scenarios = [50000000, 200000000, 500000000, 1000000000, 2000000000, 5000000000, 10000000000]
rows_html = ""
for fdv_s in scenarios:
    price_s = fdv_s / total_supply
    net_s = (total_points * price_s) - total_spent
    cls = ' class="active"' if fdv_s == target_fdv else ""
    color_cls = "green" if net_s >= 0 else "red"
    rows_html += (
        f"<tr{cls}>"
        f"<td>{fmt(fdv_s)}</td>"
        f"<td>{fmt(price_s)}</td>"
        f'<td style="color: var(--{color_cls})">{fmt(net_s)}</td>'
        f"</tr>"
    )

st.markdown(f"""
<div class="card">
  <div class="card-title">Your Profit Across FDV Scenarios</div>
  <table class="sc-table">
    <thead><tr><th>FDV</th><th>Token Price</th><th>Net Profit</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

# ── COMPARISON MODE ──
st.markdown("""
<div class="card">
  <div class="card-title">Compare — Hibachi vs Another Drop</div>
</div>
""", unsafe_allow_html=True)

with st.expander("Open Comparison Mode", expanded=False):
    b_name = st.text_input("Project B Name", value="", placeholder="e.g. Lighter, Ethereal, Aster...")

    cc1, cc2 = st.columns(2)
    with cc1:
        b_points = st.number_input(
            f"Points ({b_name or 'Project B'})",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            key="b_points",
        )
    with cc2:
        b_cost = st.number_input(
            f"Cost per Point ({b_name or 'Project B'})",
            min_value=0.0,
            value=0.0,
            step=0.0001,
            format="%.4f",
            key="b_cost",
        )

    cc3, cc4 = st.columns(2)
    with cc3:
        b_supply = st.number_input(
            f"Token Supply ({b_name or 'Project B'})",
            min_value=1.0,
            value=1000000000.0,
            step=100000000.0,
            key="b_supply",
        )
    with cc4:
        b_fdv_choice = st.selectbox(
            f"FDV ({b_name or 'Project B'})",
            options=list(FDV_PRESETS.keys()),
            index=3,
            key="b_fdv",
        )
    b_fdv = FDV_PRESETS[b_fdv_choice]

    b_label = b_name if b_name else "Project B"

    if b_points > 0 and b_cost > 0:
        b_price = b_fdv / b_supply
        b_spent = b_points * b_cost
        b_gross = b_points * b_price
        b_net = b_gross - b_spent
        b_roi = (b_net / b_spent * 100) if b_spent > 0 else 0

        a_class = "green" if net_profit >= 0 else "red"
        b_class = "green" if b_net >= 0 else "red"

        if net_profit > b_net:
            winner = "Hibachi 🔥"
        elif b_net > net_profit:
            winner = f"{b_label}"
        else:
            winner = "Tie"
        w_class = "warm"

        st.markdown(f"""
<div class="card" style="margin-top: 0.8rem;">
  <div class="card-title">Head to Head</div>
  <table class="sc-table">
    <thead>
      <tr><th style="width:34%"></th><th style="width:33%">HIBACHI</th><th style="width:33%; text-align:right">{b_label.upper()}</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>FDV</td>
        <td>{fmt(target_fdv)}</td>
        <td style="text-align:right">{fmt(b_fdv)}</td>
      </tr>
      <tr>
        <td>Invested</td>
        <td>{fmt(total_spent)}</td>
        <td style="text-align:right">{fmt(b_spent)}</td>
      </tr>
      <tr>
        <td>Net Profit</td>
        <td style="color:var(--{a_class}); font-weight:700">{fmt(net_profit)}</td>
        <td style="text-align:right; color:var(--{b_class}); font-weight:700">{fmt(b_net)}</td>
      </tr>
      <tr>
        <td>ROI</td>
        <td style="color:var(--{a_class})">{roi:+,.1f}%</td>
        <td style="text-align:right; color:var(--{b_class})">{b_roi:+,.1f}%</td>
      </tr>
    </tbody>
  </table>
  <div style="text-align:center; margin-top:1rem; padding-top:0.8rem; border-top: 1px solid rgba(255,255,255,0.04);">
    <span style="font-size:0.7rem; letter-spacing:1.2px; text-transform:uppercase; color:var(--t3);">Winner</span><br/>
    <span style="font-size:1.1rem; font-weight:700; color:var(--{w_class})">{winner}</span>
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<p style="color: #5a5a5a; font-size: 0.82rem; text-align:center; margin-top:0.5rem;">
  Fill in {b_label} details above to compare.
</p>
""", unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center;color:#333;font-size:0.7rem;margin-top:2rem;">'
    "For educational purposes only. Not financial advice.</p>",
    unsafe_allow_html=True,
)
