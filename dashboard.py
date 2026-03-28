import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE =================
st.set_page_config(page_title="Lead Intelligence Pro", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.main {background: #0b1220;}
h1, h2, h3 {color: white;}
</style>
""", unsafe_allow_html=True)

# ================= LOAD FUNCTION =================
@st.cache_data
def load(file):
    df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)

    status = next((c for c in df.columns if "status" in c.lower()), None)
    source = next((c for c in df.columns if "source" in c.lower()), None)
    revenue = next((c for c in df.columns if "rev" in c.lower() or "amount" in c.lower()), None)
    date = next((c for c in df.columns if "date" in c.lower()), None)
    cost = next((c for c in df.columns if "cost" in c.lower() or "spend" in c.lower()), None)

    if date:
        df[date] = pd.to_datetime(df[date], errors='coerce')

    return df, status, source, revenue, date, cost

# ================= APP =================
st.title("🚀 Lead Intelligence Pro Dashboard")

file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"])

if file:
    df, status_col, source_col, rev_col, date_col, cost_col = load(file)

    # ================= KPIs =================
    total = len(df)

    if status_col:
        converted_df = df[df[status_col].astype(str).str.lower() == "won"]
        converted = len(converted_df)
    else:
        converted = 0

    revenue = df[rev_col].sum() if rev_col else 0
    cost = df[cost_col].sum() if cost_col else 0

    conv_rate = (converted / total * 100) if total else 0
    cpl = (cost / total) if cost else 0
    cpa = (cost / converted) if converted else 0
    roi = ((revenue - cost) / cost * 100) if cost else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Leads", total)
    c2.metric("Conversion %", f"{conv_rate:.1f}%")
    c3.metric("Revenue", f"${revenue:,.0f}")
    c4.metric("CPL", f"${cpl:.2f}")
    c5.metric("ROI", f"{roi:.1f}%")

    st.divider()

    # ================= CHART SELECTOR =================
    chart_type = st.selectbox(
        "📊 Select Chart Type",
        ["Pie", "Bar", "Line"]
    )

    # ================= CHARTS =================
    col1, col2, col3 = st.columns(3)

    # 🥧 Leads by Source
    if source_col:
        with col1:
            st.subheader("Leads by Source")
            lead_dist = df[source_col].value_counts().reset_index()
            lead_dist.columns = [source_col, "Leads"]

            if chart_type == "Pie":
                fig = px.pie(lead_dist, names=source_col, values="Leads", hole=0.4, template="plotly_dark")
            elif chart_type == "Bar":
                fig = px.bar(lead_dist, x=source_col, y="Leads", template="plotly_dark")
            else:
                fig = px.line(lead_dist, x=source_col, y="Leads", markers=True, template="plotly_dark")

            st.plotly_chart(fig, use_container_width=True)

    # 💰 Revenue Share
    if source_col and rev_col:
        with col2:
            st.subheader("Revenue Share")
            rev_data = df.groupby(source_col)[rev_col].sum().reset_index()

            if chart_type == "Pie":
                fig = px.pie(rev_data, names=source_col, values=rev_col, hole=0.4, template="plotly_dark")
            elif chart_type == "Bar":
                fig = px.bar(rev_data, x=source_col, y=rev_col, template="plotly_dark")
            else:
                fig = px.line(rev_data, x=source_col, y=rev_col, markers=True, template="plotly_dark")

            st.plotly_chart(fig, use_container_width=True)

    # 🎯 Status Distribution
    if status_col:
        with col3:
            st.subheader("Lead Status")
            status_data = df[status_col].value_counts().reset_index()
            status_data.columns = ["Status", "Count"]

            if chart_type == "Pie":
                fig = px.pie(status_data, names="Status", values="Count", hole=0.4, template="plotly_dark")
            elif chart_type == "Bar":
                fig = px.bar(status_data, x="Status", y="Count", template="plotly_dark")
            else:
                fig = px.line(status_data, x="Status", y="Count", markers=True, template="plotly_dark")

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ================= FUNNEL =================
    if status_col:
        st.subheader("🎯 Funnel Analysis")

        funnel = df[status_col].value_counts().reset_index()
        funnel.columns = ["Stage", "Count"]

        funnel["Drop %"] = funnel["Count"].pct_change().fillna(0) * -100

        st.dataframe(funnel)

        fig = px.funnel(funnel, x="Count", y="Stage", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        if len(funnel) > 1:
            biggest_drop = funnel.iloc[funnel["Drop %"].idxmax()]
            st.error(f"🚨 Biggest drop at {biggest_drop['Stage']} ({biggest_drop['Drop %']:.1f}%)")

    # ================= TREND =================
    if date_col:
        st.subheader("📈 Lead Trend")

        trend = df.groupby(df[date_col].dt.date).size().reset_index(name="Leads")
        trend["7D Avg"] = trend["Leads"].rolling(7).mean()

        fig = px.line(trend, x=date_col, y="Leads", template="plotly_dark")
        fig.add_scatter(x=trend[date_col], y=trend["7D Avg"], mode='lines', name="7D Avg")

        st.plotly_chart(fig, use_container_width=True)

    # ================= INSIGHTS =================
    st.subheader("🧠 Business Insights")

    insights = []

    if source_col and status_col:
        perf = df.groupby(source_col).agg(
            leads=(source_col, "count"),
            conversions=(status_col, lambda x: x.astype(str).str.lower().eq("won").sum())
        ).reset_index()

        perf["conv_rate"] = perf["conversions"] / perf["leads"]

        best = perf.sort_values("conv_rate", ascending=False).iloc[0]
        worst = perf.sort_values("conv_rate").iloc[0]

        insights.append(f"🔥 Best channel: {best[source_col]} ({best['conv_rate']*100:.1f}%)")
        insights.append(f"❌ Worst channel: {worst[source_col]}")

    if roi:
        if roi < 0:
            insights.append("🚨 Campaign is losing money")
        elif roi > 100:
            insights.append("💰 High ROI — scale aggressively")

    if cpl > 50:
        insights.append("⚠️ High cost per lead — optimize ads")

    for i in insights:
        st.success(i)

    # ================= ACTIONS =================
    st.subheader("📌 Recommended Actions")

    actions = []

    if roi < 50:
        actions.append("Reduce spend on low ROI channels")
    if conv_rate < 20:
        actions.append("Improve conversion funnel")
    if source_col and status_col:
        actions.append(f"Scale {best[source_col]} channel")

    for a in actions:
        st.info(a)

    # ================= DATA =================
    with st.expander("📂 Raw Data"):
        st.dataframe(df)
