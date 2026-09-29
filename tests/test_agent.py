import re
import backend.agent as agent


def test_approach_keywords_are_module_level():
    assert isinstance(agent._APPROACH_KEYWORDS, dict)
    assert "security-first" in agent._APPROACH_KEYWORDS
    assert "phased rollout" in agent._APPROACH_KEYWORDS


def test_known_conflicts_returns_strings():
    result = agent._known_conflicts()
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)


def test_prompt_uses_placeholder_ids_not_real_ones():
    """
    Regression test: PROMPT's example JSON must use placeholder IDs
    (RFP-XXX, RFP-YYY, RFP-ZZZ), not real ones like RFP-011 or RFP-003.
    A real ID in the example gets cited by the model as if it were
    real evidence, even when that RFP was never actually retained.
    """
    real_ids_in_example = re.findall(r"RFP-\d{3}", agent.PROMPT)
    assert real_ids_in_example == [], (
        f"PROMPT contains real RFP ids as format examples: {real_ids_in_example}. "
        "Use placeholders like RFP-XXX instead."
    )