import pytest
from auto_orchestrator.decomposer import PromptDecomposer

def test_decomposes_conjoined_prompt():
    tasks = PromptDecomposer().decompose("Research AI and summarize findings")
    assert len(tasks) == 2
    assert tasks[1].depends_on == ("task-1",)

def test_rejects_empty_prompt():
    with pytest.raises(ValueError):
        PromptDecomposer().decompose("  ")
