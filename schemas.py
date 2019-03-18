from marshmallow import Schema, fields


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
    username = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    posts = fields.Nested('PostsSchema', many=True, exclude=('user_id', ))
    comments = fields.Nested('CommentsSchema', many=True)


class IndividualPostSchema(Schema):
    header = fields.Str()
    text = fields.Str()
    user_id = fields.Int()
    username = fields.Str()
    comments = fields.Nested('CommentsSchema', many=True)
