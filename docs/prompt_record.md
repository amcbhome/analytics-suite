# Prompt Log — Predictive Analytics Module

**Project:** GenAI Accounting Analytics Toolkit  
**Module:** Predictive Analytics — Diversification of Risk  
**Author:** Alastair McBride  
**Model:** ChatGPT (GPT-5.1 Thinking)  
**Date:** (fill in date you commit this, e.g. 2025-12-06)

---

## Human Instruction (excerpt)

> Another feature of the project is documentation. I want this to include the prompts that generated the code. Here is the code for the example of predictive analytics:
>
> ```python
> import streamlit as st
> import pandas as pd
> import numpy as np
> import matplotlib.pyplot as plt
> 
> # (original predictive app code omitted here for brevity in this log)
> ```
>
> Ok. I want to rebuild 3 projects that will give a uniformed branded look to the Streamlit apps. Each project will cover a type of analytics - descriptive, predictive and prescriptive.

The assistant responded by:

- Proposing a unified academic theme (grey + teal, research style).  
- Refactoring the supplied code into a documented module with:
  - Shared theming via `shared/theme.py`  
  - A clear docstring for purpose and formulas  
  - A “Methodology & Notes” section with LaTeX-rendered formulas  
  - A separation between original code (`versions/original_app.py`) and the academic-branded `app.py`.

---

## Notes on AI Involvement

- The **logic and original example** (Watson & Head returns, weightings) are from the human author’s prior work and standard finance teaching material.
- The **layout, theme, and documentation structure** (headers, methodology expander, provenance text) were suggested and drafted by the AI assistant.
- The human author remains responsible for:
  - Verifying correctness of calculations
  - Ensuring appropriate referencing (Watson & Head, 2023)
  - Deciding how the module is used in assessment or professional contexts.
