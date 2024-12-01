import pytest
from app import create_app
from models import db, Repository, Branch, Tag, Commit
from datetime import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        # Add test data
        repository = Repository(name="Test Repo", description="A test repository", author_id=1)
        branch_main = Branch(name="main", repository_id=1)
        branch_feature = Branch(name="feature", repository_id=1)
        tag = Tag(name="v1.0", commit_id=1)
        commit = Commit(
            hash="abc123",
            message="Initial commit",
            branch_id=1,
            tree_structure={"children": {"file1.txt": {}, "subdir": {"children": {}}}},
        )
        db.session.add_all([repository, branch_main, branch_feature, tag, commit])
        db.session.commit()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()


# Test: 1. Get repository default view
def test_get_repository_default_view_happy_path(client):
    response = client.get("/repositories/1")
    assert response.status_code == 200
    data = response.get_json()

    assert "repository" in response.json
    assert data["repository"]["id"]==1
    assert data["repository"]["name"]=="Test Repo"
    assert "main_branch" in response.json
    assert data["main_branch"]["id"]==1
    assert data["main_branch"]["name"]=="main"
    assert "latest_commit" in response.json
    assert data["latest_commit"]["id"]==1
    assert data["latest_commit"]["hash"]=="abc123"

# Test: 1. Get repository default view - Error: Repository not found
def test_get_repository_default_view_error(client):
    response = client.get("/repositories/99")
    assert response.status_code == 404
    assert response.json["message"] == "Repository_id Error. Repository not found"


# Test: 2. List all branches
def test_list_all_branches_happy_path(client):
    response = client.get("/repositories/1/branches")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["branch id"]==1
    assert data[0]["branch name"]=="main"
    assert data[1]["branch id"]==2
    assert data[1]["branch name"]=="feature"

# Test: 2. List all branches - Error: Invalid Repository id
def test_list_all_branches_error(client):
    response = client.get("/repositories/99/branches")
    assert response.status_code == 404
    assert response.json["message"] == "Repository not found"


# Test: 3. List all tags
def test_list_all_tags_happy_path(client):
    response = client.get("/repositories/1/tags")
    assert response.status_code == 200
    data=response.get_json()
    assert len(data) == 1
    assert data[0]["tag id"]==1
    assert data[0]["tag name"]=="v1.0"

# Test: 3. List all tags - Error: Invalid Repository id
def test_list_all_tags_error(client):
    response = client.get("/repositories/99/tags")
    assert response.status_code == 404
    assert response.json["message"] == "Repository not found"


# Test: 4. List all commits in a selected branch
def test_list_all_commits_happy_path(client):
    response = client.get("/repositories/1/branches/main/commits")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["commit id"] == 1
    assert data[0]["hash"] == "abc123"
    assert data[0]["message"] == "Initial commit"

# Test: 4. List all commits in a selected branch - Error: Invalid branch id
def test_list_all_commits_error(client):
    response = client.get("/repositories/1/branches/unknown/commits")
    assert response.status_code == 404
    assert response.json["message"] == "Repository or branch not found"

# Test: 5. Get top-level tree in a commit
def test_get_top_level_tree_happy_path(client):
    response = client.get("/repositories/1/branches/main/commits/abc123/tree")
    assert response.status_code == 200
    data = response.get_json()
    assert "tree" in data
    assert "children" in data["tree"]
    assert "file1.txt" in data["tree"]["children"]
    assert "subdir" in data["tree"]["children"]

# Test: 5. Get top-level tree in a commit - Error: invalid commit hash
def test_get_top_level_tree_error(client):
    response = client.get("/repositories/1/branches/main/commits/unknown/tree")
    assert response.status_code == 404
    assert response.json["message"] == "Repository, branch, or commit not found"


# Test: 6. View file or sub-tree
def test_view_file_or_subtree_happy_path(client):
    response = client.get("/repositories/1/branches/main/commits/abc123/tree/subdir")
    assert response.status_code == 200
    data = response.get_json()
    assert "children" in data
    assert data["children"] == {}

# Test: 6. View file or sub-tree - Error: invalid file path
def test_view_file_or_subtree_error(client):
    response = client.get("/repositories/1/branches/main/commits/abc123/tree/unknown")
    assert response.status_code == 404
    assert response.json["message"] == "File or directory not found"
