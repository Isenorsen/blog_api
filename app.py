from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
import sqlalchemy as sa
from marshmallow import Schema, fields, pprint


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Schemas

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()

class PostsSchema(Schema):
    id = fields.Int()
    header = fields.Str()
    text = fields.Str()
    user_id = fields.Int()
    username = fields.Str()

class CommentsSchema(Schema):
    id = fields.Int()
    text = fields.Str()
    user_id = fields.Int()

# Database tables

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Posts(db.Model):
    __tablename__ = 'posts'
    id = sa.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.Integer, sa.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.Integer, sa.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, sa.ForeignKey('posts.id'))

#
# @app.route('/')
# def index():
#     query = User.query.all()
#     lst = []
#     for user in query:
#         lst.append(user.username)
#     return json.dumps(lst)


# API

class ApiUsers(Resource):

    def get(self):
        query = User.query.all()
        user_schema = UserSchema(many=True)
        result = user_schema.dump(query)
        return result

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        args = parser.parse_args()
        new_user = User(username=args['username'])
        db.session.add(new_user)
        db.session.commit()
        return True


class ApiPosts(Resource):
    def get(self):
        query = Posts.query.all()
        post_schema = PostsSchema(many=True)
        result = post_schema.dump(query)
        return result

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('header')
        parser.add_argument('text')
        parser.add_argument('user_id')
        args = parser.parse_args()
        new_post = Posts(header=args['header'], text=args['text'], user_id=args['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return True


class ApiComments(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        args = parser.parse_args()
        query = Comments.query.filter_by(post_id=args['post_id'])
        comments_schema = CommentsSchema(many=True)
        result = comments_schema.dump(query)
        return result

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        parser.add_argument('user_id')
        parser.add_argument('text')
        args = parser.parse_args()
        new_comment = Comments(user_id=args['user_id'], post_id=args['post_id'], text=args['text'])
        db.session.add(new_comment)
        db.session.commit()
        return True


api.add_resource(ApiUsers, '/hello')
api.add_resource(ApiPosts, '/posts')
api.add_resource(ApiComments, '/comments')


app.run(debug=True)
