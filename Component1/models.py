from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
from datetime import datetime, timezone

db = SQLAlchemy()

class Repository(db.Model):
    __tablename__ = 'repositories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    author_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    branches = db.relationship('Branch', backref='repository')
    issues = db.relationship('Issue', backref='repository')

class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    repository_id = db.Column(db.Integer, db.ForeignKey('repositories.id'), nullable=False)

    commits = db.relationship('Commit', backref='branch')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    commit_id = db.Column(db.Integer, db.ForeignKey('commits.id'), nullable=False)

class Commit(db.Model):
    __tablename__ = 'commits'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(40), nullable=False, unique=True)
    message = db.Column(db.String(500), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    tree_structure = db.Column(JSON, nullable=True)

    tags = db.relationship('Tag', backref='commit')

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(10), default='Open')  #  status: Open or Closed
    repository_id = db.Column(db.Integer, db.ForeignKey('repositories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    submitter_id = db.Column(db.Integer, nullable=False)

    comments = db.relationship('Comment', backref='issue')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

