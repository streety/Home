""" Build CSS assets for the site """

from app import app

from flask_assets import Environment, Bundle

assets = Environment(app)

css_filters = ['scss', 'autoprefixer6', ]

if not app.config['DEBUG']:
    css_filters.append('cssmin')


css_all = Bundle(
        'sass/style.scss',
        filters=css_filters,
        output='css/site.css',
        depends=('sass/*.scss'),
        )
assets.register('css_all', css_all)
