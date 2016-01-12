from noozjunkie_webapp import db
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, PickleType, Numeric, Boolean, Enum

import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120))
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    lastseen = db.Column(db.DateTime)
    active = db.Column(Boolean, default=True)
    authenticated = db.Column(Boolean, default=True)
    perms = db.Column(db.Enum('root', 'admin', 'system', 'user', 'api', 'none', name='user_perms'), default='user')

    def __repr__(self):
        return '<User %r>' % (self.username)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class ArticleKeyword(db.Model):
    __tablename__ = 'articlekeyword'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key = True)
    articleid = Column(Integer, ForeignKey('article.id'))
    keywordid = Column(Integer, ForeignKey('keyword.id'))
    added = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<ArticleKeyword %r>' % (self.id)

class Feed(db.Model):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    title = Column(String, index=True, unique=True)
    source = Column(String)
    description = Column(String)
    published = Column(DateTime)
    interval = Column(Integer)
    retrieved = Column(DateTime)
    active = Column(Integer)
    created = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Feed %r>' % (self.title)

class Article(db.Model):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    keywords = Column(PickleType)
    description = Column(String)
    published = Column(DateTime)
    content = Column(Text)
    contenthash = Column(String)
    retrieved = Column(DateTime)
    feedid = Column(Integer, ForeignKey('feed.id'))
    assoc = db.relationship('ArticleKeyword', backref='articles', primaryjoin=id == ArticleKeyword.articleid)

    def __repr__(self):
        return 'Article %r>' % (self.title)

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key = True)
    word = Column(String, index = True)
    assoc = db.relationship('ArticleKeyword', backref='keywords', primaryjoin=id == ArticleKeyword.keywordid)

    def __repr__(self):
        return '<Article %r>' % (self.word)
