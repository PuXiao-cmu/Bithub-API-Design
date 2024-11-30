from concurrent import futures
import logging

import argparse

import grpc
import sys
import os 
import random

random.seed(7684)

sys.path.append(os.path.join(os.path.dirname(__file__), '../protos'))

from ai_assistant_pb2 import WritePRDescriptionResponse, Context, SmartAutoCompleteResponse, ChatGPTForCodeResponse, ConversationContext, ConversationResponse
from ai_assistant_pb2_grpc import AIAssistantServicer
import ai_assistant_pb2_grpc

# Generatates a random int from the string in a deterministic manner
def generate_random_int_from_str(my_str, min_val, max_val):
    hash_value = hash(my_str)
    random.seed(hash_value)
    return random.randint(min_val, max_val)

class AIAssistantServer(AIAssistantServicer):
    def WritePRDescription(self, request, context):
        predefined_responses = [
            WritePRDescriptionResponse(
                pr_description = "Good PR Descrption"
            ),
            WritePRDescriptionResponse(
                pr_description = "Great PR Descrption"
            ),
            WritePRDescriptionResponse(
                pr_description = "Best PR Descrption"
            )
        ]
        # Use committed code to determine which response to give
        chosen_response = predefined_responses[generate_random_int_from_str(request.committed_changes, 0, 2)]
        return chosen_response
    
    def SmartAutoComplete(self, request, context):
        predefined_responses = [
            # code_completion == "" means there is no plausible completion for the current piece of code
            SmartAutoCompleteResponse(
                code_completion = ""
            ),
            SmartAutoCompleteResponse(
                code_completion = "completion1"
            ),
            SmartAutoCompleteResponse(
                code_completion = "completion2"
            )
        ]
        # Use context and recent edits to determine which response to give
        concat_str = request.current_context.repo_content + request.current_context.committed_changes + request.current_context.uncommitted_changes + request.current_context.curr_branch + request.recent_edits
        chosen_response = predefined_responses[generate_random_int_from_str(concat_str, 0, 2)]
        return chosen_response
    
    def ChatGPTForCode(self, request, context):
        predefined_responses = [
            ChatGPTForCodeResponse(
                clarification_request = "Description not clear"
            ),
            ChatGPTForCodeResponse(
                clarification_request = "Missing important details"
            ),
            ChatGPTForCodeResponse(
                delta = "delta1"
            ),
            ChatGPTForCodeResponse(
                delta = "delta2"
            ),
        ]
        # Use description, committed and uncommitted code to determine response
        concat_str = request.task_description + request.committed_code + request.uncommitted_code
        chosen_response = predefined_responses[generate_random_int_from_str(concat_str, 0, 3)]
        return chosen_response
    
    def VirtualPairAssistant(self, request_iterator, context):
        predefined_responses = [
            ConversationResponse(
                proposed_delta = "proposed delta 1",
                description = "description 1"
            ),
            ConversationResponse(
                proposed_delta = "proposed delta 2",
                description = "description 2"
            ),
            ConversationResponse(
                proposed_delta = "proposed delta 3",
                description = "description 3"
            )
        ]
        # Since this is a conversation, the ai must take account previous
        # requests when forming a response
        previous_context = ""
        for request in request_iterator:
            # If end reached, terminate this service
            if request.is_end == True:
                break
            # Use provided context and previous context to determine response
            concat_str = previous_context + request.context.existing_code + request.context.stack_trace + request.context.description
            chosen_response = predefined_responses[generate_random_int_from_str(concat_str, 0, 2)]
            previous_context = concat_str
            yield chosen_response


def serve(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ai_assistant_pb2_grpc.add_AIAssistantServicer_to_server(AIAssistantServer(), server)
    server_address = f"{host}:{port}"
    server.add_insecure_port(server_address)
    server.start()
    print("Server started, listening on " + server_address)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=50051)
    
    args = parser.parse_args()
    serve(args.host, args.port)

