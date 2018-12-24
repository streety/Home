from app import db
from app.blog import blog
from app.blog import models as bm
from app.blog.forms import CommentForm
from app.blog.utils import get_sidebar_posts, get_tags
from flask import abort, render_template, request, url_for, session
from urllib.parse import urljoin, urlparse
from datetime import datetime
from werkzeug.contrib.atom import AtomFeed
from flask_login import current_user


def make_external(url):
    return urljoin(request.url_root, url)


def get_posts(tag=None):
    try:
        if tag:
            posts = bm.Tag.query.filter_by(tag=tag).first().posts
        else:
            posts = bm.Post.query
        posts = posts.filter_by(published=True). \
            order_by(bm.Post.pubdate.desc())
        return posts
    except AttributeError:
        abort(404)


@blog.context_processor
def inject_sidebar():
    sidebar_posts = get_sidebar_posts()
    sidebar_tags = get_tags(10)
    return dict(sidebar_posts=sidebar_posts,
                sidebar_tags=sidebar_tags)


@blog.route('/', defaults={'tag': None, 'page': 1, }, )
@blog.route('/tag/<tag>/', defaults={'page': 1, }, )
@blog.route('/tag/<tag>/page/<page>/', )
@blog.route('/page/<page>/', defaults={'tag': None, }, )
def index(tag, page):
    posts = get_posts(tag)
    if not posts:
        print('not found')
        abort(404)
    posts = posts.paginate(int(page), 5)
    return render_template('blog/index.html',
                           posts=posts,
                           page=page,
                           tag=tag)


@blog.route('/atom/', defaults={'tag': None})
@blog.route('/tag/<tag>/atom/')
def feed(tag):
    posts = get_posts(tag)
    posts = posts.limit(10).all()
    if not posts:
        abort(404)
    if tag:
        title = 'Posts tagged {0} at jonathanstreet.com'.format(tag)
    else:
        title = 'Posts at jonathanstreet.com'
    feed = AtomFeed(title, feed_url=request.url, url=request.url_root)
    for p in posts:
        feed.add(p.title, p.format_summary(),
                 content_type='html',
                 author='Jonathan Street',
                 url=make_external(url_for('.detail', slug=p.slug)),
                 updated=p.pubdate,
                 published=p.pubdate,)
    return feed.get_response()


@blog.route('/<slug>/', methods=('GET', 'POST'), )
def detail(slug):
    post = bm.Post.query.filter_by(slug=slug).first()
    if not post:
        abort(404)
    if not post.published and not current_user.is_authenticated:
        abort(404)
    if not post.accepting_comments:
        return render_template('blog/detail.html', post=post)
    form = CommentForm()
    if form.validate_on_submit():
        comment = bm.Comment(blogpost=post.id,
                             name=form.name.data,
                             email=form.email.data,
                             website=None,
                             body=form.comment.data,
                             pubdate=datetime.now(),
                             published=False,
                             spam=False,
                             userip=request.remote_addr,
                             useragent=request.user_agent.string,)
        # Add http to start of website if no scheme is currently present.
        # Will not modify if https, or another scheme, is included.
        if form.website.data:
            website = urlparse(form.website.data, scheme='http')
            comment.website = website.geturl()
        db.session.add(comment)
        db.session.commit()
        if 'submitted_comment' not in session:
            session['submitted_comment'] = []
        session['submitted_comment'].append(comment.id)
    return render_template('blog/detail.html', post=post, form=form)


@blog.route('/tag/',)
def tagcloud():
    tags = get_tags()
    return render_template('blog/tagcloud.html', tags=tags)
