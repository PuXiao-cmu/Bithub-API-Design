import grpc
import sys
import os 
import argparse
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../protos'))

from ai_assistant_pb2 import WritePRDescriptionRequest, Context, SmartAutoCompleteRequest, ChatGPTForCodeRequest, ConversationContext, ConversationRequest
import ai_assistant_pb2_grpc

class AIAssistantClient:
    def __init__(self, host='localhost', port=50051):
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = ai_assistant_pb2_grpc.AIAssistantStub(channel)

    def write_pr_description(self, committed_changes):
        response = self.stub.WritePRDescription(
            WritePRDescriptionRequest(
                committed_changes = committed_changes
            )
        )
        return response
    
    def smart_auto_complete(self, repo_content, committed_changes, uncommitted_changes, curr_branch, recent_edits):
        response = self.stub.SmartAutoComplete(
            SmartAutoCompleteRequest(
                current_context = Context(
                    repo_content = repo_content,
                    committed_changes = committed_changes,
                    uncommitted_changes = uncommitted_changes,
                    curr_branch = curr_branch
                ),
                recent_edits = recent_edits
            )
        )
        return response
    
    def chatgpt_for_code(self, task_description, committed_code, uncommitted_code):
        response = self.stub.ChatGPTForCode(
            ChatGPTForCodeRequest(
                task_description = task_description,
                committed_code = committed_code,
                uncommitted_code = uncommitted_code
            )
        )
        return response
    
    def virtual_pair_assistant_requests(self, existing_code, stack_trace, description):
        is_end = False
        # Send first request for context
        yield ConversationRequest(
            context = ConversationContext(
                existing_code = existing_code,
                stack_trace = stack_trace,
                description = description
            ),
            is_end = is_end
        )
        # Get input from user prompt contineously for conversation
        while True:
            # Sleep a bit so input prompt does not interfere with response
            time.sleep(0.5)
            existing_code = input("Enter existing_code: ")
            stack_trace = input("Enter stack_trace: ")
            description = input("Enter description: ")
            is_end_str = input("Enter is_end: ")
            if is_end_str == "True" or is_end_str == "T":
                is_end = True
            
            yield ConversationRequest(
                context = ConversationContext(
                    existing_code = existing_code,
                    stack_trace = stack_trace,
                    description = description
                ),
                is_end = is_end
            )
            if is_end == True:
                break
    
    def virtual_pair_assistant(self, existing_code, stack_trace, description):
        responses = self.stub.VirtualPairAssistant(
            self.virtual_pair_assistant_requests(
                existing_code = existing_code,
                stack_trace = stack_trace,
                description = description
            )
        )
        try:
            for response in responses:
                print(response)
        except grpc.RpcError as e:
            print(f"Stream terminated with error: {e}")

# Command-line Interface for interactive testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=50051)
    parser.add_argument("operation", type=str, 
                        choices=[
                            "write_pr_description",
                            "smart_auto_complete",
                            "chatgpt_for_code",
                            "virtual_pair_assistant"
                        ]
    )
    parser.add_argument("--committed_changes", type=str)
    parser.add_argument("--repo_content", type=str)
    parser.add_argument("--uncommitted_changes", type=str)
    parser.add_argument("--curr_branch", type=str)
    parser.add_argument("--recent_edits", type=str)
    parser.add_argument("--task_description", type=str)
    parser.add_argument("--committed_code", type=str)
    parser.add_argument("--uncommitted_code", type=str)
    parser.add_argument("--existing_code", type=str)
    parser.add_argument("--stack_trace", type=str)
    parser.add_argument("--description", type=str)

    args = parser.parse_args()
    
    client = AIAssistantClient(host=args.host, port=args.port)

    try:
        if args.operation == "write_pr_description":
            response = client.write_pr_description(
                committed_changes = args.committed_changes
            )
            print(response)

        elif args.operation == "smart_auto_complete":
            response = client.smart_auto_complete(
                repo_content = args.repo_content,
                committed_changes = args.committed_changes,
                uncommitted_changes = args.uncommitted_changes,
                curr_branch = args.curr_branch,
                recent_edits = args.recent_edits
            )
            print(response)

        elif args.operation == "chatgpt_for_code":
            response = client.chatgpt_for_code(
                task_description = args.task_description,
                committed_code = args.committed_code,
                uncommitted_code = args.uncommitted_code
            )
            print(response)

        elif args.operation == "virtual_pair_assistant":
            responses = client.virtual_pair_assistant(
                existing_code = args.existing_code,
                stack_trace = args.stack_trace,
                description = args.description
            )
    
    except grpc.RpcError as e:
        print("gRPC Error:", e.details())
