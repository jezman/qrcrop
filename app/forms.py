from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError


class GenerateCode(FlaskForm):
    count = IntegerField('Count', validators=[DataRequired()])
    prefix = StringField('Prefix', validators=[DataRequired()])
    submit = SubmitField('Generate')
    codes = []

    # def validate_count(self, count):
    #     if not isinstance(count.data, int):
    #         raise ValidationError('Only numbers')
    #     return True
