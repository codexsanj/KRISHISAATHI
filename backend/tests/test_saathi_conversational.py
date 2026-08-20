import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

PART_21_QUESTIONS = [
    "How much water does wheat need?",
    "Why are my tomato leaves turning yellow?",
    "What fertilizer is good for ragi?",
    "What is NPK?",
    "What is crop rotation?",
    "How can I improve soil fertility?",
    "Which crop is suitable for black soil?",
    "When should I sow maize?",
    "Why is my crop growing slowly?",
    "How can I control pests?",
    "What causes fungal diseases?",
    "What happens if there is no rain for 10 days?",
    "What if rainfall decreases by 20%?",
    "What if I reduce irrigation by 20%?",
    "What if fertilizer price increases by 10%?",
    "What if I grow maize instead of wheat?",
    "Which mandi has the best price?",
    "Should I sell my crop today?",
    "What government agricultural schemes are available?",
    "What should I do today?",
    "Why is my crop at risk?",
    "Should I irrigate today?",
    "Check my crop health.",
    "How much land do I need for maize?",
    "How can I increase my yield?",
    "My wheat leaves are yellow. What should I do?"
]

def test_all_part_21_questions():
    """Verify that Saathi successfully processes every single free-form question in Part 21."""
    for q in PART_21_QUESTIONS:
        res = client.post("/api/chat", json={"message": q})
        assert res.status_code == 200, f"Failed on question: '{q}'"
        data = res.json()
        assert "answer" in data or "message" in data, f"No answer returned for: '{q}'"
        answer = data.get("answer") or data.get("message")
        assert len(answer) > 10, f"Answer too short for question: '{q}'"
        print(f"\n[Q]: {q}\n[A]: {answer[:100]}...\n")

def test_multi_turn_follow_up():
    """Verify multi-turn follow-up context resolution."""
    # Turn 1
    r1 = client.post("/api/chat", json={"message": "My wheat leaves are yellow."})
    assert r1.status_code == 200

    # Turn 2
    r2 = client.post("/api/chat", json={"message": "Why?"})
    assert r2.status_code == 200
    a2 = r2.json().get("answer") or r2.json().get("message")
    assert "yellow" in a2.lower() or "wheat" in a2.lower() or "causes" in a2.lower()

    # Turn 3
    r3 = client.post("/api/chat", json={"message": "What should I do next?"})
    assert r3.status_code == 200
    a3 = r3.json().get("answer") or r3.json().get("message")
    assert len(a3) > 10
