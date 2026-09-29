import streamlit as st

CSS = """
<style>

/* =========================================================
   MEMORA — GLOBAL DESIGN SYSTEM
   ========================================================= */

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --ivory: #F7F5EE;
    --paper: #FCFBF7;
    --forest: #0F4D3F;
    --forest-dark: #0A382F;
    --sage: #E5EEE7;
    --sage-dark: #C9DCCF;
    --ink: #173C35;
    --muted: #6C817B;
    --coral: #E96E61;
    --coral-soft: #FBE4DF;
    --line: #DDE4DE;
    --white: #FFFFFF;
}

/* Page */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--ivory);
    color: var(--ink);
}

/* Remove Streamlit chrome */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main content */

.block-container {
    max-width: 1180px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
}

/* =========================================================
   TYPOGRAPHY
   ========================================================= */

h1, h2, h3 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    color: var(--ink) !important;
    font-weight: 500 !important;
}

h1 {
    font-size: 4.5rem !important;
    line-height: 0.98 !important;
    letter-spacing: -0.035em !important;
}

h2 {
    font-size: 3rem !important;
    line-height: 1.05 !important;
}

h3 {
    font-size: 2rem !important;
}

p {
    color: #48655E;
}

/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    border-radius: 10px !important;
    min-height: 44px !important;
    padding: 0.65rem 1.25rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: 1px solid var(--line) !important;
    background: var(--white) !important;
    color: var(--forest) !important;
    transition: all 0.18s ease !important;
}

.stButton > button:hover {
    border-color: var(--forest) !important;
    color: var(--forest-dark) !important;
    transform: translateY(-1px);
}

/* Primary buttons */

.stButton > button[kind="primary"] {
    background: var(--forest) !important;
    color: white !important;
    border-color: var(--forest) !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--forest-dark) !important;
    border-color: var(--forest-dark) !important;
}

/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--line);
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    color: #567069;
    padding: 0.7rem 1rem;
    border-radius: 9px 9px 0 0;
}

.stTabs [aria-selected="true"] {
    color: var(--forest) !important;
    background: var(--sage) !important;
    font-weight: 600 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: transparent !important;
}

/* =========================================================
   SELECTBOX / INPUTS
   ========================================================= */

.stSelectbox > div > div,
.stTextInput > div > div {
    background: var(--paper) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
}

.stSelectbox label,
.stTextInput label {
    color: var(--ink) !important;
    font-weight: 600 !important;
}

/* =========================================================
   EXPANDERS
   ========================================================= */

.streamlit-expanderHeader {
    background: var(--paper) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
}

/* =========================================================
   CUSTOM MEMORA COMPONENTS
   ========================================================= */

.memora-eyebrow {
    color: var(--coral);
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.memora-subtitle {
    color: var(--muted);
    font-size: 0.88rem;
    letter-spacing: 0.04em;
}

.memora-muted {
    color: var(--muted);
}

.memora-card {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.5rem;
}

.memora-section-label {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.memora-divider {
    height: 1px;
    background: var(--line);
    margin: 2rem 0;
}

/* =========================================================
   MEMORY ENGINE
   ========================================================= */

.memory-engine {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.5rem;
}

.memory-title {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
}

.memory-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65rem 0;
}

.memory-id {
    display: inline-block;
    background: var(--sage);
    color: var(--forest);
    border-radius: 7px;
    padding: 0.28rem 0.55rem;
    font-size: 0.72rem;
    font-weight: 700;
}

.memory-id-loss {
    background: var(--coral-soft);
    color: #C95349;
}

.memory-status-win {
    color: #18815E;
    font-weight: 600;
    font-size: 0.82rem;
}

.memory-status-loss {
    color: #D5534B;
    font-weight: 600;
    font-size: 0.82rem;
}

.memory-difference {
    background: var(--sage);
    border: 1px solid var(--sage-dark);
    color: var(--forest);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.65rem 0;
    font-weight: 600;
}

/* =========================================================
   RISK CARDS
   ========================================================= */

.risk-card {
    background: var(--paper);
    border: 1px solid var(--line);
    border-left: 4px solid var(--coral);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.risk-label {
    color: var(--coral);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.risk-title {
    color: var(--ink);
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0.35rem 0 0.7rem;
}

/* =========================================================
   EVIDENCE CHIPS
   ========================================================= */

.evidence-chip {
    display: inline-block;
    background: var(--sage);
    color: var(--forest);
    border: 1px solid var(--sage-dark);
    border-radius: 7px;
    padding: 0.3rem 0.55rem;
    margin: 0.2rem;
    font-size: 0.72rem;
    font-weight: 700;
}

/* =========================================================
   STATUS
   ========================================================= */

.connected {
    color: #18815E;
    font-size: 0.78rem;
    font-weight: 700;
}

.connected-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #35A574;
    border-radius: 50%;
    margin-right: 6px;
}

/* =========================================================
   RFP HISTORY
   ========================================================= */

.history-table {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
}

.history-header {
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    h1 {
        font-size: 3.3rem !important;
    }

    h2 {
        font-size: 2.4rem !important;
    }

    .block-container {
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }
}

</style>
"""


def apply():
    st.markdown(CSS, unsafe_allow_html=True)