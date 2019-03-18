from flask_restful import Resource, Api, reqparse
from models import User, Posts, Comments
from schemas import UserSchema, PostsSchema, CommentsSchema
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopConfig')
api = Api(app)
db = SQLAlchemy(app)


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
