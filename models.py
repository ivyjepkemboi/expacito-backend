from db import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True)
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Head(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True)
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_uuid = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('heads', lazy=True))
    categories = db.relationship('Category', backref='head', cascade="all, delete-orphan", lazy=True)

    __table_args__ = (db.UniqueConstraint('user_uuid', 'name', name='unique_head_per_user'),)

class Category(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True)
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_uuid = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)
    head_uuid = db.Column(db.String(36), db.ForeignKey('head.uuid'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('categories', lazy=True))
    subcategories = db.relationship('Subcategory', backref='category', cascade="all, delete-orphan", lazy=True)

    __table_args__ = (db.UniqueConstraint('head_uuid', 'name', name='unique_category_head'),)

class Subcategory(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True)
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_uuid = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)
    category_uuid = db.Column(db.String(36), db.ForeignKey('category.uuid'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('subcategories', lazy=True))

    __table_args__ = (db.UniqueConstraint('category_uuid', 'name', name='unique_subcategory_category'),)

class Transaction(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True)
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_uuid = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)
    type = db.Column(db.String(10), nullable=False)

    head_uuid = db.Column(db.String(36), db.ForeignKey('head.uuid'), nullable=True)
    category_uuid = db.Column(db.String(36), db.ForeignKey('category.uuid'), nullable=True)
    subcategory_uuid = db.Column(db.String(36), db.ForeignKey('subcategory.uuid'), nullable=True)
    title = db.Column(db.Text, nullable=True)

    source = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    transaction_date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    head = db.relationship('Head')
    category = db.relationship('Category')
    subcategory = db.relationship('Subcategory')
