import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "memora-rfp"  # fresh bank, so the smoke-test memory doesn't mix in
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "past_rfps.json"

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)


def _ensure_bank():
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="MEMORA RFP Memory",
            reflect_mission=(
                "I am a proposal strategist for a B2B software vendor. I learn from "
                "past RFP wins and losses. When advising, I always cite the RFP IDs "
                "that support a recommendation and I check for hard deadlines "
                "before reusing a past winning approach."
            ),
        )
    except Exception as e:
        print(f"(bank already exists or create skipped: {e})")


def _rfp_to_text(r: dict) -> str:
    """Raw experience only. lessons_learned is deliberately NOT included."""
    return (
        f"We {r['outcome'].upper()} {r['rfp_id']} for {r['client_name']} "
        f"({r['industry']}) using this approach: {r['proposal_strategy'].rstrip('.')}. "
        f"Result: {r['outcome'].upper()} because {r['client_reason'].rstrip('.')}. "
        f"Details of {r['rfp_id']}: {r['company_size']}, ${r['deal_size_usd']:,}. "
        f"Situation: {r['rfp_summary']} "
        f"Key requirements: {'; '.join(r['key_requirements'])}. "
        f"Customer priorities: {'; '.join(r['customer_priorities'])}. "
        f"Customer concerns: {'; '.join(r['customer_concerns'])}. "
        f"Pricing: {r['pricing_approach']} "
        f"Objections raised: {'; '.join(r['customer_objections'])}."
    )


def ingest_history(holdout_ids=()):
    """Retain every past RFP in date order. holdout_ids are skipped so you
    can feed them in live during the demo."""
    _ensure_bank()
    rfps = sorted(json.loads(DATA_PATH.read_text(encoding="utf-8")),
                  key=lambda r: r["date_closed"])
    for r in rfps:
        if r["rfp_id"] in holdout_ids:
            continue
        kwargs = dict(
            bank_id=BANK_ID,
            content=_rfp_to_text(r),
            context=f"rfp outcome: {r['outcome']}",
            timestamp=f"{r['date_closed']}T00:00:00Z",
        )

        client.retain(document_id=r["rfp_id"], update_mode="replace", **kwargs)
        print("retained", r["rfp_id"])

def get_strategy(new_rfp: str) -> dict:
    """Recall similar precedents, then reflect for a recommendation."""
    recalled = client.recall(bank_id=BANK_ID, query=new_rfp)
    precedents = [m.text for m in recalled.results]
    answer = client.reflect(
        bank_id=BANK_ID,
        query=(
            "A new RFP came in:\n" + new_rfp +
            "\n\nBased on our past wins and losses, what should we lead with, "
            "what should we avoid, and why? Cite the RFP IDs."
        ),
    )
    return {"recommendation": answer.text, "precedents": precedents}


def record_outcome(rfp_text: str, outcome: str, reason: str,
                   probe: str, date_iso: str, wait_s: int = 20) -> dict:
    """Retain a new outcome and return what the agent believed before/after."""
    before = client.reflect(bank_id=BANK_ID, query=probe).text
    client.retain(
        bank_id=BANK_ID,
        content=f"{rfp_text} Outcome: we {outcome.upper()}. Client's stated reason: {reason}",
        context=f"rfp outcome: {outcome}",
        timestamp=f"{date_iso}T00:00:00Z",
    )
    time.sleep(wait_s)  # give Hindsight time to extract and consolidate
    after = client.reflect(bank_id=BANK_ID, query=probe).text
    return {"before": before, "after": after}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if cmd == "ingest":
            # hold out the last two RFPs to use as live "new outcomes" later
            ingest_history(holdout_ids=("RFP-024", "RFP-025"))
        elif cmd == "ask":
            out = get_strategy(" ".join(sys.argv[2:]))
            print("\nRECOMMENDATION:\n", out["recommendation"])
            print("\nPRECEDENTS:")
            for p in out["precedents"][:5]:
                print("-", p[:200])
        else:
            print("Usage: python backend/memory.py ingest | ask <rfp text>")
    finally:
        client.close()