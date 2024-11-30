from unittest.mock import MagicMock

import grpc
import sys
import os 
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../protos'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../client'))

from ai_assistant_pb2 import WritePRDescriptionRequest, Context, SmartAutoCompleteRequest, ChatGPTForCodeRequest, ConversationContext, ConversationRequest
from ai_assistant_pb2 import WritePRDescriptionResponse, SmartAutoCompleteResponse, ChatGPTForCodeResponse, ConversationResponse
from client import AIAssistantClient

class TestAIAssistantClient:
    def test_write_pr_description(self):
        # Mock stub and response
        mock_stub = MagicMock()
        mock_stub.WritePRDescription.return_value = WritePRDescriptionResponse(
            pr_description="Mocked PR description"
        )

        # Set client stub to mock stub
        client = AIAssistantClient()
        client.stub = mock_stub

        # Testing
        response = client.write_pr_description(
            committed_changes = "test_committed_changes"
        )

        # Assertions
        mock_stub.WritePRDescription.assert_called_once()
        assert response.pr_description == "Mocked PR description"

    def test_smart_auto_complete(self):
        # Mock stub and response
        mock_stub = MagicMock()
        mock_stub.SmartAutoComplete.return_value = SmartAutoCompleteResponse(
            code_completion = "Mocked Code Completion"
        )

        # Set client stub to mock stub
        client = AIAssistantClient()
        client.stub = mock_stub

        # Testing
        response = client.smart_auto_complete(
            repo_content = "test_repo_content",
            committed_changes = "test_committed_changes",
            uncommitted_changes = "test_uncommitted_changes",
            curr_branch = "test_curr_branch",
            recent_edits = "test_recent_edits"
        )

        # Assertions
        mock_stub.SmartAutoComplete.assert_called_once()
        assert response.code_completion == "Mocked Code Completion"

    def test_chatgpt_for_code(self):
        # Mock stub and response
        mock_stub = MagicMock()
        mock_stub.ChatGPTForCode.return_value = ChatGPTForCodeResponse(
            delta = "Mocked Delta"
        )

        # Set client stub to mock stub
        client = AIAssistantClient()
        client.stub = mock_stub

        # Testing
        response = client.chatgpt_for_code(
            task_description = "test_task_description",
            committed_code = "test_committed_code",
            uncommitted_code = "test_uncommitted_code"
        )

        # Assertions
        mock_stub.ChatGPTForCode.assert_called_once()
        assert response.delta == "Mocked Delta"

    def test_virtual_pair_assistant(self, monkeypatch):
        # Mock stub and responses
        mock_stub = MagicMock()
        mock_stub.VirtualPairAssistant.return_value = iter([
            ConversationResponse(
                proposed_delta = "Mock Proposed Delta 1",
                description = "Mock Description 1"
            ),
            ConversationResponse(
                proposed_delta = "Mock Proposed Delta 2",
                description = "Mock Description 2"
            )
        ])

        # Set client stub to mock stub
        client = AIAssistantClient()
        client.stub = mock_stub

        # Mock user inputs to simulate conversation
        user_inputs = iter([
            ("test_existing_code_1", "test_stack_trace_1", "test_description_1", "F"),
            ("test_existing_code_2", "test_stack_trace_2", "test_description_2", "T")
        ])

        def mock_input(prompt):
            next_input = next(user_inputs)
            if "existing_code" in prompt:
                return next_input[0]
            elif "stack_trace" in prompt:
                return next_input[1]
            elif "description" in prompt:
                return next_input[2]
            else:
                return next_input[3]
            
        monkeypatch.setattr("builtins.input", mock_input)

        # Capture printed responses
        responses = []
        monkeypatch.setattr("builtins.print", lambda x: responses.append(x))

        # Call the function
        client.virtual_pair_assistant("initial_code", "initial_trace", "initial_description")

        # Assertions
        mock_stub.VirtualPairAssistant.assert_called_once()
        assert responses == [
            ConversationResponse(
                proposed_delta = "Mock Proposed Delta 1",
                description = "Mock Description 1"
            ),
            ConversationResponse(
                proposed_delta = "Mock Proposed Delta 2",
                description = "Mock Description 2"
            )
        ]
