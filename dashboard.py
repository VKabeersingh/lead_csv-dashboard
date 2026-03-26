import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Team 1 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🚀 Team 1 Lead Dashboard")

uploaded = st.file_uploader("📁 Upload CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    required_cols = ["Source", "Status", "Region", "Industry", "Date", "Revenue", "Ad_Spend", "Follow_up_Days"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"CSV must have columns: {', '.join(required_cols)}")
        st.stop()

    st.success(f"✅ {len(df)} leads!")

    st.sidebar.header("Filters")
    source_f = st.sidebar.multiselect("Source", sorted(df["Source"].dropna().unique()))
    status_f = st.sidebar.multiselect("Status", sorted(df["Status"].dropna().unique()))
    region_f = st.sidebar.multiselect("Region", sorted(df["Region"].dropna().unique()))
    industry_f = st.sidebar.multiselect("Industry", sorted(df["Industry"].dropna().unique()))

    all_true = pd.Series(True, index=df.index)
    mask_source = df["Source"].isin(source_f) if source_f else all_true
    mask_status = df["Status"].isin(status_f) if status_f else all_true
    mask_region = df["Region"].isin(region_f) if region_f else all_true
    mask_industry = df["Industry"].isin(industry_f) if industry_f else all_true
    filtered = df[mask_source & mask_status & mask_region & mask_industry]

    total = len(filtered)
    converted = len(filtered[filtered["Status"] == "Converted"])
    revenue = filtered["Revenue"].sum() if total else 0
    spend = filtered["Ad_Spend"].sum() if total else 0
    days = filtered["Follow_up_Days"].mean() if total else 0
    conv_rate = f"{converted / total * 100:.1f}%" if total else "0%"

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("📊 Total", total)
    c2.metric("✅ Converted", converted)
    c3.metric("💰 Revenue", f"${revenue:,.0f}")
    c4.metric("💸 Spend", f"${spend:,.0f}")
    c5.metric("📈 Conv%", conv_rate)
    c6.metric("⏱️ Days", f"{days:.1f}")

    r1, r2, r3 = st.columns(3)
    source_counts = (
        filtered["Source"]
        .value_counts()
        .reset_index(name="count")
        .rename(columns={"index": "Source"})
    )
    r1.plotly_chart(px.bar(source_counts, x="Source", y="count", title="Sources"))
    r2.plotly_chart(px.pie(filtered, names="Status", title="Status"))
    r3.plotly_chart(px.bar(filtered.groupby("Region")["Revenue"].sum().reset_index(), x="Region", y="Revenue", title="Revenue by Region"))

    st.plotly_chart(px.line(filtered.sort_values("Date"), x="Date", y="Revenue", title="Revenue Over Time"))
    st.download_button("💾 Export", filtered.to_csv(index=False), "leads.csv", mime="text/csv")
    st.dataframe(filtered)
else:
    st.info("Upload a CSV to view dashboard and apply sidebar filters.")
