from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Regexp, EqualTo, Email, ValidationError
from .models import User, Tag


class BookmarkForm(FlaskForm):
    url = URLField('The URL for your bookmark', validators=[DataRequired(), url()])
    # if url.error:
    #     print("form: Form errors: {}".format(url.errors))
    # print("dddd")
    description = StringField('description')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-z0-9, ]*$',
                    message="Tags can only contain letters and numbers")])

    def validate(self):
        if not self.url.data.startswith("http://") or \
                self.url.data.startswith("https://"):
            self.url.data = "http://" + self.url.data

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        # filter not empty and duplicate tag names
        # print(self.tags.data)
        stripped = [t.strip() for t in self.tags.data.split(",")]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True

