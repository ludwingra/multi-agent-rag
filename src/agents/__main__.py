"""Smoke test for the Orchestrator agent."""

from src.agents.orchestrator import Orchestrator


def main():
    print("Initializing Orchestrator...")
    orchestrator = Orchestrator()
    print("Orchestrator ready.\n")

    # Test queries — one per domain + one unknown
    test_queries = [
        {"query": "What is the vacation policy for new employees?", "expected_intent": "hr"},
        {"query": "How do I configure the VPN on my laptop?", "expected_intent": "tech"},
        {"query": "What is the process for submitting expense reports?", "expected_intent": "finance"},
        {"query": "What is the meaning of life?", "expected_intent": "unknown"},
    ]

    print("=" * 60)
    print("BATCH ROUTING TEST")
    print("=" * 60)

    result = orchestrator.batch_route(test_queries)

    for r in result["results"]:
        intent_match = r.get("intent_match", "N/A")
        marker = "✓" if intent_match is True else ("✗" if intent_match is False else "?")
        print(f"\n[{marker}] Query: {r['query'][:60]}...")
        print(f"    Intent: {r['intent']} (confidence: {r['confidence']:.2f})")
        print(f"    Expected: {r.get('expected_intent', 'N/A')}")
        print(f"    Agent: {r['agent']}")
        print(f"    Answer: {r['answer'][:100]}...")

    print(f"\n{'=' * 60}")
    print(f"ACCURACY: {result['correct']}/{result['evaluated']}")
    if result['accuracy'] is not None:
        print(f"Score: {result['accuracy']:.0%}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
