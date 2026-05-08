from unittest.mock import MagicMock, patch

from ai.llm.router import ask


class TestRouter:
    @patch("ai.llm.router.litellm")
    def test_ask_returns_text(self, mock_litellm):
        mock_msg = MagicMock()
        mock_msg.content = "Hello world"
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=mock_msg)]
        mock_litellm.completion.return_value = mock_resp

        result = ask("test prompt", system="you are helpful")
        assert result == "Hello world"
        mock_litellm.completion.assert_called_once()
        call_kwargs = mock_litellm.completion.call_args
        assert call_kwargs.kwargs["model"] == "gpt-4o-mini"
        assert len(call_kwargs.kwargs["messages"]) == 2

    @patch("ai.llm.router.litellm")
    def test_ask_custom_model(self, mock_litellm):
        mock_msg = MagicMock()
        mock_msg.content = "response"
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=mock_msg)]
        mock_litellm.completion.return_value = mock_resp

        ask("test", model="claude-3-haiku-20240307")
        call_kwargs = mock_litellm.completion.call_args
        assert call_kwargs.kwargs["model"] == "claude-3-haiku-20240307"
