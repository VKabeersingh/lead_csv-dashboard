import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import copy
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LeadLens · Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES  — Glassmorphism + Neon
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin:0; padding:0; }

html, body, .stApp {
    background: #020817 !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,212,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(147,51,234,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0,255,163,0.04) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
    animation: meshPulse 8s ease-in-out infinite alternate;
}
@keyframes meshPulse { 0%{opacity:.7} 100%{opacity:1} }

.stApp::after {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
}

section[data-testid="stSidebar"] {
    background: rgba(2,8,23,0.85) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(0,212,255,0.15) !important;
    z-index: 10;
}
section[data-testid="stSidebar"] > div { background: transparent !important; }
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(0,212,255,0.12) !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.2rem !important; max-width: 100% !important; position: relative; z-index: 1; }

.stRadio > label { color: #475569 !important; font-size: 10px !important; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; }
.stRadio div[role="radiogroup"] label {
    color: #64748b !important; font-size: 13px !important;
    padding: 9px 14px; border-radius: 10px;
    border: 1px solid transparent; transition: all 0.2s ease; margin-bottom: 2px;
}
.stRadio div[role="radiogroup"] label:hover {
    background: rgba(0,212,255,0.06) !important;
    border-color: rgba(0,212,255,0.2) !important; color: #00d4ff !important;
}

@keyframes fadeSlideUp {
    from { opacity:0; transform: translateY(16px); }
    to   { opacity:1; transform: translateY(0); }
}

.kpi-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px; padding: 22px 20px 18px;
    position: relative; overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeSlideUp 0.5s ease both;
}
.kpi-card:hover { transform: translateY(-3px); border-color: var(--accent,rgba(0,212,255,.4)); box-shadow: 0 0 40px var(--glow-soft,rgba(0,212,255,.1)), 0 12px 40px rgba(0,0,0,.5); }
.kpi-card.cyan   { --accent:rgba(0,212,255,.4);   --glow-soft:rgba(0,212,255,.15); }
.kpi-card.purple { --accent:rgba(168,85,247,.4);  --glow-soft:rgba(168,85,247,.15); }
.kpi-card.green  { --accent:rgba(0,255,163,.4);   --glow-soft:rgba(0,255,163,.15); }
.kpi-card.amber  { --accent:rgba(251,191,36,.4);  --glow-soft:rgba(251,191,36,.15); }
.kpi-card.red    { --accent:rgba(248,113,113,.4); --glow-soft:rgba(248,113,113,.15); }

