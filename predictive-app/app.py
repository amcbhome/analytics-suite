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

from __future__ import annotations

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
    title="📊 Predictive Analytics — Diversification of Risk",
    subtitle="Modern Portfolio Theory (MPT) example using assets S and T "
             "based on Watson & Head (2023)."
)

st.caption(
    "GenAI Accounting Analytics Toolkit · Predictive module · "
    "This app is for learning and illustration only and does not "
    "constitute investment advice."
)

# ──────────────────────────────────────────────────────────────
# Sidebar – context and options
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About this module")
    st.markdown(
        """
        This predictive analytics example uses **historic annual returns**
        to estimate:

        - Mean returns for assets S and T  
        - Volatility (standard deviation)  
        - Linear correlation between S and T  
        - Portfolio risk for different weightings  

        The example follows the structure of **Watson & Head (2023),
        Corporate Finance, Chapter on Risk and Return.**
        """
    )
    st.markdown("---")
    st.markdown("**Input mode**")
    data_choice = st.radio(
        "Choose data source:",
        ["Use Watson & Head test data", "Enter my own 5-year returns"],
        index=0,
    )

    st.markdown("---")
    st.markdown("**Instructions**")
    st.markdown(
        """
        1. Select the input mode.  
        2. If entering your own data, supply 5 annual returns for S and T.  
        3. Click **Run Analysis** to compute statistics and plot the frontier.  
        4. Open **Methodology & Notes** for formulas and interpretation.
        """
    )

# ──────────────────────────────────────────────────────────────
# Step 1 – Input Data
# ──────────────────────────────────────────────────────────────
st.subheader("Step 1 – Input data")

watson_head_data = pd.DataFrame({
    "S return (%)": [6.6, 5.6, -9.0, 12.6, 14.0],
    "T return (%)": [24.5, -5.9, 19.9, -7.8, 14.8],
})

if data_choice == "Use Watson & Head test data":
    st.markdown(
        "Using default dataset from **Watson & Head (2023)** "
        "– five years of annual returns for S and T."
    )
    st.dataframe(watson_head_data, use_container_width=True)
    df = watson_head_data.rename(
        columns={"S return (%)": "S", "T return (%)": "T"}
    ).copy()
else:
    st.markdown(
        "Enter or edit your own **5 annual returns (%)** "
        "for each asset:"
    )
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
        raise ValueError("No valid data provided – please complete the table.")
    df_clean = df_clean.astype(float) / 100.0
    return df_clean


def compute_asset_stats(df_dec: pd.DataFrame) -> dict:
    """Compute mean, standard deviation and correlation."""
    mean_s = df_dec["S"].mean()
    mean_t = df_dec["T"].mean()
    sd_s = df_dec["S"].std(ddof=0)  # population standard deviation
    sd_t = df_dec["T"].std(ddof=0)
    corr = df_dec["S"].corr(df_dec["T"])
    return {
        "mean_s": mean_s,
        "mean_t": mean_t,
        "sd_s": sd_s,
        "sd_t": sd_t,
        "corr": corr,
    }


def portfolio_return_sd(
    w_s: float, w_t: float, mean_s: float, mean_t: float,
    sd_s: float, sd_t: float, corr: float
) -> tuple[float, float]:
    """Return (expected return, standard deviation) for a 2-asset portfolio."""
    p_return = w_s * mean_s + w_t * mean_t
    variance = (
        w_s**2 * sd_s**2
        + w_t**2 * sd_t**2
        + 2 * w_s * w_t * sd_s * sd_t * corr
    )
    p_sd = float(np.sqrt(variance))
    return p_return, p_sd


