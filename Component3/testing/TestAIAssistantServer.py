import grpc
import sys
import os 
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../protos'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../server'))

from ai_assistant_pb2 import WritePRDescriptionRequest, Context, SmartAutoCompleteRequest, ChatGPTForCodeRequest, ConversationContext, ConversationRequest
from ai_assistant_pb2 import WritePRDescriptionResponse, SmartAutoCompleteResponse, ChatGPTForCodeResponse, ConversationResponse
from server import AIAssistantServer

# Mocking the grpc context
class MockContext:
    def cancel(self):
        pass
    def code(self):
        return grpc.StatusCode.OK
    def details(self):
        return "Mocked Details"
    def trailing_metadata(self):
        return []

# Mock input generator to always return 0 for deterministic results
@pytest.fixture
def mock_random():
    def mock_generate_random_int_from_str(my_str, min_val, max_val):
        return 0  
    return mock_generate_random_int_from_str

class TestAIAssistantServer:
    def testWritePRDescription(self, monkeypatch, mock_random):
        server = AIAssistantServer()

        request = WritePRDescriptionRequest(
            committed_changes = "test_committed_changes"
        )

        monkeypatch.setattr("server.generate_random_int_from_str", mock_random)

        response = server.WritePRDescription(request, MockContext())
        assert response.pr_description == "Good PR Descrption"

    def testSmartAutoComplete(self, monkeypatch, mock_random):
        server = AIAssistantServer()

        request = SmartAutoCompleteRequest(
            current_context = Context(
                repo_content = "test_repo_content",
                committed_changes = "test_committed_changes",
                uncommitted_changes = "test_uncommitted_changes",
                curr_branch = "test_curr_branch"
            ),
            recent_edits="test_recent_edits"
        )

        monkeypatch.setattr("server.generate_random_int_from_str", mock_random)

        response = server.SmartAutoComplete(request, MockContext())
        assert response.code_completion == ""

    def testChatGPTForCode(self, monkeypatch, mock_random):
        server = AIAssistantServer()

        request = ChatGPTForCodeRequest(
            task_description = "test_task_description",
            committed_code = "test_committed_code",
            uncommitted_code = "test_uncommitted_code"
        )

        monkeypatch.setattr("server.generate_random_int_from_str", mock_random)

        response = server.ChatGPTForCode(request, MockContext())
        assert response.clarification_request == "Description not clear"

    def testVirtualPairAssistant(self, monkeypatch, mock_random):
        server = AIAssistantServer()

        request_1 = ConversationRequest(
            context = ConversationContext(
                existing_code = "test_existing_code",
                stack_trace = "test_stack_trace",
                description = "test_description"
            ),
            is_end=False
        )

        request_2 = ConversationRequest(
            is_end=True
        )

        monkeypatch.setattr("server.generate_random_int_from_str", mock_random)

        # Simulate a stream of requests
        responses = list(server.VirtualPairAssistant(iter([request_1, request_2]), MockContext()))
        
        # Only one response because the second closes the conversation
        assert len(responses) == 1
        assert responses[0].proposed_delta == "proposed delta 1"


