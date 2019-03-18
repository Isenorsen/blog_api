from flask import Flask
from flask_restful import Api
from api import ApiUsers, ApiComments, ApiPosts
from extensions import db, migrate


app = Flask(__name__)
app.config.from_object('config.DevelopConfig')
api = Api(app)
db.init_app(app)
migrate.init_app(app, db)

api.add_resource(ApiUsers, '/users')
api.add_resource(ApiPosts, '/posts')
api.add_resource(ApiComments, '/comments')


app.run()
