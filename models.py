import sqlalchemy as sa
from extensions import db



class User(db.Model):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Posts(db.Model):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True)
    header = sa.Column(sa.String(80), unique=False, nullable=False)
    text = sa.Column(sa.Text, unique=False, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))


class Comments(db.Model):
    __tablename__ = 'comments'
    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.Text, unique=False, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    post_id = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))
