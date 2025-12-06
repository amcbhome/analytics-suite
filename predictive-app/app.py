"""
GenAI Accounting Analytics Toolkit — Predictive Analytics Dashboard
Live Efficient Frontier powered by editable return data.

This dashboard recalculates:
- Expected return
- Standard deviation
- Correlation
- Portfolio risk across weightings
and updates the chart instantly.

Author: Alastair McBride & GenAI Assistant
"""

# ──────────────────────────────────────────────────────────────
# PATH FIX FOR SHARED MODULES
# ──────────────────────────────────────────────────────────────
from __future__ import annotations
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ──────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from shared.theme import set_page_config, academic_header, ACCENT_COLOR

# ──────────────────────────────────────────────────────────────
# Page Setup
# ──────────────────────────────────────────────────────────────
set_page_config()

academic_header(
    "📈 Predictive Analytics — Diversification Dashboard",
    "Live efficient frontier from editable annual return data (Watson & Head, 2023)."
)

st.caption(
    "GenAI Accounting Analytics Toolkit · Predictive module · Live dashboard"
)

# ──────────────────────────────────────────────────────────────
# Sidebar Notes
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About this Dashboard")
    st.markdown(
        """
        This dashboard demonstrates **Modern Portfolio Theory**:

        ✔ Mean return  
        ✔ Volatility (σ)  
        ✔ Correlation (ρ)  
        ✔ Portfolio risk (σₚ)  

        Edit the data table — the efficient frontier updates automatically.
        """
    )
    st.markdown("---")
    st.markdown("**Reference**")
    st.markdown(
        """
        Watson, D. & Head, A. (2023).  
        *Corporate Finance* (8th Ed.).
        """
    )

# ──────────────────────────────────────────────────────────────
# STEP 1 — Editable Input Table
# ──────────────────────────────────────────────────────────────
st.subheader("📌 Step 1 — Input/Modify Annual Returns (%)")

default_df = pd.DataFrame({
    "S": [6.6, 5.6, -9.0, 12.6, 14.0],
    "T": [24.5, -5.9, 19.9, -7.8, 14.8],
})

df = st.data_editor(default_df, use_container_width=True)
df_dec = df.astype(float) / 100.0  # convert % → decimals

# ──────────────────────────────────────────────────────────────
# COMPUTATIONS — Auto recalculation with every change
# ──────────────────────────────────────────────────────────────
def compute(df):
    mean_s = df["S"].mean()
    mean_t = df["T"].mean()
    sd_s = df["S"].std(ddof=0)
    sd_t = df["T"].std(ddof=0)
    corr = df["S"].corr(df["T"])
    return mean_s, mean_t, sd_s, sd_t, corr

mean_s, mean_t, sd_s, sd_t, corr = compute(df_dec)

# Portfolio weights for discrete view
weights = [(1,0),(0.8,0.2),(0.6,0.4),(0.4,0.6),(0.2,0.8),(0,1)]
labels = ["100% S","80/20","60/40","40/60","20/80","100% T"]

def port_calc(w_s, w_t):
    ret = w_s*mean_s + w_t*mean_t
    var = (w_s**2 * sd_s**2
           + w_t**2 * sd_t**2
           + 2*w_s*w_t*sd_s*sd_t*corr)
    return ret, np.sqrt(var)

rows, sd_vals = [], []
for (w_s, w_t), label in zip(weights, labels):
    r, s = port_calc(w_s, w_t)
    rows.append([label, r*100, s*100])
    sd_vals.append(s)

table_df = pd.DataFrame(rows, columns=["Portfolio","Mean return (%)","Std dev (%)"])

# ──────────────────────────────────────────────────────────────
# STEP 2 & 3 — Table + Slider Side-by-side
# ──────────────────────────────────────────────────────────────
left, right = st.columns([1.1, 1.3])

with left:
    st.subheader("📋 Step 2 — Portfolio Table")
    st.dataframe(table_df, use_container_width=True)

with right:
    st.subheader("🎚 Step 3 — Explore Portfolio Weights")

    weight_slider = st.slider(
        "Weight allocated to Asset S (remaining goes to T)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        format="%.2f"
    )

    w_s = weight_slider
    w_t = 1 - weight_slider

    sel_ret, sel_sd = port_calc(w_s, w_t)

    st.info(
        f"""
        **Selected Portfolio Mix:**  
        - S Weight: **{w_s:.2f}**
        - T Weight: **{w_t:.2f}**

        **Expected Return:** {sel_ret*100:.2f}%  
        **Risk (Std Dev):** {sel_sd*100:.2f}%
        """
    )

# ──────────────────────────────────────────────────────────────
# STEP 4 — Chart with Slider Pointer
# ──────────────────────────────────────────────────────────────
st.subheader("📈 Step 4 — Efficient Frontier")

x = table_df["Std dev (%)"]
y = table_df["Mean return (%)"]

fig, ax = plt.subplots(figsize=(6, 5))

# Plot discrete frontier points
ax.plot(x, y, marker="o", linestyle="-", color=ACCENT_COLOR, label="Frontier Points")

# Plot slider-selected point
ax.scatter(sel_sd*100, sel_ret*100, color="red", s=120, zorder=5, label="Your Selection")

ax.set_xlabel("Risk (σ, %)")
ax.set_ylabel("Expected Return (%)")
ax.grid(True, linestyle="--", linewidth=0.5)
ax.legend()
st.pyplot(fig)

# ──────────────────────────────────────────────────────────────
# STEP 5 — Diversification Insight
# ──────────────────────────────────────────────────────────────
st.subheader("💡 Step 5 — Diversification Insight")
min_risk = min(sd_vals) * 100

st.success(
    f"📉 Minimum observed portfolio risk: **{min_risk:.2f}%** "
    f"(vs S = {sd_s*100:.2f}%, T = {sd_t*100:.2f}%)"
)

# ──────────────────────────────────────────────────────────────
# FORMULAS + REFERENCES
# ──────────────────────────────────────────────────────────────
with st.expander("📎 Methodology & Notes (Formulas + References)"):
    st.markdown(
        r"""
        ### Two-Asset Portfolio (Watson & Head, 2023)
        \[
        E(R_P) = w_S\mu_S + w_T\mu_T
        \]
        \[
        \sigma_P = \sqrt{
        w_S^2\sigma_S^2 + w_T^2\sigma_T^2 + 2w_Sw_T\sigma_S\sigma_T\rho_{S,T}}
        \]
        **Reference:** Watson, D. & Head, A. (2023). *Corporate Finance (8th Ed.)*.
        """
    )
