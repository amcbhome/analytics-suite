"""
GenAI Accounting Analytics Toolkit — Predictive Analytics Module
File: predictive-app/app.py

Author(s): Alastair McBride & GenAI Assistant

Purpose:
    Demonstrates Modern Portfolio Theory (MPT) with two risky assets
    using annual return data (default from Watson & Head, 2023,
    Corporate Finance, 8th Edition).

    The app:
        - Accepts 5 years of returns for assets S and T
        - Computes mean returns, standard deviations, and correlation
        - Evaluates a set of portfolio weightings
        - Calculates portfolio variance and standard deviation
        - Plots a simple efficient frontier diagram
        - Provides a "Methodology & Notes" section suitable for
          academic or professional documentation.

Prompt provenance (human instruction, summarised):
    The human user requested three Streamlit projects (descriptive,
    predictive, prescriptive) with a unified, branded look, and asked
    that documentation include the prompts that generated the code.
    The original predictive example code was supplied by the user and
    refactored  into this academic-themed module.

    Full prompt text is recorded separately in docs/prompt_record.md.
"""

# ──────────────────────────────────────────────────────────────
# FIX FOR STREAMLIT CLOUD PATHS
# ──────────────────────────────────────────────────────────────
from __future__ import annotations
import sys, os

# Add repo root to Python module path to locate "shared"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ──────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from shared.theme import set_page_config, academic_header, ACCENT_COLOR

# ──────────────────────────────────────────────────────────────
# Page & layout setup
# ──────────────────────────────────────────────────────────────
set_page_config()

academic_header(
    title="📈 Predictive Analytics — Diversification of Risk",
    subtitle="Modern Portfolio Theory example using assets S and T "
             "(Watson & Head, 2023)."
)

st.caption(
    "GenAI Accounting Analytics Toolkit · Predictive Module · "
    "This app is for educational illustration only and does not "
    "constitute investment advice."
)

# ──────────────────────────────────────────────────────────────
# Sidebar – context and options
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About this Module")
    st.markdown(
        """
        This example uses **historic annual returns** to estimate:

        - Mean (expected) return  
        - Volatility (standard deviation)  
        - Correlation  
        - Portfolio risk under different weightings  

        Follows the approach used in **Watson & Head (2023),
        Corporate Finance**, in the chapter on Risk and Return.
        """
    )
    st.markdown("---")
    st.markdown("**Input Mode**")
    data_choice = st.radio(
        "Choose data source:",
        ["Use Watson & Head test data", "Enter my own 5-year returns"],
        index=0,
    )
    st.markdown("---")
    st.markdown("**Instructions**")
    st.markdown(
        """
        1. Choose a data source  
        2. If entering custom values, supply 5 returns for each asset  
        3. Click **Run Analysis**  
        4. Review the efficient frontier and notes  
        """
    )

# ──────────────────────────────────────────────────────────────
# Step 1 – Input Data
# ──────────────────────────────────────────────────────────────
st.subheader("Step 1 – Input Data")

watson_head_data = pd.DataFrame({
    "S return (%)": [6.6, 5.6, -9.0, 12.6, 14.0],
    "T return (%)": [24.5, -5.9, 19.9, -7.8, 14.8],
})

if data_choice == "Use Watson & Head test data":
    st.markdown("Default dataset from **Watson & Head (2023)**.")
    st.dataframe(watson_head_data, use_container_width=True)
    df = watson_head_data.rename(columns={"S return (%)": "S", "T return (%)": "T"}).copy()
else:
    st.markdown("Enter your own **5 annual returns (%)** for each asset:")
    df = st.data_editor(
        pd.DataFrame({"S": [None] * 5, "T": [None] * 5}),
        num_rows="fixed",
        use_container_width=True,
    )

