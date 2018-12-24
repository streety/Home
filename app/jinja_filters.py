import re
from jinja2 import Markup, escape, evalcontextfilter
from app import app

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@app.template_filter('nl2br')
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
