import os
import json
import time
import re
from dotenv import load_dotenv
from groq import Groq
from memory import client, BANK_ID

load_dotenv()

llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

from pathlib import Path

_RFPS = json.loads(
    (Path(__file__).parent.parent / "data" / "past_rfps.json").read_text(encoding="utf-8")
)
_CLIENT_TO_ID = {r["client_name"]: r["rfp_id"] for r in _RFPS}


_APPROACH_KEYWORDS = {
    "security-first": ["security-first", "security first"],
    "phased rollout": ["phased", "phase one", "three-phase", "three-wave"],
    "24/7 support bundled": ["24/7 support"],
    "premium pricing / roi": ["premium tier", "roi model"],
    "lean core package": ["lean core", "lean-core"],
}

_KNOWN_RESOLUTIONS = {
    "security-first": "RFP-019",
}


def _label(text: str) -> str:
    """Prefix a recalled memory with the bid it is about, or say we can't tell."""
    low = text.lower()

    for name, rid in _CLIENT_TO_ID.items():
        if name.lower() in low:
            return f"[{rid}] {text}"

    ids = sorted(set(re.findall(r"RFP-\d{3}", text)))
    if ids:
        return f"[mentions {', '.join(ids)}] {text}"

    return f"[unattributed] {text}"


def _known_conflicts() -> list[str]:
    """Find approach tags that won at least one bid and lost at least one
    other, straight from past_rfps.json. This does not depend on how
    Hindsight rewrites or attributes text."""
    by_tag: dict[str, list[dict]] = {}
    for r in _RFPS:
        strat = r.get("proposal_strategy", "").lower()
        for tag, needles in _APPROACH_KEYWORDS.items():
            if any(n in strat for n in needles):
                by_tag.setdefault(tag, []).append(r)

    lines = []
    for tag, records in by_tag.items():
        won = [r for r in records if r["outcome"].lower() == "won"]
        lost = [r for r in records if r["outcome"].lower() == "lost"]
        if won and lost:
            w, l = won[0], lost[0]
            
            lines.append(
                
                f"Approach '{tag}' WON {w['rfp_id']} ({w['client_name']}) "
                f"but LOST {l['rfp_id']} ({l['client_name']}): "
                f"win reason - {w['client_reason']}; loss reason - {l['client_reason']}."
            )
            if tag in _KNOWN_RESOLUTIONS:
                res_id = _KNOWN_RESOLUTIONS[tag]
                res = next((x for x in _RFPS if x["rfp_id"] == res_id), None)
                if res:
                    lines.append(
                        f"RESOLVED BY {res['rfp_id']} ({res['client_name']}): "
                        f"WON using '{tag}' delivered as {res['proposal_strategy']} "
                        f"- reason: {res['client_reason']}."
                    )
    return lines


def gather_context(rfp: dict, per_query: int = 8) -> list[str]:
    industry = rfp.get("industry", "")
    client_name = rfp.get("client_name", "")
    queries = [
        f"Why did we lose {industry} deals?",
        f"Which {industry} proposals did we win and why did the client choose us?",
        f"What does {client_name} care about and what concerns did they raise?",
        f"Timeline or deadline problems in past proposals: {rfp.get('rfp_summary', '')[:200]}",
        f"What proposal strategies did we use in {industry} bids, and what was the outcome of each?",
    ]

    seen, out = set(), []
    for q in queries:
        res = client.recall(bank_id=BANK_ID, query=q)
        for m in res.results[:per_query]:
            if m.text not in seen:
                seen.add(m.text)
                out.append(_label(m.text))
    return out


