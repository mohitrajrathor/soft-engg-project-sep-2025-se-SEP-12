"""
Unit tests for Doubt Summarizer Service.
Tests initialization, empty states, and LLM interaction without calling real APIs.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.doubt_summarizer_service import doubt_summarizer_service

# Sample Mock Data (What we pretend the AI returns)
MOCK_LLM_RESPONSE = {
    "course_code": "CS101",
    "overall_summary": "Students are struggling with recursion.",
    "topics": [
        {
            "label": "Recursion",
            "trend": "Increasing",
            "count": 5,
            "sample_questions": ["What is a base case?"]
        }
    ],
    "learning_gaps": [],
    "insights": ["Review base cases."]
}

@pytest.mark.unit
class TestDoubtSummarizerService:
    """Tests for the Doubt Summarizer Service logic."""

    @pytest.mark.asyncio
    async def test_generate_summary_empty_input(self):
        """Test that empty input list returns empty state immediately."""
        # FIX: Swapped args ([], "CS101") and updated function name
        result = await doubt_summarizer_service.generate_summary_topics_insights([], "CS101")
        
        # Assertions
        assert result["course_code"] == "CS101"
        assert result["overall_summary"] == "No data."
        assert len(result["topics"]) == 0

    @pytest.mark.asyncio
    async def test_generate_summary_missing_llm(self):
        """Test graceful failure if LLM is not configured."""
        # 1. Temporarily remove the LLM from the service
        original_llm = doubt_summarizer_service.llm
        doubt_summarizer_service.llm = None
        
        # 2. Call service (FIX: Updated name and arg order)
        result = await doubt_summarizer_service.generate_summary_topics_insights(["Help me"], "CS101")
        
        # 3. Restore LLM (Cleanup)
        doubt_summarizer_service.llm = original_llm

        # Assertions
        assert "LLM not configured" in result.get("error", "")

    @pytest.mark.asyncio
    async def test_generate_summary_success_mocked(self):
        """
        Test a successful run by MOCKING the chain execution.
        """
        # Mock the entire chain execution flow
        with patch("app.services.doubt_summarizer_service.PromptTemplate") as mock_prompt:
            # When the service calls chain.ainvoke, we return MOCK_LLM_RESPONSE
            mock_chain_instance = AsyncMock()
            mock_chain_instance.ainvoke.return_value = MOCK_LLM_RESPONSE
            
            # This magic line makes the pipe operator (|) return our mock_chain_instance
            mock_prompt.return_value.__or__.return_value.__or__.return_value = mock_chain_instance

            # Run the Service (FIX: Updated name and arg order)
            doubts = ["What is recursion?", "Help with loops"]
            result = await doubt_summarizer_service.generate_summary_topics_insights(doubts, "CS101")

            # Assertions
            assert result["course_code"] == "CS101"
            assert result["overall_summary"] == "Students are struggling with recursion."
            assert len(result["topics"]) == 1
            assert result["topics"][0]["label"] == "Recursion"

    @pytest.mark.asyncio
    async def test_error_handling_during_analysis(self):
        """Test that exceptions during AI processing are caught gracefully."""
        
        # Force an error by creating a mock chain that raises an exception
        with patch("app.services.doubt_summarizer_service.PromptTemplate") as mock_prompt:
            mock_chain_instance = AsyncMock()
            mock_chain_instance.ainvoke.side_effect = Exception("Google AI is down")
            
            # Setup the pipe chain mock
            mock_prompt.return_value.__or__.return_value.__or__.return_value = mock_chain_instance

            # Run Service (FIX: Updated name and arg order)
            result = await doubt_summarizer_service.generate_summary_topics_insights(["test"], "CS101")

            # Should return an error dict
            assert "Google AI is down" in result.get("error", "")