from marshmallow import Schema, fields, pprint

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
