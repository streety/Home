import markdown
import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

import hashlib

from app.blog import models as bm
from app import db
from sqlalchemy.sql import func


class markdownplus:

    store = {}

    def render(self, text):
        """Apply markdown formatting to text.  Code blocks surrounded
        by {{{#!Lang }}} are first converted to pygments highlighted
        code blocks."""
        if text is None:
            return text
        text = self.convert_code(text)
        markdowntext = markdown.markdown(text)
        return self.replace_code(markdowntext)

    def replace_code(self, text):
        for key, value in self.store.items():
            text = text.replace(key, value)
        return text

    def convert_code(self, text):
        """Search the supplied text for blocks of code and format
        with pygments"""
        pattern = '{{{(.*?)}}}'
        patterncompiled = re.compile(pattern, flags=re.DOTALL)
        return re.sub(patterncompiled, self.format_code, text)

    def format_code(self, matchobj):
        """Callback function for regex in convert_code"""
        code = matchobj.group(0)
        firstline = code.split('\n')[0]
        code = '\n'.join(code.split('\n')[1:])[:-3]
        if firstline[:5] == '{{{#!':
            try:
                lexer = get_lexer_by_name(firstline[5:].strip().lower())
            except:
                lexer = guess_lexer(code[3:])
        else:
            try:
                lexer = guess_lexer(code[3:])
            except:
                lexer = get_lexer_by_name('text')
        formatter = HtmlFormatter()
        highlightedcode = highlight(code, lexer, formatter)
        style = formatter.get_style_defs('.highlight')
        output = "<style>%s</style>\n%s" % (style, highlightedcode)
        m = hashlib.md5()
        m.update(output.encode('utf-8'))
        outputhash = m.hexdigest()
        self.store[outputhash] = output
        return outputhash


def render_html_post(text):
    mdp = markdownplus()
    text = mdp.render(text)
    return text


def get_sidebar_posts(limit=5):
    """ Return the most recent posts """
    return bm.Post.query.filter_by(published=True). \
            order_by(bm.Post.pubdate.desc()).limit(limit).all()


def get_tags(limit=None):
    """ Return a list of tags sorted by usage """
    tags = db.session.query(bm.Tag,
            func.count(bm.tags.c.posts_id).label('total')).join(bm.tags). \
            group_by(bm.Tag).order_by('total DESC', 'tag')
    if limit:
        return tags.limit(limit).all()
    else:
        return tags.all()