# ──────────────────────────────────────────────────────────────
# Step 2 – Run Analysis
# ──────────────────────────────────────────────────────────────
st.subheader("Step 2 – Run analysis")

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

    st.success("✅ Calculation complete.")

    # Summary statistics
    st.markdown("### Asset statistics")
    summary = pd.DataFrame(
        {
            "Mean return (%)": [f"{mean_s * 100:.2f}", f"{mean_t * 100:.2f}"],
            "Standard deviation (%)": [
                f"{sd_s * 100:.2f}",
                f"{sd_t * 100:.2f}",
            ],
        },
        index=["S", "T"],
    )
    st.dataframe(summary, use_container_width=True)
    st.metric("Correlation coefficient (r)", f"{corr:.2f}")

    # ──────────────────────────────────────────────────────────
    # Step 3 – Portfolio risk & return
    # ──────────────────────────────────────────────────────────
    st.subheader("Step 3 – Portfolio risk and return")

    # Watson & Head style weightings
    weights = [
        (1.0, 0.0),
        (0.8, 0.2),
        (0.6, 0.4),
        (0.4, 0.6),
        (0.2, 0.8),
        (0.0, 1.0),
    ]
    labels = [
        "All S (100/0)",
        "A (80/20)",
        "B (60/40)",
        "C (40/60)",
        "D (20/80)",
        "All T (0/100)",
    ]

    rows = []
    sd_values = []
    for (w_s, w_t), label in zip(weights, labels, strict=True):
        p_ret, p_sd = portfolio_return_sd(
            w_s, w_t, mean_s, mean_t, sd_s, sd_t, corr
        )
        rows.append(
            [
                label,
                f"{p_ret * 100:.2f}",
                f"{p_sd * 100:.2f}",
            ]
        )
        sd_values.append(p_sd)

    table_df = pd.DataFrame(
        rows,
        columns=["Portfolio", "Mean return (%)", "Standard deviation (%)"],
    )
    st.dataframe(table_df, use_container_width=True)

    # Efficient frontier plot
    st.subheader("Step 4 – Efficient frontier (two-asset example)")
    x = table_df["Standard deviation (%)"].astype(float)
    y = table_df["Mean return (%)"].astype(float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(x, y, marker="o", linestyle="-", color=ACCENT_COLOR)

    for i, row in table_df.iterrows():
        ax.annotate(
            row["Portfolio"],
            (x.iloc[i], y.iloc[i]),
            fontsize=8,
            xytext=(5, 3),
            textcoords="offset points",
        )

    ax.set_xlabel("Risk (standard deviation, %)")
    ax.set_ylabel("Expected return (%)")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    st.pyplot(fig)

    # ──────────────────────────────────────────────────────────
    # Step 5 – Diversification benefit
    # ──────────────────────────────────────────────────────────
    st.subheader("Step 5 – Diversification benefit")

    min_portfolio_risk = min(sd_values) * 100.0
    s_risk_reduction = sd_s * 100.0 - min_portfolio_risk
    t_risk_reduction = sd_t * 100.0 - min_portfolio_risk

    st.info(
        f"📉 Minimum portfolio risk (across the tested weightings) is "
        f"**{min_portfolio_risk:.2f}%**, compared with:\n\n"
        f"- Asset S: **{sd_s * 100:.2f}%**\n"
        f"- Asset T: **{sd_t * 100:.2f}%**\n\n"
        f"This illustrates how diversification can reduce volatility when "
        f"assets are not perfectly positively correlated."
    )

    st.markdown(
        f"> **Approximate risk reduction** – relative to the minimum observed "
        f"portfolio risk:\n"
        f"> - S: ≈ **{s_risk_reduction:.2f} percentage points**\n"
        f"> - T: ≈ **{t_risk_reduction:.2f} percentage points**"
    )

# ──────────────────────────────────────────────────────────────
# Methodology & Notes (Collapsible)
# ──────────────────────────────────────────────────────────────
with st.expander("📎 Methodology & Notes (formulas and references)"):
    st.markdown(
        """
        ### Statistical measures

        Let \\( R_S \\) and \\( R_T \\) denote the random returns on assets S and T.

        - **Mean (expected) return** for S:

          \\[
          \\mu_S = \\frac{1}{n} \\sum_{i=1}^n R_{S,i}
          \\]

        - **Standard deviation** (volatility) for S (population form):

          \\[
          \\sigma_S = \\sqrt{\\frac{1}{n} \\sum_{i=1}^n (R_{S,i} - \\mu_S)^2}
          \\]

        - **Correlation coefficient** between S and T:

          \\[
          \\rho_{S,T} = \\frac{\\mathrm{Cov}(R_S, R_T)}{\\sigma_S \\sigma_T}
          \\]

        ### Two-asset portfolio

        For weights \\( w_S \\) and \\( w_T \\) (with \\( w_S + w_T = 1 \\)):

        - **Expected portfolio return**:

          \\[
          E(R_P) = w_S \\mu_S + w_T \\mu_T
          \\]

        - **Portfolio variance**:

          \\[
          \\sigma_P^2 = w_S^2 \\sigma_S^2
          + w_T^2 \\sigma_T^2
          + 2 w_S w_T \\sigma_S \\sigma_T \\rho_{S,T}
          \\]

        - **Portfolio standard deviation**:

          \\[
          \\sigma_P = \\sqrt{\\sigma_P^2}
          \\]

        ### Interpretation in this app

        - Default data replicates a teaching example from Watson & Head (2023).  
        - The portfolios labelled A, B, C, D follow a standard 2-asset
          teaching pattern (e.g. 80/20, 60/40, etc.).  
        - The efficient frontier plotted here is discrete (only the tested
          weightings), but it illustrates the risk–return trade-off.

        ### Documentation and AI provenance

        - This module was co-created by **Alastair McBride** and a
          **Generative AI assistant**.  
        - The original human instruction and prompt are recorded in:
          `docs/prompt_record.md`.  
        - The purpose is to provide **transparent, auditable documentation**
          of AI-assisted coding for academic and professional review.
        """
    )
