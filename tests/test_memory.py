import json
import backend.memory as memory


def test_rfp_to_text_includes_key_fields():
    """_rfp_to_text must embed the fields the agent actually reasons over."""
    sample = {
        "rfp_id": "RFP-999",
        "client_name": "Test Client",
        "industry": "Healthcare",
        "company_size": "Mid-market",
        "deal_size_usd": 100000,
        "rfp_summary": "Test summary text.",
        "key_requirements": ["Req A", "Req B"],
        "customer_priorities": ["Fast go-live"],
        "customer_concerns": ["Cost"],
        "proposal_strategy": "Security-first approach.",
        "pricing_approach": "Tiered pricing.",
        "customer_objections": ["Too expensive"],
        "outcome": "won",
        "client_reason": "Great pricing.",
    }
    text = memory._rfp_to_text(sample)
    assert "RFP-999" in text
    assert "Test Client" in text
    assert "Security-first approach" in text
    assert "WON" in text


def test_rfp_to_text_excludes_lessons_learned():
    """
    Regression test: lessons_learned must never be fed into Hindsight.
    If it were, the agent would just be echoing a pre-written
    conclusion instead of forming its own belief from raw facts.
    """
    sample = {
        "rfp_id": "RFP-999",
        "client_name": "Test Client",
        "industry": "Healthcare",
        "company_size": "Mid-market",
        "deal_size_usd": 100000,
        "rfp_summary": "Test summary text.",
        "key_requirements": [],
        "customer_priorities": [],
        "customer_concerns": [],
        "proposal_strategy": "Security-first approach.",
        "pricing_approach": "Tiered pricing.",
        "customer_objections": [],
        "outcome": "lost",
        "client_reason": "Missed deadline.",
        "lessons_learned": "UNIQUE_MARKER_SHOULD_NEVER_APPEAR",
    }
    text = memory._rfp_to_text(sample)
    assert "UNIQUE_MARKER_SHOULD_NEVER_APPEAR" not in text


def test_ingest_history_respects_holdout_ids(monkeypatch):
    """
    ingest_history must skip any rfp_id listed in holdout_ids —
    this is what makes the learning-loop demo's staged reveal possible.
    """
    fake_rfps = [
        {"rfp_id": "RFP-001", "date_closed": "2025-01-01", "outcome": "won",
         "client_name": "A", "industry": "X", "company_size": "Y",
         "deal_size_usd": 1, "rfp_summary": "", "key_requirements": [],
         "customer_priorities": [], "customer_concerns": [],
         "proposal_strategy": "", "pricing_approach": "",
         "customer_objections": [], "client_reason": ""},
        {"rfp_id": "RFP-002", "date_closed": "2025-01-02", "outcome": "lost",
         "client_name": "B", "industry": "X", "company_size": "Y",
         "deal_size_usd": 1, "rfp_summary": "", "key_requirements": [],
         "customer_priorities": [], "customer_concerns": [],
         "proposal_strategy": "", "pricing_approach": "",
         "customer_objections": [], "client_reason": ""},
    ]

    retained_ids = []

    def fake_read_text(self, encoding="utf-8"):
        return json.dumps(fake_rfps)

    def fake_retain(**kwargs):
        retained_ids.append(kwargs.get("document_id"))

    monkeypatch.setattr(memory.Path, "read_text", fake_read_text)
    monkeypatch.setattr(memory.client, "retain", fake_retain)
    monkeypatch.setattr(memory, "_ensure_bank", lambda: None)

    memory.ingest_history(holdout_ids=("RFP-002",))

    assert "RFP-001" in retained_ids
    assert "RFP-002" not in retained_ids