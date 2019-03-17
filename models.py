

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

