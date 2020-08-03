from router import db,bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship('BlogPost', backref='author')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymouse(self):
        return True

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '{}-{}-{}'.format(self.username,self.email,self.password)

class BlogPost(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'),nullable=False)

    def __init__(self, title, description,author_id):
        self.title = title
        self.description = description
        self.author_id = author_id

    def __repr__(self):
        return '{}-{}'.format(self.title, self.description)