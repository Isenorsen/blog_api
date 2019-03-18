from flask_restful import Resource, Api, reqparse
from models import User, Posts, Comments
from schemas import UserSchema, PostsSchema, CommentsSchema, IndividualPostSchema
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
        new_post = Posts(header=args['header'],
                         text=args['text'],
                         user_id=args['user_id'])
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
        user = User.query.filter_by(id=args['user_id']).first()
        new_comment = Comments(user_id=args['user_id'],
                               post_id=args['post_id'],
                               text=args['text'],
                               username=user.username)
        db.session.add(new_comment)
        db.session.commit()
        return True


class ApiIndividualPost(Resource):
    def get(self):

        """
        Method allows to get user's post and all it's comments by post_id

        parameters: post_id (int)
        """

        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        args = parser.parse_args()
        post = Posts.query.filter_by(id=args['post_id'])
        post_schema = IndividualPostSchema(many=True)
        result = post_schema.dump(post)
        return result


