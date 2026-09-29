import sys
import json
import subprocess
from pathlib import Path

import streamlit as st


# ============================================================
# PATHS / IMPORTS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "frontend"))

st.set_page_config(
    page_title="MEMORA — RFP Decision Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    import theme
    theme.apply()
except Exception:
    pass


# ============================================================
# EXTRA UI CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .block-container {
        max-width: 1120px;
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
    }

    /* ---------- HEADER ---------- */

    .memora-header {
        padding: 4px 0 14px 0;
        border-bottom: 1px solid #D9DED8;
        margin-bottom: 24px;
    }

    .brand-name {
        color: #14503C;
        font-size: 20px;
        font-weight: 700;
        line-height: 1;
        letter-spacing: .01em;
    }

    .brand-tagline {
        color: #7A8982;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1.8px;
        margin-top: 6px;
    }

    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: #14503C;
        color: #F8F5ED;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        font-weight: 700;
        box-shadow: 0 7px 18px rgba(20,80,60,.15);
    }

    .status-pill {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 8px;
        color: #315C4E;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .8px;
        padding-top: 5px;
    }

    .status-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #36A66E;
        display: inline-block;
        box-shadow: 0 0 0 5px #E2F0E7;
    }

    /* ---------- HERO ---------- */

    .eyebrow {
        color: #D9694F;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #14503C;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 55px;
        line-height: 1.02;
        letter-spacing: -1.8px;
        margin: 0 0 12px 0;
    }

    .hero-title em {
        color: #D9694F;
        font-weight: 400;
    }

    .hero-copy {
        color: #426057;
        font-size: 16px;
        line-height: 1.55;
        max-width: 650px;
        margin-bottom: 15px;
    }

    /* ---------- MEMORY CARD ---------- */

    .memory-label {
        color: #7D8B85;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 17px;
    }

    .memory-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0;
        color: #345249;
        font-size: 14px;
    }

    .memory-id {
        background: #EAF2EA;
        color: #087F55;
        border-radius: 6px;
        padding: 5px 8px;
        font-family: monospace;
        font-size: 11px;
        margin-right: 8px;
    }

    .memory-id-loss {
        background: #FCE8E2;
        color: #D9694F;
    }

    .memory-found {
        background: #E2F0DF;
        color: #14503C;
        padding: 12px 13px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 600;
        margin: 10px 0;
    }

    /* ---------- SECTION LABEL ---------- */

    .section-label {
        color: #7D8B85;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    /* ---------- RESULT CARDS ---------- */

    .result-title {
        color: #14503C;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 28px;
        margin-bottom: 4px;
    }

    .evidence-chip {
        display: inline-block;
        background: #EAF2EA;
        color: #14503C;
        border-radius: 6px;
        padding: 4px 7px;
        font-family: monospace;
        font-size: 11px;
        margin-right: 4px;
    }

    .draft-box {
        background: #F1F6F0;
        border: 1px solid #D5E2D4;
        border-radius: 12px;
        padding: 18px;
        color: #294C40;
        line-height: 1.65;
    }

    .comparison-box {
        min-height: 150px;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #DADFD9;
        background: #FBFAF6;
    }

    .comparison-box-memory {
        border: 1px solid #BFD6C1;
        background: #F1F7EF;
    }

    .comparison-title {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #7D8B85;
        margin-bottom: 10px;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 9px !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"] {
        background: #14503C !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* ---------- TABS ---------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        border-bottom: 1px solid #D9DED8;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 9px 9px 0 0;
        padding: 9px 14px;
    }

    .stTabs [aria-selected="true"] {
        background: #E6EDE6;
        color: #14503C;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: #14503C;
    }

    /* ---------- SMALL TEXT ---------- */

    .muted {
        color: #77877F;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SAMPLE RFPs
# ============================================================

SAMPLE_RFPS = {
    "Lakeview Clinics — hard 90-day go-live": {
        "rfp_id": "RFP-NEW-1",
        "client_name": "Lakeview Clinics",
        "industry": "Healthcare",
        "company_size": "Mid-market",
        "rfp_summary": (
            "Patient intake and billing platform with a hard "
            "90-day go-live requirement."
        ),
        "key_requirements": [
            "HIPAA compliance",
            "EHR integration",
            "90-day go-live",
        ],
        "customer_priorities": [
            "Fast go-live",
            "Regulatory compliance",
        ],
        "customer_concerns": [
            "Vendor timelines slipping",
            "Data security",
        ],
    },
    "Northgate Community Health — flexible timeline": {
        "rfp_id": "RFP-NEW-2",
        "client_name": "Northgate Community Health",
        "industry": "Healthcare",
        "company_size": "Mid-market",
        "rfp_summary": (
            "Patient records modernisation with no fixed deadline. "
            "Security review is the main concern."
        ),
        "key_requirements": [
            "HIPAA compliance",
            "Security review",
            "Patient records",
        ],
        "customer_priorities": [
            "Security",
            "Reliability",
        ],
        "customer_concerns": [
            "Data security",
            "Integration risk",
        ],
    },
    "Pinecrest Specialty Hospital — hard 60-day go-live": {
        "rfp_id": "RFP-NEW-3",
        "client_name": "Pinecrest Specialty Hospital",
        "industry": "Healthcare",
        "company_size": "Enterprise",
        "rfp_summary": (
            "Scheduling and billing platform that must be live "
            "within 60 days with strict data-security requirements."
        ),
        "key_requirements": [
            "Security",
            "Scheduling",
            "Billing",
            "60-day go-live",
        ],
        "customer_priorities": [
            "Fast implementation",
            "Security",
        ],
        "customer_concerns": [
            "Implementation delays",
            "Data security",
        ],
    },
}


# ============================================================
# HELPERS
# ============================================================

def ids(items):
    if not items:
        return "No specific RFP evidence"

    return " ".join(
        f'<span class="evidence-chip">{item}</span>'
        for item in items
    )


def build_draft(rfp, result):
    """
    Create a concise proposal approach from the pre-mortem output.
    This is intentionally framed as a draft informed by MEMORA's
    evidence, rather than pretending it is a full proposal.
    """

    risks = result.get("risks", []) if result else []

    mitigations = []

    for risk in risks:
        mitigation = str(risk.get("mitigation", "")).strip()
        if mitigation and mitigation not in mitigations:
            mitigations.append(mitigation)

    if mitigations:
        strategy = " ".join(mitigations[:2])
    else:
        strategy = (
            "Lead with a delivery plan that directly addresses the "
            "client's highest-priority requirements and explicitly "
            "reduces the implementation risks identified in prior bids."
        )

    priorities = ", ".join(
        rfp.get("customer_priorities", [])[:2]
    )

    requirements = ", ".join(
        rfp.get("key_requirements", [])[:3]
    )

    return (
        f"For {rfp['client_name']}, the proposal should lead with "
        f"{priorities}. The response should explicitly address "
        f"{requirements} and make the delivery plan concrete rather "
        f"than relying on broad capability statements. "
        f"MEMORA's pre-mortem recommends: {strategy}"
    )


def memory_reason(result):
    if not result:
        return (
            "MEMORA has not analyzed this RFP yet. Run the pre-mortem "
            "to retrieve relevant organizational memory."
        )

    risks = result.get("risks", [])

    if not risks:
        return (
            "MEMORA did not identify a high-confidence historical risk "
            "for this RFP."
        )

    evidence = []

    for risk in risks[:3]:
        for item in risk.get("evidence", []) or []:
            if item not in evidence:
                evidence.append(item)

    if evidence:
        return (
            "MEMORA changed the recommendation using historical evidence "
            f"from {', '.join(evidence)}."
        )

    return (
        "MEMORA used recalled organizational experience to identify "
        "the risks shown below."
    )


def get_history():
    path = ROOT / "data" / "past_rfps.json"

    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return list(data.values())

    return data


# ============================================================
# HEADER
# ============================================================

h1, h2, h3 = st.columns([1.8, 5.2, 2.0], vertical_alignment="center")

with h1:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:11px;">
            <div class="brand-icon">M</div>
            <div>
                <div class="brand-name">MEMORA</div>
                <div class="brand-tagline">RFP DECISION INTELLIGENCE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with h2:
    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:center;
            gap:28px;
            color:#536860;
            font-size:14px;
            padding-top:7px;
        ">
            <span style="
                background:#E6EDE6;
                color:#14503C;
                padding:9px 14px;
                border-radius:9px;
                font-weight:600;
            ">
                Analyze RFP
            </span>
            <span style="padding-top:9px;">Watch Memory Learn</span>
            <span style="padding-top:9px;">Past RFPs</span>
            <span style="padding-top:9px;">How It Works</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with h3:
    st.markdown(
        """
        <div class="status-pill">
            <span class="status-dot"></span>
            HINDSIGHT CONNECTED
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="memora-header"></div>', unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

hero_left, hero_right = st.columns([1.65, 1], gap="large")

with hero_left:

    st.markdown(
        '<div class="eyebrow">RFP DECISION INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title">
            Before you write,<br>
            <em>remember.</em>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-copy">
            MEMORA reviews your organization's past RFP wins and losses
            before you respond, identifies evidence-backed risks,
            and recommends how to adapt your strategy.
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:

    with st.container(border=True):

        st.markdown(
            '<div class="memory-label">MEMORY ENGINE</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="memory-row">
                <span>
                    <span class="memory-id">RFP-003</span>
                    Security-first
                </span>
                <span style="color:#198754;">✓ Won</span>
            </div>

            <div class="memory-row">
                <span>
                    <span class="memory-id memory-id-loss">RFP-011</span>
                    Security-first
                </span>
                <span style="color:#D9694F;">× Lost</span>
            </div>

            <div class="memory-found">
                ◉ &nbsp; MEMORA found the difference
            </div>

            <div class="memory-row">
                <span>
                    <span class="memory-id">RFP-019</span>
                    Adapted strategy
                </span>
                <span style="color:#198754;">✓ Won</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# NAVIGATION
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Analyze RFP",
        "Watch Memory Learn",
        "Past RFPs",
        "How It Works",
    ]
)


# ============================================================
# TAB 1 — ANALYZE RFP
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-label">NEW RFP UNDER REVIEW</div>',
        unsafe_allow_html=True,
    )

    choice = st.selectbox(
        "Choose a new RFP",
        list(SAMPLE_RFPS.keys()),
        label_visibility="collapsed",
    )

    rfp = SAMPLE_RFPS[choice]

    # Client context appears immediately.
    c1, c2, c3 = st.columns(3)

    with c1:
        st.caption("CLIENT PRIORITIES")
        st.write(
            " · ".join(rfp.get("customer_priorities", []))
        )

    with c2:
        st.caption("KEY REQUIREMENTS")
        st.write(
            " · ".join(rfp.get("key_requirements", []))
        )

    with c3:
        st.caption("CLIENT CONCERNS")
        st.write(
            " · ".join(rfp.get("customer_concerns", []))
        )

    # Main action is ABOVE output and visible.
    action_col, details_col = st.columns([1, 3])

    with action_col:

        analyze = st.button(
            "Analyze RFP",
            type="primary",
            use_container_width=True,
        )

    with details_col:

        with st.expander("View selected RFP"):

            st.write(rfp["rfp_summary"])

            st.json(rfp)

    if analyze:

        with st.spinner(
            "Recalling organizational memory and running pre-mortem..."
        ):

            try:

                import agent

                result = agent.premortem(rfp)

                st.session_state["result"] = result
                st.session_state["result_for"] = choice

            except Exception as e:

                st.session_state["result"] = None

                st.error(
                    f"MEMORA could not complete the analysis: {e}"
                )

    result = st.session_state.get("result")

    if result and st.session_state.get("result_for") == choice:

        st.markdown("---")

        # ----------------------------------------------------
        # MEMORY SIGNAL
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">MEMORY SIGNAL</div>',
            unsafe_allow_html=True,
        )

        st.info(memory_reason(result))

        # ----------------------------------------------------
        # RISKS
        # ----------------------------------------------------

        st.markdown(
            '<div class="result-title">What could make us lose?</div>',
            unsafe_allow_html=True,
        )

        risks = result.get("risks", [])

        if risks:

            for risk in risks:

                with st.container(border=True):

                    st.markdown(
                        f"### {risk.get('risk', '')}"
                    )

                    evidence = risk.get("evidence", [])

                    if evidence:
                        st.markdown(
                            f"**Evidence:** {ids(evidence)}",
                            unsafe_allow_html=True,
                        )

                    if risk.get("why_it_matters"):
                        st.write(
                            risk.get("why_it_matters")
                        )

                    if risk.get("mitigation"):
                        st.success(
                            "Recommended adaptation: "
                            + str(risk.get("mitigation"))
                        )

        else:

            st.success(
                "No major evidence-backed risk was returned."
            )

        # ----------------------------------------------------
        # DRAFTED APPROACH
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label" style="margin-top:25px;">'
            'DRAFTED APPROACH'
            '</div>',
            unsafe_allow_html=True,
        )

        draft = build_draft(rfp, result)

        st.markdown(
            f"""
            <div class="draft-box">
                <strong>Proposal approach for {rfp['client_name']}</strong><br><br>
                {draft}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # WITHOUT MEMORY / WITH MEMORY
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label" style="margin-top:25px;">'
            'WHAT MEMORY CHANGED'
            '</div>',
            unsafe_allow_html=True,
        )

        comparison_left, comparison_right = st.columns(2)

        with comparison_left:

            st.markdown(
                """
                <div class="comparison-box">
                    <div class="comparison-title">
                        WITHOUT ORGANIZATIONAL MEMORY
                    </div>

                    Start with a generic security-first proposal,
                    describe platform capabilities, and assume that
                    security strength is enough to establish confidence.
                </div>
                """,
                unsafe_allow_html=True,
            )

        with comparison_right:

            first_mitigation = ""

            if risks:
                first_mitigation = str(
                    risks[0].get("mitigation", "")
                )

            if not first_mitigation:
                first_mitigation = (
                    "Adapt the proposal to the historical failure "
                    "patterns identified for this RFP."
                )

            st.markdown(
                f"""
                <div class="comparison-box comparison-box-memory">
                    <div class="comparison-title">
                        WITH MEMORA MEMORY
                    </div>

                    {first_mitigation}

                    <br><br>

                    <strong>
                        Historical evidence is attached to the decision.
                    </strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # CONFLICTS
        # ----------------------------------------------------

        conflicts = result.get("conflicts", [])

        if conflicts:

            st.markdown(
                '<div class="section-label" style="margin-top:25px;">'
                'CONFLICTS IN OUR HISTORY'
                '</div>',
                unsafe_allow_html=True,
            )

            for conflict in conflicts:

                with st.container(border=True):

                    st.markdown(
                        f"**{conflict.get('claim', '')}**"
                    )

                    won = conflict.get("evidence_for", [])
                    lost = conflict.get("evidence_against", [])

                    st.markdown(
                        f"Won with: {ids(won)}",
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"Lost with: {ids(lost)}",
                        unsafe_allow_html=True,
                    )

                    if conflict.get("deciding_factor"):
                        st.write(
                            conflict.get("deciding_factor")
                        )

                    if conflict.get("resolution"):
                        st.success(
                            "Resolved by "
                            f"{conflict.get('resolution')}"
                        )

        # ----------------------------------------------------
        # MEMORIES USED
        # ----------------------------------------------------

        with st.expander(
            "Show the memories Hindsight recalled"
        ):

            memories = result.get("memories_used", [])

            if memories:

                for memory in memories:
                    st.write("• " + str(memory))

            else:

                st.caption(
                    "No recalled memories were returned."
                )

        # ----------------------------------------------------
        # CLOSE THE LOOP
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label" style="margin-top:25px;">'
            'CLOSE THE LOOP'
            '</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "After the real bid outcome is known, record it so "
            "MEMORA can learn from the experience."
        )

        with st.form("outcome_form"):

            outcome = st.radio(
                "Bid outcome",
                ["Won", "Lost"],
                horizontal=True,
            )

            reason = st.text_area(
                "What happened?",
                placeholder=(
                    "Example: The client chose a competitor because "
                    "our implementation timeline was too long."
                ),
            )

            save_outcome = st.form_submit_button(
                "Record outcome",
                type="primary",
            )

            if save_outcome:

                outcome_file = ROOT / "data" / "outcomes.jsonl"

                record = {
                    "rfp_id": rfp["rfp_id"],
                    "client_name": rfp["client_name"],
                    "outcome": outcome,
                    "reason": reason,
                }

                with open(
                    outcome_file,
                    "a",
                    encoding="utf-8",
                ) as f:

                    f.write(
                        json.dumps(
                            record,
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

                # Try to retain into Hindsight if backend supports it.
                retained = False

                try:

                    import memory

                    if hasattr(memory, "record_outcome"):

                        memory.record_outcome(
                            rfp_id=rfp["rfp_id"],
                            outcome=outcome,
                            reason=reason,
                        )

                        retained = True

                except Exception as e:

                    st.warning(
                        "Outcome saved locally, but Hindsight "
                        f"retention was not completed: {e}"
                    )

                if retained:

                    st.success(
                        "Outcome recorded and sent to Hindsight memory."
                    )

                else:

                    st.success(
                        "Outcome recorded locally."
                    )


# ============================================================
# TAB 2 — WATCH MEMORY LEARN
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-label">MEMORY EVOLUTION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="result-title">
            Watch MEMORA change its understanding.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "The same Lakeview-style RFP is evaluated as new experiences "
        "enter organizational memory."
    )

    # Target RFP summary
    with st.container(border=True):

        st.markdown(
            "**TARGET RFP**  Lakeview Clinics · Healthcare · "
            "Hard 90-day go-live"
        )

        st.caption(
            "The demo reveals the Cedar Ridge loss and Bayshore "
            "resolution as new experiences."
        )

    run1, run2 = st.columns([1, 1])

    with run1:

        if st.button(
            "Run full learning demo",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "Running the three-stage memory demonstration..."
            ):

                try:

                    process = subprocess.run(
                        [
                            sys.executable,
                            str(
                                ROOT
                                / "backend"
                                / "learning_demo.py"
                            ),
                        ],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        cwd=str(ROOT),
                    )

                    output = (
                        process.stdout
                        + "\n"
                        + process.stderr
                    )

                    st.session_state[
                        "learning_output"
                    ] = output

                except Exception as e:

                    st.error(
                        f"Learning demo failed: {e}"
                    )

    with run2:

        recorded = ROOT / "docs" / "run_stage012.txt"

        if st.button(
            "Show recorded learning run",
            use_container_width=True,
        ):

            if recorded.exists():

                st.session_state[
                    "learning_output"
                ] = recorded.read_text(
                    encoding="utf-8",
                    errors="replace",
                )

            else:

                st.warning(
                    "No recorded learning run found."
                )

    if "learning_output" in st.session_state:

        st.markdown("---")

        st.markdown(
            "### Memory learning trace"
        )

        st.code(
            st.session_state["learning_output"],
            language="text",
        )

        st.success(
            "The important demo story: past outcome → new memory "
            "→ changed risk assessment → adapted strategy."
        )


# ============================================================
# TAB 3 — PAST RFPs
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-label">ORGANIZATIONAL MEMORY</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="result-title">
            Past RFPs
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "The experiences MEMORA can learn from."
    )

    rows = get_history()

    if rows:

        q = st.text_input(
            "Search clients or RFPs",
            placeholder="Search Cedar Ridge, RFP-011, healthcare...",
        )

        outcome_filter = st.radio(
            "Outcome",
            ["All", "Won", "Lost"],
            horizontal=True,
        )

        industry_filter = st.selectbox(
            "Industry",
            ["All"]
            + sorted(
                {
                    str(r.get("industry", ""))
                    for r in rows
                    if r.get("industry")
                }
            ),
        )

        filtered = rows

        if q:

            filtered = [
                r
                for r in filtered
                if q.lower()
                in json.dumps(
                    r,
                    ensure_ascii=False,
                ).lower()
            ]

        if outcome_filter != "All":

            filtered = [
                r
                for r in filtered
                if str(
                    r.get("outcome", "")
                ).lower()
                == outcome_filter.lower()
            ]

        if industry_filter != "All":

            filtered = [
                r
                for r in filtered
                if r.get("industry")
                == industry_filter
            ]

        display_rows = []

        for r in filtered:

            display_rows.append(
                {
                    "RFP": r.get("rfp_id", ""),
                    "Client": r.get("client_name", ""),
                    "Industry": r.get("industry", ""),
                    "Outcome": r.get("outcome", ""),
                    "Strategy": r.get(
                        "proposal_strategy",
                        r.get("strategy", ""),
                    ),
                }
            )

        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.warning(
            "No RFP history found in data/past_rfps.json."
        )


# ============================================================
# TAB 4 — HOW MEMORA LEARNS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-label">THE MEMORY LOOP</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="result-title">
            How MEMORA learns
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "MEMORA does not simply retrieve documents. "
        "It uses organizational experience to change future decisions."
    )

    steps = [

        (
            "01",
            "Retain",
            "Past RFP experiences enter Hindsight memory."
        ),

        (
            "02",
            "Recall",
            "Relevant wins, losses, requirements and outcomes "
            "are retrieved for the new RFP."
        ),

        (
            "03",
            "Reflect",
            "MEMORA compares what worked, what failed, "
            "and what differed between those experiences."
        ),

        (
            "04",
            "Pre-Mortem",
            "Before writing, MEMORA identifies how the "
            "new proposal could fail."
        ),

        (
            "05",
            "Adapt",
            "The proposal strategy changes based on evidence "
            "from previous outcomes."
        ),

        (
            "06",
            "Outcome",
            "The real bid result is recorded so the next "
            "proposal starts with more experience."
        ),
    ]

    for number, heading, description in steps:

        with st.container(border=True):

            col1, col2 = st.columns([1, 8])

            with col1:

                st.markdown(
                    f"### {number}"
                )

            with col2:

                st.markdown(
                    f"**{heading}**"
                )

                st.write(
                    description
                )

    st.markdown("---")

    st.markdown(
        "### Why Hindsight matters"
    )

    st.write(
        "Hindsight is the memory layer behind MEMORA's retain, "
        "recall and reflection workflow. The application uses that "
        "organizational memory before generating its pre-mortem."
    )

    st.info(
        "Core idea: MEMORA remembers why the organization won "
        "or lost — not just what was written."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

footer_left, footer_right = st.columns(2)

with footer_left:

    st.caption(
        "MEMORA · RFP Decision Intelligence"
    )

with footer_right:

    st.caption(
        "Powered by Hindsight memory + LLM reasoning"
    )