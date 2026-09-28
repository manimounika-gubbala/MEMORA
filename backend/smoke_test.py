import os
import time
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

BANK_ID = "memora"


def test_memory():
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="MEMORA Proposal Intelligence",
            reflect_mission="I am a proposal strategist. I learn from past RFP wins and losses.",
        )
        print("Bank created.")
    except Exception as e:
        print(f"Bank create skipped ({e})")

    client.retain(
        bank_id=BANK_ID,
        content=(
            "RFP-011 healthcare, mid-market: our security-first proposal lost "
            "because the 7-month plan missed the client's hard go-live date."
        ),
        context="rfp outcome",
        timestamp="2026-03-10T00:00:00Z",
    )

    query = "Why did we lose a healthcare deal?"
    for attempt in range(6):
        result = client.recall(bank_id=BANK_ID, query=query)
        if result.results:
            break
        print(f"No memories yet, retrying ({attempt + 1}/6)...")
        time.sleep(5)

    print("\nMEMORA MEMORY TEST\n------------------")
    for memory in result.results:
        print("-", memory.text)


if __name__ == "__main__":
    test_memory()