"""
Learning-loop demo: shows MEMORA's pre-mortem changing after a new
outcome (RFP-011's loss) is added to memory.

Uses a SEPARATE bank ("memora-demo") so the real "memora-rfp" bank
used by agent.py and the tests is never touched.
"""
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import memory
import agent

DEMO_BANK = "memora-demo"
memory.BANK_ID = DEMO_BANK
agent.BANK_ID = DEMO_BANK

_real_known_conflicts = agent._known_conflicts
_hidden_ids = {"RFP-011", "RFP-019"}  # both hidden at Stage 0


def _staged_known_conflicts():
    lines = _real_known_conflicts()
    return [
        line for line in lines
        if not (agent._ids(line) & _hidden_ids)
    ]


agent._known_conflicts = _staged_known_conflicts

TEST_RFP = {
    "rfp_id": "TEST-LAKEVIEW",
    "client_name": "Lakeview Clinics",
    "industry": "Healthcare",
    "company_size": "Mid-market",
    "deal_size_usd": 300000,
    "rfp_summary": (
        "Lakeview Clinics needs a HIPAA-compliant patient intake and "
        "billing platform live within 90 days to support three new "
        "clinic openings."
    ),
    "key_requirements": ["HIPAA compliance", "EHR integration", "90-day go-live"],
    "customer_priorities": ["Fast go-live", "Regulatory compliance"],
    "customer_concerns": ["Vendor timelines slipping", "Data security"],
}


def _section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _show(result):
    if result.get("error"):
        print("ERROR:", result["error"])
        return
    risks = result.get("risks", [])
    if not risks:
        print("(no risks returned)")
    for r in risks:
        print(f"- RISK: {r['risk']}")
        print(f"  evidence: {r.get('evidence', [])}")
    ids = {e for r in risks for e in r.get("evidence", [])}
    print(f"\n  [risk evidence ids: {sorted(ids)}]")


def main():
    _section("STAGE 0 — RFP-011 and RFP-019 both hidden")
    memory.ingest_history(holdout_ids=("RFP-011", "RFP-019"))
    print("\nWaiting for Hindsight to process...")
    time.sleep(30)

    stage0 = agent.premortem(TEST_RFP)
    _show(stage0)

    _section("STAGE 0 CHECK")
    stage0_ids = {e for r in stage0.get("risks", []) for e in r.get("evidence", [])}
    print("RFP-011 cited in risks:", "RFP-011" in stage0_ids, "(expect False)")
    print("RFP-019 cited in risks:", "RFP-019" in stage0_ids, "(expect False)")
    print(
        "\nNote: the CONFLICTS block (from _known_conflicts, a deterministic "
        "check on the static JSON) will still show the RFP-019 resolution "
        "even here — that's expected and by design, not a bug. It's a "
        "separate safety layer from the memory-driven risks above."
    )


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()