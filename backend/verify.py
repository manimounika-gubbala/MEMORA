from memory import client, BANK_ID

QUERIES = [
    "Why did we lose a healthcare deal?",
    "Which deals did we win and what made the difference?",
    "What does Northbridge Mutual Insurance care about?",
]

for q in QUERIES:
    print(f"\nQ: {q}\n" + "-" * 40)

    result = client.recall(
        bank_id=BANK_ID,
        query=q
    )

    for m in result.results[:4]:
        print("-", m.text[:200])

client.close()