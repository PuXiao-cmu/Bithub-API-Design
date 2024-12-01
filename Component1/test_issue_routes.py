import pytest
from app import create_app
from models import db, Repository, Issue, Comment
from datetime import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

        # add test data
        repository = Repository( name='Test Repo', description='A test repository', author_id=1)
        db.session.add(repository)
        issue_open = Issue( repository_id=1, title='Open Issue', description='An open issue', status='Open', submitter_id=1)
        issue_closed = Issue(repository_id=1, title='Closed Issue', description='A closed issue', status='Closed', submitter_id=2)
        db.session.add(issue_open)
        db.session.add(issue_closed)
        comment = Comment(issue_id=1, content='Test comment for issue 1')
        db.session.add(comment)
        db.session.commit()

    yield app.test_client()
    with app.app_context():
        db.session.remove()
        db.drop_all()


# Test: 7 List repository issues
def test_list_repository_issues_happy_path(client):
    response = client.get('/repositories/1/issues')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['title'] == 'Open Issue'
    assert data[0]['status'] == 'Open'
    assert data[0]['submitter_id'] == 1
    assert data[1]['title'] == 'Closed Issue'
    assert data[1]['status'] == 'Closed'
    assert data[1]['submitter_id'] == 2

# Test: 7 List repository issues - filter status
def test_list_repository_issues_filter_by_status_open(client):
    response = client.get('/repositories/1/issues?status=Open')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Open Issue'
    assert data[0]['status'] == 'Open'
    assert data[0]['submitter_id'] == 1

# Test: 7 List repository issues - Error: repository not found
def test_list_repository_issues_repository_not_found(client):
    response = client.get('/repositories/99/issues')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Repository not found'

# Test: 8 View a specific issue details
# shows the issue description and its data (submission date, submitter ID, status, etc), and one page of comments.
def test_view_issue_details_happy_path(client):
    response = client.get('/repositories/1/issues/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Open Issue'
    assert data['description'] == 'An open issue'
    assert data['status'] == 'Open'
    assert data['submitter_id'] == 1
    assert len(data['comments']) == 1
    assert data['comments'][0]['content'] == 'Test comment for issue 1'

    # Check submission_date
    submission_date = data['submission_date']
    parsed_date = datetime.fromisoformat(submission_date)
    assert parsed_date.year == datetime.now().year
    assert parsed_date.month == datetime.now().month
    assert parsed_date.day == datetime.now().day

# Test: 8 View a specific issue detai - Error: Issue not found
def test_view_issue_details_issue_not_found(client):
    response = client.get('/repositories/1/issues/99')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Issue not found'

# Test: 9 Report a new issue
def test_report_new_issue_happy_path(client):
    response = client.post('/repositories/1/issues', json={
        'title': 'New Issue',
        'description': 'New issue description',
        'submitter_id': 2
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Issue created successfully'

    response = client.get('/repositories/1/issues')
    issues = response.get_json()
    assert len(issues) == 3  # database have 2 issues before
    assert issues[2]['title'] == 'New Issue'
    assert issues[2]['status'] == 'Open'

# Test: 9 Report a new issue - Error: 
def test_report_new_issue_repository_not_found(client):
    response = client.post('/repositories/99/issues', json={
        'description': 'Report to invalid repo'
    })
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Repository not found'

# Test: 10 Paginate comments for an issue
def test_paginate_issue_comments_happy_path(client):
    response = client.get('/repositories/1/issues/1/comments?page=1&size=1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['content'] == 'Test comment for issue 1'

# Test: 10 Paginate comments for an issue - Error: page is negative number
def test_paginate_issue_comments_page_negative(client):
    response = client.get('/repositories/1/issues/1/comments?page=-1&size=1')
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Page and size must be positive integers'

# Test: 11 Submit a new comment
def test_submit_new_comment_happy_path(client):
    response = client.post('/repositories/1/issues/1/comments', json={
        'content': 'Another comment'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Comment added successfully'

    response = client.get('/repositories/1/issues/1/comments')
    data = response.get_json()
    assert len(data) == 2  # 应该有两个评论

# Test: 11 Submit a new comment - Error: no commit content
def test_submit_new_comment_invalid_input(client):
    response = client.post('/repositories/1/issues/1/comments', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Invalid input, no commit content'
