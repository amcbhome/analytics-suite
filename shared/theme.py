"""
shared/theme.py

Shared theme and layout utilities for the
GenAI Accounting Analytics Toolkit (Academic Theme).

Author: Alastair McBride & GenAI Assistant
"""

import streamlit as st

PRIMARY_COLOR = "#555555"   # Neutral graphite
ACCENT_COLOR = "#008080"    # Academic teal
BACKGROUND_COLOR = "#F5F5F5"
CARD_BACKGROUND = "#FFFFFF"


def set_page_config():
    """Configure the Streamlit page and inject global CSS."""
    st.set_page_config(
        page_title="GenAI Accounting – Predictive Analytics",
        layout="centered"
    )
    _inject_css()


def _inject_css():
    """Inject simple academic-style CSS for typography and layout."""
    st.markdown(
        f"""
        <style>
            html, body, [class*="stApp"] {{
                background-color: {BACKGROUND_COLOR};
                font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
            }}

            h1, h2, h3, h4 {{
                font-family: "Merriweather", "Georgia", "Times New Roman", serif;
                color: {PRIMARY_COLOR};
            }}

            .genai-header {{
                padding: 1.2rem 1.5rem;
                border-radius: 0.75rem;
                background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {ACCENT_COLOR} 100%);
                color: white;
                margin-bottom: 1.5rem;
            }}

            .genai-header h1 {{
                font-size: 1.8rem;
                margin-bottom: 0.3rem;
            }}

            .genai-header p {{
                margin: 0;
                font-size: 0.95rem;
                opacity: 0.9;
            }}

            .genai-card {{
                background-color: {CARD_BACKGROUND};
                padding: 1rem 1.25rem;
                border-radius: 0.75rem;
                border: 1px solid #DDDDDD;
                margin-bottom: 1rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def academic_header(title: str, subtitle: str | None = None):
    """Render a consistent academic-style header."""
    st.markdown('<div class="genai-header">', unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
