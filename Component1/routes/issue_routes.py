from flask import Blueprint, jsonify, request
from models import db, Issue, Comment, Repository

issue_bp = Blueprint('issue', __name__)

# 9. List repository issues
@issue_bp.route('/repositories/<int:id>/issues', methods=['GET'])
def list_repository_issues(id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404

    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 5))

    query = Issue.query.filter_by(repository_id=id)
    if status:
        query = query.filter_by(status=status)

    paginated_issues = query.paginate(page=page, per_page=size, error_out=False).items
    return jsonify([
        {
            "id": issue.id,
            "title": issue.title,
            "status": issue.status,
            "submitter_id": issue.submitter_id
        }
        for issue in paginated_issues
    ]), 200



# 10. View a specific issue details
@issue_bp.route('/repositories/<int:id>/issues/<int:issue_id>', methods=['GET'])
def view_issue_details(id, issue_id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404
    issue = Issue.query.filter_by(repository_id=id, id=issue_id).first()
    if not issue:
        return jsonify({"message": "Issue not found"}), 404
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 5))

    paginated_comments = Comment.query.filter_by(id=issue.id).order_by(Comment.created_at).paginate(page=page, per_page=size, error_out=False).items

    return jsonify({
        "id": issue.id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status,
        "submitter_id": issue.submitter_id,
        "submission_date": issue.created_at.isoformat(),
        "comments": [
            {"id": comment.id, "content": comment.content}
            for comment in paginated_comments
        ]
    }), 200


# 11. Report a new issue
@issue_bp.route('/repositories/<int:id>/issues', methods=['POST'])
def report_new_issue(id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404

    data = request.get_json()
    if not data or 'description' not in data or 'submitter_id' not in data:
        return jsonify({"message": "Invalid input: no issue description or submitter_id"}), 400

    issue = Issue(
        repository_id=id,
        title=data.get('title', 'Untitled Issue'),
        description=data['description'],
        status='Open',
        submitter_id=int(data['submitter_id'])
    )
    db.session.add(issue)
    db.session.commit()

    return jsonify({"id": issue.id, "message": "Issue created successfully"}), 201


# 12. Paginate comments for an issue
@issue_bp.route('/repositories/<int:id>/issues/<int:issue_id>/comments', methods=['GET'])
def paginate_issue_comments(id, issue_id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404
    issue = Issue.query.filter_by(repository_id=id, id=issue_id).first()
    if not issue:
        return jsonify({"message": "Issue not found"}), 404

    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 5))
    except ValueError:
        return jsonify({"message": "Page and size must be integers"}), 400

    if page <= 0 or size <= 0:
        return jsonify({"message": "Page and size must be positive integers"}), 400

    paginated_comments = Comment.query.filter_by(issue_id=issue.id).order_by(Comment.created_at).paginate(page=page, per_page=size, error_out=False).items

    return jsonify([
        {"id": comment.id, "content": comment.content}
        for comment in paginated_comments
    ]), 200


# 13. Submit a new comment
@issue_bp.route('/repositories/<int:id>/issues/<int:issue_id>/comments', methods=['POST'])
def submit_new_comment(id, issue_id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404

    issue = Issue.query.filter_by(repository_id=id, id=issue_id).first()
    if not issue:
        return jsonify({"message": "Issue not found"}), 404

    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"message": "Invalid input, no commit content"}), 400

    comment = Comment(
        issue_id=issue_id,
        content=data['content']
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({"id": comment.id, "message": "Comment added successfully"}), 201
