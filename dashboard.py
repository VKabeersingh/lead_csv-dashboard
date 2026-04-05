import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import copy
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  SIDEBAR STATE (FIX)
# ─────────────────────────────────────────────
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

def toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open

# ─────────────────────────────────────────────
#  PAGE CONFIG (ONLY ONCE — FIXED)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LeadLens · Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.sidebar_open else "collapsed",
)

# ─────────────────────────────────────────────
#  FLOATING TOGGLE BUTTON (PRO UI)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.toggle-btn {
    position: fixed;
    top: 16px;
    left: 16px;
    z-index: 999;
}
.toggle-btn button {
    background: rgba(0,212,255,0.1) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    color: #00d4ff !important;
    border-radius: 10px !important;
    padding: 6px 12px !important;
    font-size: 18px !important;
    backdrop-filter: blur(10px);
}
.toggle-btn button:hover {
    background: rgba(0,212,255,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# Button container
st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
st.button("☰", on_click=toggle_sidebar)
st.markdown('</div>', unsafe_allow_html=True)