# ──────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────
def clean_and_convert(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Drop missing values and convert % returns to decimals."""
    df_clean = df_raw.dropna()
    if df_clean.empty:
        raise ValueError("No valid data provided — please complete the table.")
    return df_clean.astype(float) / 100.0


def compute_asset_stats(df_dec: pd.DataFrame) -> dict:
    """Compute mean, standard deviation and correlation."""
    mean_s = df_dec["S"].mean()
    mean_t = df_dec["T"].mean()
    sd_s = df_dec["S"].std(ddof=0)  # population standard deviation
    sd_t = df_dec["T"].std(ddof=0)
    corr = df_dec["S"].corr(df_dec["T"])
    return {
        "mean_s": mean_s, "mean_t": mean_t,
        "sd_s": sd_s, "sd_t": sd_t,
        "corr": corr,
    }


def portfolio_return_sd(
    w_s: float, w_t: float, mean_s: float, mean_t: float,
    sd_s: float, sd_t: float, corr: float
) -> tuple[float, float]:
    """Return (expected return, standard deviation) for a two-asset portfolio."""
    ret = w_s * mean_s + w_t * mean_t
    var = (
        w_s**2 * sd_s**2
        + w_t**2 * sd_t**2
        + 2 * w_s * w_t * sd_s * sd_t * corr
    )
    return ret, float(np.sqrt(var))


# ──────────────────────────────────────────────────────────────
# Step 2 – Run Analysis
# ──────────────────────────────────────────────────────────────
st.subheader("Step 2 – Run Analysis")
run = st.button("Run Analysis", type="primary")

if run:
    try:
        df_dec = clean_and_convert(df)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    stats = compute_asset_stats(df_dec)
    mean_s, mean_t = stats["mean_s"], stats["mean_t"]
    sd_s, sd_t = stats["sd_s"], stats["sd_t"]
    corr = stats["corr"]

    st.success("✔ Calculation complete.")

    # Summary statistics
    st.markdown("### Asset Statistics")
    summary = pd.DataFrame(
        {
            "Mean return (%)": [f"{mean_s * 100:.2f}", f"{mean_t * 100:.2f}"],
            "Standard deviation (%)": [f"{sd_s * 100:.2f}", f"{sd_t * 100:.2f}"],
        },
        index=["S", "T"],
    )
    st.dataframe(summary, use_container_width=True)
    st.metric("Correlation coefficient (r)", f"{corr:.2f}")

    # Portfolios
    st.subheader("Step 3 – Portfolio Risk and Return")

    weights = [
        (1.0, 0.0), (0.8, 0.2), (0.6, 0.4),
        (0.4, 0.6), (0.2, 0.8), (0.0, 1.0)
    ]
    labels = ["100% S", "80/20", "60/40", "40/60", "20/80", "100% T"]

    rows = []
    sd_values = []
    for (w_s, w_t), label in zip(weights, labels, strict=True):
        r, s = portfolio_return_sd(w_s, w_t, mean_s, mean_t, sd_s, sd_t, corr)
        rows.append([label, f"{r * 100:.2f}", f"{s * 100:.2f}"])
        sd_values.append(s)

    table_df = pd.DataFrame(rows, columns=["Portfolio", "Mean return (%)", "Standard deviation (%)"])
    st.dataframe(table_df, use_container_width=True)

    # Plot
    st.subheader("Step 4 – Efficient Frontier (Discrete Example)")
    x = table_df["Standard deviation (%)"].astype(float)
    y = table_df["Mean return (%)"].astype(float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(x, y, marker="o", linestyle="-", color=ACCENT_COLOR)

    for i, row in table_df.iterrows():
        ax.annotate(row["Portfolio"], (x.iloc[i], y.iloc[i]), fontsize=8, xytext=(5, 3), textcoords="offset points")

    ax.set_xlabel("Risk (standard deviation, %)")
    ax.set_ylabel("Expected return (%)")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    st.pyplot(fig)

    # Diversification
    st.subheader("Step 5 – Diversification Benefit")
    min_risk = min(sd_values) * 100
    st.info(
        f"📉 Minimum portfolio risk observed: **{min_risk:.2f}%** "
        f"\n(compared to S = {sd_s*100:.2f}%, T = {sd_t*100:.2f}%)"
    )

# ──────────────────────────────────────────────────────────────
# Methodology Notes
# ──────────────────────────────────────────────────────────────
with st.expander("📎 Methodology & Notes (Formulas + References)"):
    st.markdown(
        r"""
        ### Statistical Measures
        
        - Mean return:
          \[
          \mu = \frac{1}{n}\sum_{i=1}^{n} R_i
          \]
        
        - Population standard deviation:
          \[
          \sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(R_i - \mu)^2}
          \]
        
        - Correlation:
          \[
          \rho_{S,T}=\frac{\mathrm{Cov}(R_S, R_T)}{\sigma_S \sigma_T}
          \]
        
        ### Two-Asset Portfolio
        
        - Expected return:
          \[
          E(R_P)=w_S\mu_S+w_T\mu_T
          \]
        
        - Portfolio variance:
          \[
          \sigma_P^2=w_S^2\sigma_S^2+w_T^2\sigma_T^2+2w_Sw_T\sigma_S\sigma_T\rho_{S,T}
          \]
        
        - Standard deviation:
          \[
          \sigma_P=\sqrt{\sigma_P^2}
          \]
        
        ### References
        
        - Watson, D. & Head, A. (2023). *Corporate Finance* (8th ed.). Pearson Education.
        - This module was co-created by **Alastair McBride** and a **Generative AI Assistant**, with full prompt documentation in `docs/prompt_record.md`.
        """
    )
