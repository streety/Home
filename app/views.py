from app import app
from flask import render_template

from app.blog.utils import get_sidebar_posts


@app.route('/')
def index():
    posts = get_sidebar_posts()
    return render_template('index.html', posts=posts)


@app.route('/cv-publications/')
def cv():
    return render_template('cv-publications.html')


@app.route('/now/')
def now():
    return render_template('now.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')
