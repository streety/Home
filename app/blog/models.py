from flask import session
from sqlalchemy import or_

from app import db
from app.blog import utils

from datetime import datetime


tags = db.Table('tags',
                db.Column('tags_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('posts_id', db.Integer, db.ForeignKey('post.id'))
                )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, )
    summary = db.Column(db.Text, )
    body = db.Column(db.Text, )
    pubdate = db.Column(db.DateTime, )
    published = db.Column(db.Boolean, )
    slug = db.Column(db.String(140), index=True, unique=True, )
    accepting_comments = db.Column(db.Boolean, )
    comments = db.relationship('Comment', backref='post', lazy='dynamic', )
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title='', summary='', body='', pubdate=None, 
                 published=False, slug='', accepting_comments=False, tags=[]):
        self.title = title
        self.summary = summary
        self.body = body
        if pubdate is None:
            pubdate = datetime.now()
        self.pubdate = pubdate
        self.published = published
        self.slug = slug
        self.accepting_comments = accepting_comments
        self.tags = tags

    def __repr__(self):
        return '<Post %r>' % (self.slug)

    def format_summary(self):
        return utils.render_html_post(self.summary)

    def format_body(self):
        return utils.render_html_post(self.body)

    @property
    def approved_and_visitor_comments(self):
        if 'submitted_comment' in session:
            return self.comments.filter(or_(Comment.published == True,
                Comment.id.in_(session['submitted_comment']))). \
                order_by(Comment.pubdate).all()
        else:
            return self.comments.filter(Comment.published == True). \
                order_by(Comment.pubdate).all()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(140), index=True, unique=True,)

    def __init__(self, tag=''):
        self.tag = tag

    def __repr__(self):
        return '<Tag %r>' % (self.tag)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blogpost = db.Column(db.Integer, db.ForeignKey('post.id'))
    name = db.Column(db.String(255), )
    email = db.Column(db.Text, nullable=True, )
    website = db.Column(db.Text, nullable=True, )
    body = db.Column(db.Text, )
    pubdate = db.Column(db.DateTime, )
    published = db.Column(db.Boolean, index=True, )
    spam = db.Column(db.Boolean, index=True, )
    userip = db.Column(db.String(255), nullable=True, )
    useragent = db.Column(db.String(255), nullable=True, )

    def __init__(self, blogpost=None, name='', email='', website='',
                 body='', pubdate=None, published=None, spam=None, userip='',
                 useragent=''):
        self.blogpost = blogpost
        self.name = name
        self.email = email
        self.website = website
        self.body = body
        if pubdate is None:
            pubdate = datetime.now()
        self.pubdate = pubdate
        self.published = published
        self.spam = spam
        self.userip = userip
        self.useragent = useragent

    def __repr__(self):
        return '<Comment %r>' % (self.name)
