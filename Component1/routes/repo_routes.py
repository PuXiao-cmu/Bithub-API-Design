from flask import Blueprint, jsonify, request
from models import db, Repository, Branch, Tag, Commit

repo_bp = Blueprint('repository', __name__)

# 1. Get repository default view (the latest commit on the main branch.)
@repo_bp.route('/repositories/<int:id>', methods=['GET'])
def get_repository_default(id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository_id Error. Repository not found"}), 404
    main_branch = Branch.query.filter_by(repository_id=id, name='main').one_or_none()
    if not main_branch:
        return jsonify({"message": "Main branch not found in the repository"}), 404
    latest_commit = Commit.query.filter_by(branch_id=main_branch.id).order_by(Commit.created_at.desc()).first()
    if not latest_commit:
        return jsonify({"message": "No commits found on the main branch"}), 404

    return jsonify({
        "repository": {
            "id": repository.id,
            "name": repository.name,
            "description": repository.description,
            "author_id": repository.author_id
        },
        "main_branch": {
            "id": main_branch.id,
            "name": main_branch.name
        },
        "latest_commit": {
            "id": latest_commit.id,
            "hash": latest_commit.hash,
            "message": latest_commit.message,
            "created_at": latest_commit.created_at.isoformat(sep=' ', timespec='seconds') 
        }
    }), 200

# 2. Navigate to commits in the main branch
@repo_bp.route('/repositories/<int:id>/branches/main/commits', methods=['GET'])
def navigate_to_commits_in_main_branch(id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404
    main_branch = Branch.query.filter_by(repository_id=id, name='main').one_or_none()
    if not main_branch:
        return jsonify({"message": "Main branch not found"}), 404

    commits = Commit.query.filter_by(branch_id=main_branch.id).all()
    return jsonify([
        {
            "commit id": commit.id,
            "hash": commit.hash,
            "message": commit.message,
            "created_at": commit.created_at.isoformat(sep=' ', timespec='seconds')
        }
        for commit in commits
    ]), 200

# 3. Select commit by hash
@repo_bp.route('/repositories/<int:id>/commits/<string:hash>', methods=['GET'])
def select_commit_by_hash(id, hash):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404

    commit = Commit.query.join(Branch).filter(
        Branch.repository_id == id,
        Commit.hash == hash
    ).one_or_none()
    if not commit:
        return jsonify({"message": "Commit not found"}), 404

    return jsonify({
        "commit id": commit.id,
        "hash": commit.hash,
        "message": commit.message,
        "created_at": commit.created_at.isoformat(sep=' ', timespec='seconds'),
        "branch id": commit.branch_id
    }), 200


# 4. List all branches
@repo_bp.route('/repositories/<int:id>/branches', methods=['GET'])
def list_all_branches(id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404

    branches = Branch.query.filter_by(repository_id=id).all()
    return jsonify([{"branch id": branch.id, "branch name": branch.name} for branch in branches]), 200

# 5. List all tags
@repo_bp.route('/repositories/<int:id>/tags', methods=['GET'])
def list_all_tags(id):
    repository = db.session.get(Repository, id)
    if not repository:
        return jsonify({"message": "Repository not found"}), 404

    tags = Tag.query.join(Commit).join(Branch).filter(Branch.repository_id == id).all()
    return jsonify([{"tag id": tag.id, "tag name": tag.name} for tag in tags]), 200

# 6. List all commits in a branch
@repo_bp.route('/repositories/<int:id>/branches/<string:branch>/commits', methods=['GET'])
def list_all_commits(id, branch):
    branch_obj = Branch.query.filter_by(repository_id=id, name=branch).one_or_none()
    if not branch_obj:
        return jsonify({"message": "Repository or branch not found"}), 404

    commits = Commit.query.filter_by(branch_id=branch_obj.id).all()
    return jsonify([{"commit id": commit.id, "hash": commit.hash, "message": commit.message, 
                     "created_at": commit.created_at.isoformat(sep=' ', timespec='seconds') } 
                     for commit in commits]), 200

# 7. Get top-level tree in a commit
@repo_bp.route('/repositories/<int:id>/branches/<string:branch>/commits/<string:hash>/tree', methods=['GET'])
def get_top_level_tree(id, branch, hash):
    commit = Commit.query.join(Branch).filter(
        Branch.repository_id == id,
        Branch.name == branch,
        Commit.hash == hash
    ).one_or_none()
    if not commit:
        return jsonify({"message": "Repository, branch, or commit not found"}), 404
    if not commit.tree_structure:
        return jsonify({"message": "No top-level tree available for this commit"}), 404

    return jsonify({"tree": commit.tree_structure}), 200


# 8. View file or sub-tree
@repo_bp.route('/repositories/<int:id>/branches/<string:branch>/commits/<string:hash>/tree/<path:path>', methods=['GET'])
def view_file_or_subtree(id, branch, hash, path):
    commit = Commit.query.join(Branch).filter(
        Branch.repository_id == id,
        Branch.name == branch,
        Commit.hash == hash
    ).first()
    if not commit:
        return jsonify({"message": "Repository, branch, or commit not found"}), 404
    if not commit.tree_structure:
        return jsonify({"message": "No directory tree available for this commit"}), 404

    def get_tree_at_path(tree, path):
        segments = path.split('/')
        current = tree

        for segment in segments:
            if "children" in current and segment in current["children"]:
                current = current["children"][segment]
            else:
                return None
        return current

    subtree = get_tree_at_path(commit.tree_structure, path)
    if not subtree:
        return jsonify({"message": "File or directory not found"}), 404

    return jsonify(subtree), 200
