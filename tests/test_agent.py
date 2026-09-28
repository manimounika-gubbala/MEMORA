import backend.agent as agent


def test_approach_keywords_are_module_level():
    assert isinstance(agent._APPROACH_KEYWORDS, dict)
    assert "security-first" in agent._APPROACH_KEYWORDS
    assert "phased rollout" in agent._APPROACH_KEYWORDS


def test_known_conflicts_returns_strings():
    result = agent._known_conflicts()
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