PROMPT = """You are a bid strategist reviewing a NEW RFP before anyone writes a response.
Use ONLY the past-bid memories below as evidence. Cite the RFP id (like RFP-011)
for every claim. If no memory supports a point, do not make it up.Each memory starts with a tag such as [RFP-003] naming the bid it is about.
Cite an RFP id only from that tag. Never cite memories tagged [unattributed] or
[mentions ...] as evidence for a specific bid. Never list the same RFP as both
for and against the same claim.

If two past bids point in opposite directions (same approach, different outcome),
say so explicitly and explain what differed.

NEW RFP:
{rfp}

PAST MEMORIES:KNOWN CONTESTED APPROACHES (verified from our records; use these real ids directly
and explain the deciding factor in your own words). Some entries include a line
starting with "RESOLVED BY" naming a later bid that reconciled the contradiction —
when present, use it to explain HOW the approach was adapted to win, not just that
the two bids disagreed:
{known_conflicts}
{memories}

Return ONLY JSON in this shape:
{{
  "risks": [
    {{"risk": "...", "evidence": ["RFP-011"], "why_it_matters": "...", "mitigation": "..."}}
  ],
  "conflicts": [
      {{"claim": "...", "evidence_for": ["RFP-003"], "evidence_against": ["RFP-011"], 
"deciding_factor": "...", "resolution": "RFP-019 or null if unresolved"}}
    ]
}}
"""

_CHAR_FIXES = {
    "\u2011": "-", "\u2010": "-", "\u2013": "-",
    "\u2014": " - ",
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u00a0": " ",
}

def _clean_obj(x):
    """Normalize typographic characters in every string of a parsed result."""
    if isinstance(x, str):
        for bad, good in _CHAR_FIXES.items():
            x = x.replace(bad, good)
        return x
    if isinstance(x, list):
        return [_clean_obj(i) for i in x]
    if isinstance(x, dict):
        return {k: _clean_obj(v) for k, v in x.items()}
    return x

def _ask_llm(prompt: str, retries: int = 3) -> dict:
    last = None
    for attempt in range(retries):
        try:
            r = llm.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            text = r.choices[0].message.content.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            last = e
            time.sleep(2)
    return {"risks": [], "conflicts": [], "error": str(last)}

def _ids(text: str) -> set[str]:
    return set(re.findall(r"RFP-\d{3}", text))

def premortem(rfp: dict) -> dict:
    memories = gather_context(rfp)
    if not memories:
        return {"risks": [], "conflicts": [], "note": "No relevant memory yet."}
    prompt = PROMPT.format(
        rfp=json.dumps(rfp, indent=2),
        known_conflicts="\n".join(_known_conflicts()) or "(none found)",
        memories="\n".join(f"- {m}" for m in memories),
    )
    result = _ask_llm(prompt)
    real = _ids(" ".join(memories))
    cited = _ids(
        json.dumps(result.get("risks", []))
        + json.dumps(result.get("conflicts", []))
    ) 

    result["ids_in_memory"] = sorted(real)
    result["invented_ids"] = sorted(cited - real)
    result["memories_used"] = memories

    return _clean_obj(result)

def record_outcome(rfp: dict, outcome: str, reason: str) -> None:
    """Write the result of a bid back into memory so the next pre-mortem is smarter."""
    text = (
        f"{outcome.capitalize()} {rfp['rfp_id']} for {rfp['client_name']} "
        f"({rfp['industry']}) because {reason}."
    )
    client.retain(
        bank_id=BANK_ID,
        content=text,
        document_id=f"{rfp['rfp_id']}-outcome",
    )


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    new_rfp = {
        "rfp_id": "RFP-NEW-1",
        "client_name": "Lakeview Clinics",
        "industry": "Healthcare",
        "company_size": "Mid-market",
        "rfp_summary": "Patient intake and billing platform, hard go-live in 90 days.",
    }
    result = premortem(new_rfp)
    print("ERROR:", result.get("error"))
    print("INVENTED IDS:", result.get("invented_ids"))
    print("RISK EVIDENCE:", [r.get("evidence") for r in result.get("risks", [])])
    print("CONFLICTS:", [(c.get("evidence_for"), c.get("evidence_against")) for c in result.get("conflicts", [])])
    print("-----")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    client.close()