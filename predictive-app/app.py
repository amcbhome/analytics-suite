"""
GenAI Accounting Analytics Toolkit — Predictive Analytics Dashboard (Altair)
Interactive efficient frontier with editable returns, weight slider,
and hover detail panel.

Author: Alastair McBride & GenAI Assistant
"""

from __future__ import annotations
import sys, os

# Ensure we can import shared utilities (for Streamlit Cloud)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

from shared.theme import set_page_config, academic_header, ACCENT_COLOR

# ──────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────
def compute_stats(df_dec: pd.DataFrame):
    """Return mean, sd and correlation for S and T given decimal returns."""
    mean_s = df_dec["S"].mean()
    mean_t = df_dec["T"].mean()
    sd_s = df_dec["S"].std(ddof=0)
    sd_t = df_dec["T"].std(ddof=0)
    corr = df_dec["S"].corr(df_dec["T"])
    return mean_s, mean_t, sd_s, sd_t, corr


def portfolio_point(mean_s, mean_t, sd_s, sd_t, corr, w_s: float):
    """Return (return_pct, risk_pct) for given weight in S (decimal)."""
    w_t = 1.0 - w_s
    ret = w_s * mean_s + w_t * mean_t
    var = (
        w_s**2 * sd_s**2
        + w_t**2 * sd_t**2
        + 2 * w_s * w_t * sd_s * sd_t * corr
    )
    sd = float(np.sqrt(var))
    return ret * 100.0, sd * 100.0


# ──────────────────────────────────────────────────────────────
# Page layout
# ──────────────────────────────────────────────────────────────
set_page_config()

academic_header(
    "📈 Predictive Analytics — Diversification Dashboard",
    "Altair-based efficient frontier with editable returns and weight slider "
    "(Watson & Head, 2023).",
)

st.caption(
    "GenAI Accounting Analytics Toolkit · Predictive module · "
    "Interactive academic dashboard"
)

# ──────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About this dashboard")
    st.markdown(
        """
        This dashboard illustrates **Modern Portfolio Theory** for two assets:

        - Edit 5 years of annual returns for S and T  
        - Move the **weight slider** for S (T = 1 − S)  
        - Hover over the curve to inspect risk/return combinations  

        The underlying example follows **Watson & Head (2023), Corporate Finance
        (8th ed.)**, in the chapter on risk and return.
        """
    )
    st.markdown("---")
    st.markdown("**Reference**")
    st.markdown(
        """
        Watson, D. & Head, A. (2023).  
        *Corporate Finance* (8th Ed.). Pearson.
        """
    )

# ──────────────────────────────────────────────────────────────
# Step 1 – Editable Input Table
# ──────────────────────────────────────────────────────────────
st.subheader("📌 Step 1 — Input / modify annual returns (%)")

default_df = pd.DataFrame(
    {
        "S": [6.6, 5.6, -9.0, 12.6, 14.0],
        "T": [24.5, -5.9, 19.9, -7.8, 14.8],
    }
)

df = st.data_editor(default_df, use_container_width=True)
df_dec = df.astype(float) / 100.0  # % → decimal

# Compute statistics
mean_s, mean_t, sd_s, sd_t, corr = compute_stats(df_dec)

# ──────────────────────────────────────────────────────────────
# Step 2 – Discrete Portfolios (teaching table)
# ──────────────────────────────────────────────────────────────
weights_discrete = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
labels_discrete = ["100% S", "80/20", "60/40", "40/60", "20/80", "100% T"]

rows = []
for w_s, label in zip(weights_discrete, labels_discrete):
    ret_pct, sd_pct = portfolio_point(mean_s, mean_t, sd_s, sd_t, corr, w_s)
    rows.append([label, w_s, 1.0 - w_s, ret_pct, sd_pct])

table_df = pd.DataFrame(
    rows,
    columns=["Portfolio", "w_S", "w_T", "Mean return (%)", "Std dev (%)"],
)

left, right = st.columns([1.1, 1.3])

