from flask_wtf import Form
from wtforms import TextAreaField, StringField, validators


class CommentForm(Form):
    """ Basic comment form """

    name = StringField('Name', [validators.required()])
    email = StringField('Email', [validators.optional()])
    website = StringField('Website', [validators.optional()])
    comment = TextAreaField('Comment', [validators.required()])
