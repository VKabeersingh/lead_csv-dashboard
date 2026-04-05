import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE =================
st.set_page_config(page_title="Lead Intelligence Pro+", layout="wide")

# ================= MODERN UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e2e8f0;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
}

.big-text {
    font-size: 28px;
    font-weight: bold;
}

.small-text {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD =================
@st.cache_data
def load(file):
    df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)

    cols = {c.lower(): c for c in df.columns}

    def find(keyword_list):
        for k in keyword_list:
            for col in cols:
                if k in col:
                    return cols[col]
        return None

    status = find(["status"])
    source = find(["source", "channel"])
    revenue = find(["rev", "amount", "price"])
    date = find(["date"])
    cost = find(["cost", "spend"])

    if date:
        df[date] = pd.to_datetime(df[date], errors="coerce")

    return df, status, source, revenue, date, cost


# ================= APP =================
st.title("🚀 Lead Intelligence Pro+")

file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"])

if file:
    df, status_col, source_col, rev_col, date_col, cost_col = load(file)

    # Clean status
    if status_col:
        df[status_col] = df[status_col].astype(str).str.lower().str.strip()

    # ================= SIDEBAR =================
    with st.sidebar:
        st.header("⚙️ Controls")

        chart_type = st.selectbox("Chart Type", ["Bar", "Pie", "Line"])

        if source_col:
            selected_sources = st.multiselect(
                "Source",
                df[source_col].dropna().unique(),
                default=df[source_col].dropna().unique()
            )
            df = df[df[source_col].isin(selected_sources)]

    # ================= KPIs =================
    total = len(df)

    converted = 0
    if status_col:
        converted = df[status_col].isin(["won", "converted", "closed"]).sum()

    revenue = df[rev_col].sum() if rev_col else 0
    cost = df[cost_col].sum() if cost_col else 0

    conv_rate = (converted / total * 100) if total else 0
    roi = ((revenue - cost) / cost * 100) if cost > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='card'><div class='big-text'>{total}</div><div class='small-text'>Leads</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><div class='big-text'>{conv_rate:.1f}%</div><div class='small-text'>Conversion</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><div class='big-text'>₹{revenue:,.0f}</div><div class='small-text'>Revenue</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card'><div class='big-text'>{roi:.1f}%</div><div class='small-text'>ROI</div></div>", unsafe_allow_html=True)

    st.divider()

    # ================= CHART =================
    if source_col:
        data = df[source_col].value_counts().reset_index()
        data.columns = [source_col, "Leads"]

        if chart_type == "Pie":
            fig = px.pie(data, names=source_col, values="Leads", hole=0.4)
        elif chart_type == "Line":
            fig = px.line(data, x=source_col, y="Leads", markers=True)
        else:
            fig = px.bar(data, x=source_col, y="Leads")

        st.plotly_chart(fig, use_container_width=True)

    # ================= INSIGHTS =================
    st.subheader("🧠 Smart Insights")

    if source_col and status_col:
        perf = df.groupby(source_col).agg(
            leads=(source_col, "count"),
            conversions=(status_col, lambda x: x.isin(["won", "converted", "closed"]).sum())
        ).reset_index()

        perf["conv_rate"] = perf["conversions"] / perf["leads"]

        best = perf.sort_values("conv_rate", ascending=False).iloc[0]
        worst = perf.sort_values("conv_rate").iloc[0]

        st.success(f"🔥 Best Source: {best[source_col]} ({best['conv_rate']*100:.1f}%)")
        st.error(f"❌ Worst Source: {worst[source_col]} ({worst['conv_rate']*100:.1f}%)")

        # Smart suggestion
        if best["conv_rate"] > 0.3:
            st.info("👉 Scale this source — high conversion detected")

        if worst["conv_rate"] < 0.1:
            st.warning("👉 Optimize or cut this source")

    # ROI insight
    if roi < 0:
        st.error("🚨 Negative ROI — you're losing money")
    elif roi > 50:
        st.success("💰 Strong ROI — scalable campaign")

    # ================= GOAL =================
    st.subheader("🎯 Goal Tracker")

    target = st.number_input("Set Revenue Target", value=50000)

    progress = (revenue / target) * 100 if target else 0
    progress = min(progress, 100)

    st.progress(int(progress))
    st.write(f"{progress:.1f}% achieved")

    # ================= TOP SOURCE =================
    if source_col and rev_col:
        top = df.groupby(source_col)[rev_col].sum().idxmax()
        st.info(f"🏆 Top Revenue Source: {top}")

    # ================= DATA =================
    with st.expander("📂 View Data"):
        st.dataframe(df)
