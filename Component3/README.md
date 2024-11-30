# api-design-final-project-team-15
api-design-final-project-team-15 created by GitHub Classroom

## Enter venv (Mac)
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Compile grpc code
```bash
python -m grpc_tools.protoc -I=protos/ --python_out=protos/ --grpc_python_out=protos/ protos/ai_assistant.proto
```

## Start the server
```bash
python server/server.py
```

## Manual Testing Commands
```bash
python client/client.py write_pr_description --committed_changes abcd
python client/client.py smart_auto_complete --repo_content repo --committed_changes abcd --uncommitted_changes def --curr_branch myBranch --recent_edits myEdit
python client/client.py chatgpt_for_code --task_description taskDescription --committed_code abc --uncommitted_code def
python client/client.py virtual_pair_assistant --existing_code myCode --stack_trace myTrace --description myDescription
```

## Execute test
```bash
pytest -p no:warnings testing/TestAIAssistantClient.py
pytest -p no:warnings testing/TestAIAssistantServer.py
```
