from db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Head(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # added
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    categories = db.relationship('Category', backref='head', cascade="all, delete-orphan", lazy=True)
    user = db.relationship('User', backref=db.backref('heads', lazy=True))  # added

    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='unique_head_per_user'),)  # ensure uniqueness per user

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # added
    head_id = db.Column(db.Integer, db.ForeignKey('head.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subcategories = db.relationship('Subcategory', backref='category', cascade="all, delete-orphan", lazy=True)
    user = db.relationship('User', backref=db.backref('categories', lazy=True))  # added

    __table_args__ = (db.UniqueConstraint('head_id', 'name', name='unique_category_head'),)

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # added
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('subcategories', lazy=True))  # added

    __table_args__ = (db.UniqueConstraint('category_id', 'name', name='unique_subcategory_category'),)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'

    # For expenses:
    head_id = db.Column(db.Integer, db.ForeignKey('head.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    title = db.Column(db.String(100), nullable=True)

    # For income:
    source = db.Column(db.String(100), nullable=True)

    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    head = db.relationship('Head')
    category = db.relationship('Category')
    subcategory = db.relationship('Subcategory')