with left:
    st.subheader("📋 Step 2 — Discrete portfolios (teaching set)")
    st.dataframe(table_df, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Step 3 – Slider to Select Weight of S
# ──────────────────────────────────────────────────────────────
with right:
    st.subheader("🎚 Step 3 — Set S/T mix")

    w_s_slider = st.slider(
        "Weight allocated to Asset S (T = 1 − S)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        format="%.2f",
    )
    w_t_slider = 1.0 - w_s_slider
    sel_ret, sel_sd = portfolio_point(
        mean_s, mean_t, sd_s, sd_t, corr, w_s_slider
    )

    st.info(
        f"""
        **Slider-selected mix**  
        - S weight: **{w_s_slider:.2f}**  
        - T weight: **{w_t_slider:.2f}**  

        **Expected return:** {sel_ret:.2f}%  
        **Risk (std dev):** {sel_sd:.2f}%
        """
    )

# ──────────────────────────────────────────────────────────────
# Step 4 – Continuous Frontier Data (for Altair curve)
# ──────────────────────────────────────────────────────────────
fine_weights = np.linspace(0.0, 1.0, 201)
frontier_rows = []
for w in fine_weights:
    ret_pct, sd_pct = portfolio_point(mean_s, mean_t, sd_s, sd_t, corr, w)
    frontier_rows.append(
        {
            "w_S": float(w),
            "w_T": float(1.0 - w),
            "Mean return (%)": ret_pct,
            "Std dev (%)": sd_pct,
        }
    )

frontier_df = pd.DataFrame(frontier_rows)

# Text label for hover panel
frontier_df["hover_label"] = (
    "σ = "
    + frontier_df["Std dev (%)"].round(2).astype(str)
    + "%,  R = "
    + frontier_df["Mean return (%)"].round(2).astype(str)
    + "%,  w_S = "
    + frontier_df["w_S"].round(2).astype(str)
)

# One-row dataframe for slider point
selected_df = pd.DataFrame(
    {
        "w_S": [w_s_slider],
        "w_T": [w_t_slider],
        "Mean return (%)": [sel_ret],
        "Std dev (%)": [sel_sd],
    }
)

# ──────────────────────────────────────────────────────────────
# Altair Chart — Smooth Curve + Slider Point + Hover Panel
# ──────────────────────────────────────────────────────────────
st.subheader("📈 Step 4 — Efficient frontier (Altair)")

# Hover selection
hover = alt.selection_point(
    fields=["w_S"],
    nearest=True,
    on="mouseover",
    empty="none",
)

base = alt.Chart(frontier_df).properties(width=420, height=320)

# Smooth frontier line
line = base.mark_line(color=ACCENT_COLOR, strokeWidth=2).encode(
    x=alt.X("Std dev (%):Q", title="Risk (σ, %)"),
    y=alt.Y("Mean return (%):Q", title="Expected return (%)"),
)

# Hoverable small points
points = base.mark_point(size=20, color=ACCENT_COLOR).encode(
    x="Std dev (%):Q",
    y="Mean return (%):Q",
).add_params(hover)

# Highlight hovered point
hover_points = points.transform_filter(hover).encode(size=alt.value(60))

# Slider-selected point (red)
sel_point = (
    alt.Chart(selected_df)
    .mark_point(color="red", size=140)
    .encode(x="Std dev (%):Q", y="Mean return (%):Q")
)

curve_chart = (line + points + hover_points + sel_point).properties(
    title="Efficient frontier (two-asset mix)"
)

# Floating-style hover detail box
hover_panel = (
    alt.Chart(frontier_df)
    .mark_text(align="left", baseline="top")
    .encode(text="hover_label:N")
    .transform_filter(hover)
    .properties(width=240, height=80)
)

hover_background = alt.Chart(pd.DataFrame({"x": [0]})).mark_rect(
    fill="#FFFFFF", stroke="#CCCCCC", cornerRadius=8
).encode().properties(width=260, height=100)

# ❗ FIX: Use alt.layer, NOT "+"
info_panel = alt.layer(
    hover_background,
    hover_panel
).properties(title="Hover details")

# Final layout (side-by-side chart + hover panel)
full_chart = alt.hconcat(curve_chart, info_panel).resolve_scale(y="shared")

st.altair_chart(full_chart, use_container_width=False)

# ──────────────────────────────────────────────────────────────
# Step 5 — Diversification Insight
# ──────────────────────────────────────────────────────────────
st.subheader("💡 Step 5 — Diversification insight")

min_risk = frontier_df["Std dev (%)"].min()
st.success(
    f"📉 Minimum observed portfolio risk on this frontier: "
    f"**{min_risk:.2f}%** (compare with individual asset risks "
    f"S = {sd_s*100:.2f}%, T = {sd_t*100:.2f}%)."
)

# ──────────────────────────────────────────────────────────────
# Methodology & Notes
# ──────────────────────────────────────────────────────────────
with st.expander("📎 Methodology & Notes (formulas + references)"):
    st.markdown(
        r"""
        ### Two-asset portfolio

        Let \( R_S \) and \( R_T \) be the returns on assets S and T.

        - Expected return:
          \[
          E(R_P) = w_S \mu_S + w_T \mu_T
          \]

        - Portfolio variance:
          \[
          \sigma_P^2 =
            w_S^2 \sigma_S^2 +
            w_T^2 \sigma_T^2 +
            2 w_S w_T \sigma_S \sigma_T \rho_{S,T}
          \]

        - Portfolio standard deviation:
          \[
          \sigma_P = \sqrt{\sigma_P^2}
          \]

        Here, the frontier is generated for weights \( w_S \in [0, 1] \),
        with \( w_T = 1 - w_S \).

        ### Reference

        Watson, D. & Head, A. (2023). *Corporate Finance* (8th ed.). Pearson.
        """
    )