.kpi-topbar { height:2px; width:40px; border-radius:2px; margin-bottom:14px; }
.cyan   .kpi-topbar { background:linear-gradient(90deg,#00d4ff,#0ea5e9); box-shadow:0 0 12px #00d4ff; }
.purple .kpi-topbar { background:linear-gradient(90deg,#a855f7,#8b5cf6); box-shadow:0 0 12px #a855f7; }
.green  .kpi-topbar { background:linear-gradient(90deg,#00ffa3,#10b981); box-shadow:0 0 12px #00ffa3; }
.amber  .kpi-topbar { background:linear-gradient(90deg,#fbbf24,#f59e0b); box-shadow:0 0 12px #fbbf24; }
.red    .kpi-topbar { background:linear-gradient(90deg,#f87171,#ef4444); box-shadow:0 0 12px #f87171; }

.kpi-icon  { font-size:20px; margin-bottom:8px; }
.kpi-label { font-size:11px; color:#475569; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }
.kpi-value { font-size:26px; font-weight:700; color:#f8fafc; letter-spacing:-0.5px; font-family:'Space Mono',monospace; }
.kpi-delta { font-size:11px; margin-top:5px; }
.kpi-delta.pos{color:#00ffa3} .kpi-delta.neg{color:#f87171} .kpi-delta.neu{color:#475569}

.sec-title {
    font-size:16px; font-weight:600; color:#e2e8f0;
    letter-spacing:-0.3px; margin-bottom:14px;
    display:flex; align-items:center; gap:8px;
}
.sec-title::before {
    content:''; display:inline-block; width:3px; height:16px; border-radius:2px;
    background:linear-gradient(180deg,#00d4ff,#a855f7); box-shadow:0 0 8px #00d4ff;
}

.ins-card {
    border-radius:14px; padding:15px 16px; border:1px solid;
    margin-bottom:10px; display:flex; gap:12px; align-items:flex-start;
    backdrop-filter:blur(12px); animation:fadeSlideUp 0.4s ease both; transition:all 0.2s ease;
}
.ins-card:hover{transform:translateX(4px)}
.ins-card.good{background:rgba(0,255,163,.05);border-color:rgba(0,255,163,.2)}
.ins-card.bad {background:rgba(248,113,113,.05);border-color:rgba(248,113,113,.2)}
.ins-card.warn{background:rgba(251,191,36,.05);border-color:rgba(251,191,36,.2)}
.ins-card.info{background:rgba(0,212,255,.05);border-color:rgba(0,212,255,.2)}
.ins-icon {font-size:20px;flex-shrink:0;margin-top:1px}
.ins-title{font-weight:600;font-size:13px;color:#f1f5f9;margin-bottom:3px}
.ins-desc {font-size:12px;color:#64748b;line-height:1.6}

.rec-pill {
    display:flex; align-items:flex-start; gap:10px;
    background:rgba(255,255,255,.03); backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,.07); color:#cbd5e1; font-size:13px;
    padding:12px 16px; border-radius:12px; margin-bottom:8px;
    transition:all 0.2s ease; animation:fadeSlideUp 0.4s ease both;
}
.rec-pill:hover{border-color:rgba(0,212,255,.25);background:rgba(0,212,255,.04)}
.rec-badge {
    font-size:9px;font-weight:700;padding:3px 8px;border-radius:20px;
    letter-spacing:1px;text-transform:uppercase;flex-shrink:0;margin-top:1px;
}
.rec-badge.high  {background:rgba(248,113,113,.2);color:#f87171;border:1px solid rgba(248,113,113,.4)}
.rec-badge.medium{background:rgba(251,191,36,.2) ;color:#fbbf24;border:1px solid rgba(251,191,36,.4)}
.rec-badge.low   {background:rgba(0,255,163,.15) ;color:#00ffa3;border:1px solid rgba(0,255,163,.3)}

.risk-item {
    display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:12px;
    background:rgba(255,255,255,.025);backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,.06);margin-bottom:8px;
    transition:all 0.2s ease;animation:fadeSlideUp 0.4s ease both;
}
.risk-item:hover{border-color:rgba(0,212,255,.2)}
.risk-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;animation:dotPulse 2s ease-in-out infinite}
.risk-dot.high  {background:#f87171;box-shadow:0 0 10px #f87171}
.risk-dot.medium{background:#fbbf24;box-shadow:0 0 10px #fbbf24}
.risk-dot.low   {background:#00ffa3;box-shadow:0 0 10px #00ffa3}
@keyframes dotPulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.5);opacity:.6}}
.risk-text {font-size:13px;color:#94a3b8;flex:1;line-height:1.5}
.risk-level{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase}
.risk-level.high{color:#f87171}.risk-level.medium{color:#fbbf24}.risk-level.low{color:#00ffa3}

.pred-card {
    background:rgba(147,51,234,.08);backdrop-filter:blur(20px);
    border:1px solid rgba(147,51,234,.25);border-radius:18px;padding:22px;
    text-align:center;transition:all 0.3s ease;animation:fadeSlideUp 0.5s ease both;
}
.pred-card:hover{border-color:rgba(168,85,247,.5);box-shadow:0 0 40px rgba(147,51,234,.2);transform:translateY(-3px)}
.pred-month{font-size:11px;color:#7c3aed;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px}
.pred-value{font-size:30px;font-weight:700;color:#a855f7;font-family:'Space Mono';letter-spacing:-1px}
.pred-note {font-size:11px;color:#6d28d9;margin-top:6px}

.pg-header{margin-bottom:2rem;animation:fadeSlideUp 0.4s ease both}
.pg-badge {
    display:inline-block;
    background:linear-gradient(135deg,rgba(0,212,255,.15),rgba(168,85,247,.15));
    border:1px solid rgba(0,212,255,.3);color:#00d4ff;font-size:10px;font-weight:600;
    padding:3px 12px;border-radius:20px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;
}
.pg-title{font-size:30px;font-weight:700;color:#f8fafc;letter-spacing:-0.8px;line-height:1.2}
.pg-sub {color:#475569;font-size:13px;margin-top:5px}

.neon-hr{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,.3),transparent);margin:1.5rem 0}

.info-box {
    background:rgba(255,255,255,.025);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:22px;margin-bottom:14px;
    animation:fadeSlideUp 0.4s ease both;
}
.info-box h3{color:#e2e8f0;font-size:15px;font-weight:600;margin-bottom:10px}
.feat-tag{display:inline-block;background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.2);color:#00d4ff;font-size:11px;padding:4px 10px;border-radius:8px;margin:3px}

.stProgress > div > div{background:rgba(255,255,255,.06)!important;border-radius:99px}
.stProgress > div > div > div{background:linear-gradient(90deg,#00d4ff,#a855f7)!important;border-radius:99px;box-shadow:0 0 12px rgba(0,212,255,.5)}
div[data-testid="stFileUploader"]{background:rgba(255,255,255,.02);border:2px dashed rgba(0,212,255,.2);border-radius:16px;padding:8px;transition:all 0.2s ease;backdrop-filter:blur(12px)}
div[data-testid="stFileUploader"]:hover{border-color:rgba(0,212,255,.5);background:rgba(0,212,255,.04)}
.stButton>button{background:linear-gradient(135deg,rgba(0,212,255,.15),rgba(168,85,247,.15))!important;border:1px solid rgba(0,212,255,.3)!important;color:#00d4ff!important;border-radius:12px!important;font-weight:600!important;font-family:'Space Grotesk'!important;transition:all 0.2s ease!important}
.stButton>button:hover{background:linear-gradient(135deg,rgba(0,212,255,.25),rgba(168,85,247,.25))!important;box-shadow:0 0 20px rgba(0,212,255,.3)!important}
.stNumberInput input,.stSelectbox select,.stTextInput input{background:rgba(255,255,255,.04)!important;color:#e2e8f0!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:10px!important;backdrop-filter:blur(12px)!important}
.stExpander{background:rgba(255,255,255,.02)!important;border:1px solid rgba(255,255,255,.07)!important;border-radius:14px!important;backdrop-filter:blur(12px)!important}
label,.stSelectbox label,.stNumberInput label,.stMultiSelect label{color:#475569!important;font-size:12px!important;letter-spacing:.5px}
.stDataFrame{border-radius:12px;overflow:hidden}

@keyframes glowPulse{0%,100%{text-shadow:0 0 10px rgba(0,212,255,.5),0 0 20px rgba(0,212,255,.3)}50%{text-shadow:0 0 20px rgba(0,212,255,.8),0 0 40px rgba(0,212,255,.5)}}
.glow-text{animation:glowPulse 3s ease-in-out infinite}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BUG-FREE CHART LAYOUT HELPER
#  Deep-merges overrides so no duplicate-key TypeError
# ─────────────────────────────────────────────
_BASE_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748b", family="Space Grotesk, sans-serif", size=12),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.05)",
               tickcolor="rgba(255,255,255,0.1)", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.05)",
               tickcolor="rgba(255,255,255,0.1)", showgrid=True, zeroline=False),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.06)",
                borderwidth=1, font=dict(color="#64748b")),
    hoverlabel=dict(bgcolor="rgba(2,8,23,0.9)", bordercolor="rgba(0,212,255,0.3)",
                    font=dict(color="#e2e8f0", family="Space Grotesk")),
)

def chart_layout(**overrides):
    """Deep-merge overrides into base layout — prevents duplicate-key TypeError."""
    layout = copy.deepcopy(_BASE_LAYOUT)
    for k, v in overrides.items():
        if k in layout and isinstance(layout[k], dict) and isinstance(v, dict):
            layout[k].update(v)
        else:
            layout[k] = v
    return layout


PALETTE = ["#00d4ff","#a855f7","#00ffa3","#fbbf24","#f87171","#38bdf8","#fb7185","#34d399"]


# ─────────────────────────────────────────────
#  HELPER WIDGETS
# ─────────────────────────────────────────────
def kpi(col, icon, label, value, delta_text="", delta_pos=None, color="cyan"):
    pos = "pos" if delta_pos else ("neg" if delta_pos is False else "neu")
    col.markdown(f"""
<div class='kpi-card {color}'>
  <div class='kpi-topbar'></div>
  <div class='kpi-icon'>{icon}</div>
  <div class='kpi-label'>{label}</div>
  <div class='kpi-value'>{value}</div>
  <div class='kpi-delta {pos}'>{delta_text}</div>
</div>""", unsafe_allow_html=True)

def insight(kind, icon, title, desc):
    st.markdown(f"""
<div class='ins-card {kind}'>
  <div class='ins-icon'>{icon}</div>
  <div><div class='ins-title'>{title}</div><div class='ins-desc'>{desc}</div></div>
</div>""", unsafe_allow_html=True)

def risk_item(level, text):
    st.markdown(f"""
<div class='risk-item'>
  <div class='risk-dot {level}'></div>
  <div class='risk-text'>{text}</div>
  <div class='risk-level {level}'>{level.upper()}</div>
</div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f"<div class='sec-title'>{title}</div>", unsafe_allow_html=True)

def neon_hr():
    st.markdown("<div class='neon-hr'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file) if file.name.lower().endswith("csv") else pd.read_excel(file)
    cols_lower = {c.strip().lower(): c for c in df.columns}

    def find(*keys):
        for k in keys:
            for cl, co in cols_lower.items():
                if k in cl:
                    return co
        return None

    status_col = find("status","stage","state","result")
    source_col = find("source","channel","medium","campaign","utm")
    rev_col    = find("revenue","amount","value","deal","sale","price")
    date_col   = find("date","created","time","closed","opened")
    cost_col   = find("cost","spend","budget","expense","cac")
    region_col = find("region","area","territory","location","city","country")
    owner_col  = find("owner","rep","agent","assignee","salesperson","manager")

    if status_col:
        df[status_col] = df[status_col].astype(str).str.strip().str.lower()
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    return df, status_col, source_col, rev_col, date_col, cost_col, region_col, owner_col


def is_won(series):
    return series.isin(["won","closed","converted","sale","deal","yes","true","1",
                         "success","complete","completed","paid"])

def fmt_inr(n):
    n = float(n) if n else 0
    if n >= 1e7:  return f"₹{n/1e7:.2f}Cr"
    if n >= 1e5:  return f"₹{n/1e5:.1f}L"
    if n >= 1e3:  return f"₹{n/1e3:.1f}K"
    return f"₹{n:,.0f}"

def simple_forecast(vals, periods=3):
    x = np.arange(len(vals))
    if len(x) < 2: return [vals[-1]] * periods
    m, b = np.polyfit(x, vals, 1)
    return [max(0, m*(len(x)+i)+b) for i in range(periods)]


# ─────────────────────────────────────────────
#  SIDEBAR (FIXED WITH TOGGLE CONTROL)
# ─────────────────────────────────────────────
with st.sidebar:

    # Sidebar header
    st.markdown("""
<div style='padding:4px 0 12px'>
  <div style='font-size:22px;font-weight:700;color:#f8fafc;letter-spacing:-0.5px' class='glow-text'>⚡ LeadLens</div>
  <div style='font-size:11px;color:#334155;letter-spacing:1px;text-transform:uppercase;margin-top:4px'>Intelligence Suite</div>
</div>""", unsafe_allow_html=True)

    # 🔥 Toggle info (UX improvement)
    st.info("💡 Use the top-left arrow to collapse / expand sidebar")

    st.markdown("<hr style='border-color:rgba(0,212,255,0.12);margin:0 0 16px'>", unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        ["📊  Dashboard", "💡  Insights & AI", "🗺️  Channel Deep-Dive",
         "📈  Predictions", "⚠️  Risks", "ℹ️  How It Works"],
        label_visibility="visible",
    )

    st.markdown("<hr style='border-color:rgba(0,212,255,0.12);margin:16px 0'>", unsafe_allow_html=True)

    st.markdown("""
<div style='font-size:10px;color:#1e293b;line-height:2;text-transform:uppercase;letter-spacing:1px'>
AUTO-DETECTED COLS<br>
<span style='color:#334155'>Status · Source · Revenue<br>
Date · Cost · Region · Owner</span><br><br>
FORMATS<br><span style='color:#334155'>.csv · .xlsx</span>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HOW IT WORKS PAGE
# ─────────────────────────────────────────────
if page == "ℹ️  How It Works":
    st.markdown("""
<div class='pg-header'>
  <div class='pg-badge'>Guide</div>
  <div class='pg-title'>How LeadLens Works</div>
  <div class='pg-sub'>Upload any CSV or Excel — auto-detects columns and builds your complete analysis</div>
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class='info-box'>
<h3>🎯 What this dashboard does</h3>
<p style='color:#64748b;font-size:13px;line-height:1.9'>
• Auto-detects column types (status, source, revenue, date, cost…)<br>
• Calculates conversion, ROI, revenue & pipeline velocity<br>
• Identifies best/worst performing channels<br>
• Runs trend analysis + 3-period revenue forecasts<br>
• Surfaces automated insights, recommendations & risks
</p>
</div>
<div class='info-box'>
<h3>📊 Dashboard Sections</h3>
<span class='feat-tag'>📊 Dashboard</span>
<span class='feat-tag'>💡 Insights & AI</span>
<span class='feat-tag'>🗺️ Channel Deep-Dive</span>
<span class='feat-tag'>📈 Predictions</span>
<span class='feat-tag'>⚠️ Risk Analysis</span>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class='info-box'>
<h3>📁 Accepted Formats</h3>
<p style='color:#64748b;font-size:13px;line-height:1.9'>
Upload <span style='color:#00d4ff'>.csv</span> or <span style='color:#00d4ff'>.xlsx</span> files.
Column names are fuzzy-matched — no strict naming required.<br><br>
<b style='color:#94a3b8'>Won values recognised:</b><br>
won · closed · converted · sale · success · complete · paid · yes · true
</p>
</div>
<div class='info-box'>
<h3>⚡ Tips for best results</h3>
<p style='color:#64748b;font-size:13px;line-height:1.9'>
• Include <span style='color:#00ffa3'>Status</span> col with Won/Lost for conversion metrics<br>
• Add a <span style='color:#00ffa3'>Date</span> col to unlock trends & forecasting<br>
• Include <span style='color:#00ffa3'>Cost</span> to see ROI per channel<br>
• Works with any domain: SaaS, real estate, e-com, agencies…
</p>
</div>""", unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
#  FILE UPLOAD
# ─────────────────────────────────────────────
st.markdown("""
<div class='pg-header'>
  <div class='pg-badge'>Lead Intelligence Platform</div>
  <div class='pg-title'>LeadLens Dashboard</div>
  <div class='pg-sub'>Upload your data · Get instant AI-powered insights, predictions & risk analysis</div>
</div>""", unsafe_allow_html=True)

file = st.file_uploader("", type=["csv","xlsx"], label_visibility="collapsed")

if not file:
    st.markdown("""
<div style='text-align:center;padding:80px 20px;animation:fadeSlideUp 0.5s ease'>
  <div style='font-size:52px;margin-bottom:16px'>📂</div>
  <div style='font-size:17px;color:#334155;margin-bottom:6px'>Drop your CSV or Excel file above to get started</div>
  <div style='font-size:12px;color:#1e293b'>Supports any sales, lead, or marketing dataset</div>
</div>""", unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
df, status_col, source_col, rev_col, date_col, cost_col, region_col, owner_col = load_data(file)

total     = len(df)
converted = is_won(df[status_col]).sum() if status_col else 0
revenue   = df[rev_col].sum() if rev_col else 0
cost      = df[cost_col].sum() if cost_col else 0
conv_rate = (converted / total * 100) if total else 0
roi       = ((revenue - cost) / cost * 100) if cost > 0 else 0
avg_deal  = (
    df.loc[is_won(df[status_col]), rev_col].mean()
    if (status_col and rev_col) else (df[rev_col].mean() if rev_col else 0)
) or 0


# ═══════════════════════════════════════════════════════
#  PAGE — DASHBOARD
# ═══════════════════════════════════════════════════════
if page == "📊  Dashboard":

    c1,c2,c3,c4,c5 = st.columns(5)
    kpi(c1,"📋","Total Leads",  f"{total:,}",          "dataset size",  None,             "cyan")
    kpi(c2,"✅","Converted",    f"{converted:,}",       f"{conv_rate:.1f}% rate", conv_rate>20, "green")
    kpi(c3,"💰","Revenue",      fmt_inr(revenue),       "gross revenue", None,             "purple")
    kpi(c4,"📊","ROI",          f"{roi:.1f}%" if cost else "N/A", "on spend", roi>100 if cost else None, "amber")
    kpi(c5,"🎯","Avg Deal",     fmt_inr(avg_deal) if avg_deal else "N/A", "per closed lead", None, "cyan")

    neon_hr()

    left, right = st.columns([1.6,1])
    with left:
        if date_col and rev_col:
            section("Revenue Over Time")
            tmp = df.dropna(subset=[date_col,rev_col]).copy()
            tmp["month"] = tmp[date_col].dt.to_period("M").astype(str)
            trend = tmp.groupby("month")[rev_col].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend["month"], y=trend[rev_col], name="Revenue",
                mode="lines+markers",
                line=dict(color="#00d4ff",width=2.5),
                marker=dict(color="#00d4ff",size=7,line=dict(color="#020817",width=2)),
                fill="tozeroy", fillcolor="rgba(0,212,255,0.06)",
            ))
            fig.update_layout(**chart_layout(height=290))
            st.plotly_chart(fig, use_container_width=True)
        elif source_col:
            section("Channel Performance")
            data = df[source_col].value_counts().reset_index()
            data.columns = ["Channel","Leads"]
            fig = px.bar(data, x="Channel", y="Leads", text="Leads",
                         color="Channel", color_discrete_sequence=PALETTE)
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(**chart_layout(height=290, showlegend=False))
            st.plotly_chart(fig, use_container_width=True)

    with right:
        if status_col:
            section("Lead Status Split")
            vc = df[status_col].value_counts().reset_index()
            vc.columns = ["Status","Count"]
            fig = px.pie(vc, names="Status", values="Count",
                         color_discrete_sequence=PALETTE, hole=0.62)
            fig.update_traces(textinfo="percent+label", textfont_size=11,
                              marker=dict(line=dict(color="#020817",width=2)))
            fig.update_layout(**chart_layout(
                height=290, showlegend=False,
                annotations=[dict(text=f"<b>{total}</b>",x=0.5,y=0.5,
                                  font=dict(size=22,color="#f8fafc"),showarrow=False)]
            ))
            st.plotly_chart(fig, use_container_width=True)

    if source_col and status_col:
        neon_hr()
        section("Conversion Rate by Channel")
        perf = df.groupby(source_col).agg(
            Leads=(source_col,"count"),
            Won=(status_col, lambda x: is_won(x).sum())
        ).reset_index()
        perf["Rate"] = (perf["Won"]/perf["Leads"]*100).round(1)
        perf = perf.sort_values("Rate", ascending=True)
        fig = go.Figure(go.Bar(
            x=perf["Rate"], y=perf[source_col], orientation="h",
            text=[f"{v}%" for v in perf["Rate"]], textposition="outside",
            marker=dict(color=perf["Rate"],
                        colorscale=[[0,"#f87171"],[0.5,"#fbbf24"],[1,"#00ffa3"]],
                        showscale=False, line=dict(width=0)),
        ))
        fig.update_layout(**chart_layout(height=max(220,len(perf)*44)))
        st.plotly_chart(fig, use_container_width=True)

    neon_hr()
    section("Goal Tracker")
    g1,g2 = st.columns([2,1])
    with g1:
        target = st.number_input("Set Revenue Target (₹)", value=int(revenue*1.3) or 50000,
                                 step=10000, format="%d")
    progress = min((revenue/target*100) if target else 0, 100)
    with g2:
        remaining = max(target-revenue, 0)
        st.markdown(f"""
<div class='kpi-card cyan' style='margin-top:28px'>
  <div class='kpi-topbar'></div>
  <div class='kpi-label'>Remaining to Goal</div>
  <div class='kpi-value' style='font-size:18px'>{fmt_inr(remaining)}</div>
</div>""", unsafe_allow_html=True)
    st.progress(int(progress))
    st.caption(f"**{progress:.1f}%** of ₹{target:,} achieved")

    with st.expander("📄 View Raw Data"):
        st.dataframe(df, use_container_width=True)


# ═══════════════════════════════════════════════════════
#  PAGE — INSIGHTS & AI
# ═══════════════════════════════════════════════════════
elif page == "💡  Insights & AI":
    st.markdown("""
<div class='pg-header'>
  <div class='pg-badge'>AI Analysis</div>
  <div class='pg-title'>Insights & Recommendations</div>
</div>""", unsafe_allow_html=True)

    ins_col, rec_col = st.columns(2)

    with ins_col:
        section("🔍 Auto-Generated Insights")

        if status_col and total > 0:
            if conv_rate >= 30:
                insight("good","🏆","Excellent Conversion Rate",
                    f"Your {conv_rate:.1f}% rate is well above the 20% benchmark. Qualifying process is working.")
            elif conv_rate >= 15:
                insight("warn","⚡","Moderate Conversion Rate",
                    f"At {conv_rate:.1f}%, there's room to improve. Tighten ICP criteria or improve follow-up.")
            else:
                insight("bad","🚨","Low Conversion Rate",
                    f"Only {conv_rate:.1f}% convert. Investigate drop-off stages and implement lead scoring urgently.")

        if source_col and status_col:
            perf = df.groupby(source_col).agg(
                leads=(source_col,"count"), won=(status_col, lambda x: is_won(x).sum()))
            perf["rate"] = perf["won"]/perf["leads"]
            best  = perf["rate"].idxmax(); worst = perf["rate"].idxmin()
            best_r = perf.loc[best,"rate"]*100; worst_r = perf.loc[worst,"rate"]*100
            insight("good","🔥",f"Top Channel: {best}",
                f"{best} converts at {best_r:.1f}% — your highest performer. Scale budget here for quick returns.")
            insight("bad","📉",f"Underperforming: {worst}",
                f"{worst} has only {worst_r:.1f}% conversion. Audit lead quality or pause spend.")
            top_vol = perf["leads"].idxmax()
            if top_vol != best:
                insight("warn","⚖️","Volume vs Quality Mismatch",
                    f"{top_vol} sends the most leads but converts at only {perf.loc[top_vol,'rate']*100:.1f}%.")

        if rev_col and source_col:
            rev_s = df.groupby(source_col)[rev_col].sum()
            insight("good","💎",f"Revenue Champion: {rev_s.idxmax()}",
                f"{rev_s.idxmax()} generates {fmt_inr(rev_s.max())} — your highest-value channel.")

        if date_col and rev_col:
            tmp = df.dropna(subset=[date_col,rev_col]).copy()
            tmp["month"] = tmp[date_col].dt.to_period("M").astype(str)
            monthly = tmp.groupby("month")[rev_col].sum()
            if len(monthly) >= 2:
                delta = monthly.iloc[-1] - monthly.iloc[-2]
                pct = delta/monthly.iloc[-2]*100 if monthly.iloc[-2] else 0
                kind = "good" if delta>0 else "bad"; emoji = "📈" if delta>0 else "📉"
                insight(kind,emoji,"Month-on-Month Revenue",
                    f"Last month vs previous: {'+' if delta>=0 else ''}{fmt_inr(delta)} ({pct:+.1f}%).")

    with rec_col:
        section("🧠 Recommendations")
        recs = []
        if conv_rate < 20 and status_col:
            recs.append(("HIGH","Implement lead scoring — rank prospects by intent signals to focus rep time on likely converters."))
        if source_col and status_col:
            perf = df.groupby(source_col).agg(
                leads=(source_col,"count"), won=(status_col, lambda x: is_won(x).sum()))
            perf["rate"] = perf["won"]/perf["leads"]
            best_ch = perf["rate"].idxmax(); worst_ch = perf["rate"].idxmin()
            recs.append(("HIGH",f"Scale {best_ch} — reallocate 30–40% of underperforming channel budget here."))
            recs.append(("MEDIUM",f"A/B test {worst_ch} messaging or pause it for 30 days and measure impact."))
        if cost and roi < 100:
            recs.append(("HIGH",f"ROI is {roi:.0f}% — below breakeven. Reduce CAC or increase avg deal size via upselling."))
        if avg_deal and rev_col:
            recs.append(("MEDIUM",f"Avg deal is {fmt_inr(avg_deal)}. Add a premium tier or annual billing to lift this 20–30%."))
        if date_col:
            recs.append(("LOW","Set up automated drip sequences for leads older than 14 days."))
        recs.append(("LOW","Build a referral programme. Referred leads convert 3–5× faster."))
        recs.append(("MEDIUM","Segment by company size — personalised outreach lifts response rates 40–60%."))

        for priority, text in recs:
            cls = priority.lower()
            st.markdown(f"""
<div class='rec-pill'>
  <span class='rec-badge {cls}'>{priority}</span>
  <span style='color:#94a3b8;font-size:13px;line-height:1.6'>{text}</span>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE — CHANNEL DEEP-DIVE
# ═══════════════════════════════════════════════════════
elif page == "🗺️  Channel Deep-Dive":
    st.markdown("""
<div class='pg-header'>
  <div class='pg-badge'>Analysis</div>
  <div class='pg-title'>Channel Deep-Dive</div>
</div>""", unsafe_allow_html=True)

    if not source_col:
        st.warning("No Source/Channel column detected in your dataset.")
        st.stop()

    channels = df[source_col].value_counts().index.tolist()
    selected = st.multiselect("Filter channels", channels, default=channels)
    dff = df[df[source_col].isin(selected)]

    neon_hr()
    top, bot = st.columns(2)

    with top:
        section("Lead Volume by Channel")
        vc = dff[source_col].value_counts().reset_index()
        vc.columns = ["Channel","Leads"]
        fig = px.bar(vc, x="Channel", y="Leads", text="Leads",
                     color="Channel", color_discrete_sequence=PALETTE)
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(**chart_layout(height=300, showlegend=False))
        st.plotly_chart(fig, use_container_width=True)

    with bot:
        if rev_col:
            section("Revenue by Channel")
            rv = dff.groupby(source_col)[rev_col].sum().reset_index()
            rv.columns = ["Channel","Revenue"]
            rv = rv.sort_values("Revenue", ascending=False)
            fig = px.bar(rv, x="Channel", y="Revenue",
                         text=rv["Revenue"].apply(fmt_inr),
                         color="Channel", color_discrete_sequence=PALETTE)
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(**chart_layout(height=300, showlegend=False))
            st.plotly_chart(fig, use_container_width=True)

    if status_col:
        neon_hr()
        section("Conversion Funnel by Channel")
        funnel = dff.groupby(source_col).agg(
            Leads=(source_col,"count"),
            Won=(status_col, lambda x: is_won(x).sum())
        ).reset_index()
        funnel["Lost"] = funnel["Leads"] - funnel["Won"]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Won", x=funnel[source_col], y=funnel["Won"],
                             marker_color="#00ffa3", marker_line_width=0,
                             text=funnel["Won"], textposition="inside"))
        fig.add_trace(go.Bar(name="Lost/Open", x=funnel[source_col], y=funnel["Lost"],
                             marker_color="#f87171", marker_line_width=0,
                             text=funnel["Lost"], textposition="inside"))
        # ✅ FIX: legend dict is merged by chart_layout() — no TypeError
        fig.update_layout(**chart_layout(
            barmode="stack", height=320,
            legend=dict(orientation="h", y=1.08)
        ))
        st.plotly_chart(fig, use_container_width=True)

    if rev_col and cost_col:
        neon_hr()
        section("ROI by Channel")
        roi_df = dff.groupby(source_col).agg(Rev=(rev_col,"sum"), Cost=(cost_col,"sum")).reset_index()
        roi_df["ROI"] = ((roi_df["Rev"]-roi_df["Cost"])/roi_df["Cost"].replace(0,np.nan)*100).round(1)
        roi_df = roi_df.dropna(subset=["ROI"]).sort_values("ROI", ascending=False)
        fig = px.bar(roi_df, x=source_col, y="ROI", text="ROI",
                     color="ROI", color_continuous_scale=["#f87171","#fbbf24","#00ffa3"])
        fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig.update_layout(**chart_layout(height=300, coloraxis_showscale=False))
        st.plotly_chart(fig, use_container_width=True)

    neon_hr()
    section("Channel Summary Table")
    summary = dff.groupby(source_col).agg(Leads=(source_col,"count")).reset_index()
    if status_col:
        won_vals = dff.groupby(source_col).apply(lambda x: is_won(x[status_col]).sum()).reset_index(drop=True)
        summary["Won"] = won_vals.values
        summary["Conv %"] = (summary["Won"]/summary["Leads"]*100).round(1)
    if rev_col:
        summary["Revenue"] = [fmt_inr(v) for v in dff.groupby(source_col)[rev_col].sum().values]
    if cost_col:
        summary["Cost"] = [fmt_inr(v) for v in dff.groupby(source_col)[cost_col].sum().values]
    st.dataframe(summary.sort_values("Leads",ascending=False), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
#  PAGE — PREDICTIONS
# ═══════════════════════════════════════════════════════
elif page == "📈  Predictions":
    st.markdown("""
<div class='pg-header'>
  <div class='pg-badge'>Forecasting</div>
  <div class='pg-title'>Predictions & Trend Analysis</div>
</div>""", unsafe_allow_html=True)

    if not date_col:
        st.warning("No Date column found. Add a date column to enable predictions.")
        st.stop()
    if not rev_col:
        st.warning("No Revenue column found. Forecasting requires a revenue column.")
        st.stop()

    tmp = df.dropna(subset=[date_col,rev_col]).copy()
    tmp["month"] = tmp[date_col].dt.to_period("M").astype(str)
    monthly = tmp.groupby("month")[rev_col].sum().reset_index()
    monthly.columns = ["Month","Revenue"]

    if len(monthly) < 2:
        st.warning("Need at least 2 months of data for predictions.")
        st.stop()

    future_rev = simple_forecast(monthly["Revenue"].tolist(), periods=3)
    last_dt = pd.Period(monthly["Month"].iloc[-1], freq="M")
    future_months = [(last_dt+i).strftime("%Y-%m") for i in range(1,4)]

    f1,f2,f3 = st.columns(3)
    for col_ui, month, val in zip([f1,f2,f3], future_months, future_rev):
        col_ui.markdown(f"""
<div class='pred-card'>
  <div class='pred-month'>{month}</div>
  <div class='pred-value'>{fmt_inr(val)}</div>
  <div class='pred-note'>Linear trend projection</div>
</div>""", unsafe_allow_html=True)

    neon_hr()
    section("Revenue Trend + 3-Month Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Revenue"], name="Actual",
        mode="lines+markers",
        line=dict(color="#00d4ff",width=2.5),
        marker=dict(color="#00d4ff",size=7,line=dict(color="#020817",width=2)),
        fill="tozeroy", fillcolor="rgba(0,212,255,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=future_months, y=future_rev, name="Forecast",
        mode="lines+markers",
        line=dict(color="#a855f7",width=2.5,dash="dot"),
        marker=dict(color="#a855f7",size=9,symbol="diamond",line=dict(color="#020817",width=2)),
        fill="tozeroy", fillcolor="rgba(168,85,247,0.06)",
    ))
    fig.update_layout(**chart_layout(height=340))
    st.plotly_chart(fig, use_container_width=True)

    if status_col:
        neon_hr()
        section("Monthly Lead Volume & Conversions")
        tmp2 = df.dropna(subset=[date_col]).copy()
        tmp2["month"] = tmp2[date_col].dt.to_period("M").astype(str)
        lead_trend = tmp2.groupby("month").agg(
            Leads=("month","count"),
            Won=(status_col, lambda x: is_won(x).sum())
        ).reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=lead_trend["month"], y=lead_trend["Leads"],
                              name="Total Leads", marker_color="rgba(0,212,255,0.3)",
                              marker_line_width=0))
        fig2.add_trace(go.Bar(x=lead_trend["month"], y=lead_trend["Won"],
                              name="Converted", marker_color="#00ffa3", marker_line_width=0))
        fig2.update_layout(**chart_layout(barmode="overlay", height=300))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
<div class='info-box' style='margin-top:8px'>
<p style='color:#334155;font-size:12px;margin:0'>
⚠️ <b style='color:#475569'>Forecast disclaimer:</b> Predictions use linear trend extrapolation. They do not account for seasonality, market shifts or pipeline events. Use as directional guide only.
</p>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE — RISKS
# ═══════════════════════════════════════════════════════
elif page == "⚠️  Risks":
    st.markdown("""
<div class='pg-header'>
  <div class='pg-badge'>Risk Intelligence</div>
  <div class='pg-title'>Risk Analysis</div>
</div>""", unsafe_allow_html=True)

    r1, r2 = st.columns(2)

    with r1:
        section("🚨 Identified Risks")

        if source_col:
            vc = df[source_col].value_counts(normalize=True)*100
            sh = vc.iloc[0]; src = vc.index[0]
            if sh > 60:
                risk_item("high", f"Channel concentration: {src} drives {sh:.0f}% of leads. Single-source dependency is fragile.")
            elif sh > 40:
                risk_item("medium", f"Moderate concentration: {src} is {sh:.0f}% of leads. Diversify to reduce exposure.")
            else:
                risk_item("low", f"Good diversification — top source ({src}) is only {sh:.0f}% of pipeline.")

        if status_col:
            if conv_rate < 10:
                risk_item("high", f"Critical conversion: {conv_rate:.1f}%. Revenue target will be missed without intervention.")
            elif conv_rate < 20:
                risk_item("medium", f"Below-benchmark conversion ({conv_rate:.1f}%). Industry avg is ~20–25%.")
            else:
                risk_item("low", f"Healthy conversion rate ({conv_rate:.1f}%). Monitor to stay above 20%.")

        if cost_col:
            if roi < 0:
                risk_item("high", f"Negative ROI ({roi:.1f}%). Spending more than earning — immediate action required.")
            elif roi < 50:
                risk_item("medium", f"Low ROI ({roi:.1f}%). Marginally profitable. Review cost allocation per channel.")
            else:
                risk_item("low", f"Positive ROI ({roi:.1f}%). Profitable — maintain cost discipline.")

        if source_col and rev_col:
            rv = df.groupby(source_col)[rev_col].sum()
            sh2 = rv.max()/rv.sum()*100 if rv.sum()>0 else 0
            if sh2 > 70:
                risk_item("high", f"Revenue concentration: {sh2:.0f}% from one channel. Losing it could be catastrophic.")
            elif sh2 > 50:
                risk_item("medium", f"Revenue dependency: {sh2:.0f}% from top channel. Diversify revenue sources.")

        if date_col:
            latest = df[date_col].dropna().max()
            days_old = (pd.Timestamp.now() - latest).days
            if days_old > 60:
                risk_item("medium", f"Data freshness: most recent entry is {latest.strftime('%b %d, %Y')}. Pipeline may be stale.")
            else:
                risk_item("low", "Data is recent and likely reflects current pipeline.")

        risk_item("medium" if total<50 else "low",
            f"Sample size: {total} leads — {'may not be statistically reliable' if total<50 else 'sufficient for reliable analysis'}.")

    with r2:
        section("📊 Risk Heatmap")

        risk_areas  = ["Channel Concentration","Conversion Rate","ROI / Profitability",
                       "Revenue Concentration","Data Freshness","Sample Size"]
        risk_levels = [1,1,1,1,1,1]

        if source_col:
            vc = df[source_col].value_counts(normalize=True)*100
            risk_levels[0] = 3 if vc.iloc[0]>60 else (2 if vc.iloc[0]>40 else 1)
        if status_col:
            risk_levels[1] = 3 if conv_rate<10 else (2 if conv_rate<20 else 1)
        if cost_col:
            risk_levels[2] = 3 if roi<0 else (2 if roi<50 else 1)
        if source_col and rev_col:
            rv = df.groupby(source_col)[rev_col].sum()
            sh3 = rv.max()/rv.sum()*100 if rv.sum()>0 else 0
            risk_levels[3] = 3 if sh3>70 else (2 if sh3>50 else 1)
        if date_col:
            days2 = (pd.Timestamp.now()-df[date_col].dropna().max()).days
            risk_levels[4] = 2 if days2>60 else 1
        risk_levels[5] = 2 if total<50 else 1

        colors = {1:"#00ffa3",2:"#fbbf24",3:"#f87171"}
        labels = {1:"LOW",2:"MEDIUM",3:"HIGH"}

        fig = go.Figure(go.Bar(
            x=risk_levels, y=risk_areas, orientation="h",
            marker=dict(color=[colors[l] for l in risk_levels], line=dict(width=0)),
            text=[labels[l] for l in risk_levels],
            textposition="inside",
            textfont=dict(color="#020817",size=11,family="Space Grotesk"),
        ))
        # ✅ FIX: xaxis dict is merged by chart_layout() — no TypeError
        fig.update_layout(**chart_layout(
            height=380,
            xaxis=dict(showgrid=False, showticklabels=False, range=[0,3.5])
        ))
        st.plotly_chart(fig, use_container_width=True)

        avg_risk = sum(risk_levels)/len(risk_levels)
        overall  = "HIGH" if avg_risk>2.2 else ("MEDIUM" if avg_risk>1.4 else "LOW")
        oc = {"HIGH":"#f87171","MEDIUM":"#fbbf24","LOW":"#00ffa3"}[overall]

        st.markdown(f"""
<div style='text-align:center;padding:22px;
     background:rgba(255,255,255,0.025);backdrop-filter:blur(16px);
     border:1px solid rgba(255,255,255,0.07);border-radius:16px;margin-top:10px'>
  <div style='font-size:11px;color:#334155;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px'>Overall Risk Score</div>
  <div style='font-size:44px;font-weight:700;color:{oc};font-family:Space Mono;
       text-shadow:0 0 20px {oc};letter-spacing:-1px'>{overall}</div>
  <div style='font-size:12px;color:#334155;margin-top:6px'>{avg_risk:.1f} / 3.0</div>
</div>""", unsafe_allow_html=True)
