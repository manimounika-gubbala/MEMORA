from memory import client, BANK_ID

queries = [
    "What proposal strategy did we use for RFP-011 Cedar Ridge Medical Group?",
    "What proposal strategy did we use for RFP-003 Meridian Valley Health System?",
]
for q in queries:
    print("\nQ:", q)
    res = client.recall(bank_id=BANK_ID, query=q)
    for m in res.results[:8]:
        print("-", m.text[:300])
client.close()