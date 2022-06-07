from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.validators import InputRequired
from controller import ontologyComparision


class FormValidator(FlaskForm):
    owlfile = StringField('owlfile', validators=[InputRequired(message="Please choose an ontology to upload"),
                                                 FileAllowed(['owl', 'ttl'], 'Only ontology file!')])
    owlfile1 = StringField('owlfile1', validators=[])
    owlfile2 = StringField('owlfile2', validators=[])
    group = StringField('group')


class DoubleFormValidator(FlaskForm):
    owlfile1 = StringField('owlfile1', validators=[InputRequired(message="Please choose ontology 1 to upload"),
                                                   FileAllowed(['owl', 'ttl'], 'Only ontology file!')])
    owlfile2 = StringField('owlfile2', validators=[InputRequired(message="Please choose ontology 2 to upload"),
                                                   FileAllowed(['owl', 'ttl'], 'Only ontology file!')])
    owlfile = StringField('owlfile', validators=[])
    group = StringField('group')


class IndicatorValidator(FlaskForm):
    indicator1 = StringField('indicator1',
                             validators=[InputRequired(message="Please enter the first indicator definition")])
    indicator2 = StringField('indicator2', validators=[InputRequired(message="Please enter the second indicator "
                                                                             "definition")])
    group = StringField('group', validators=[InputRequired(message="Please select a method for comparative analysis")])

    def validate_indicator1(self, indicator1):
        result = ontologyComparision.indicator_validation(indicator1.data)
        if not result:
            raise ValidationError('Indicator 1 can not be found in the owl file(s)')

    def validate_indicator2(self, indicator2):
        if self.indicator1.data == indicator2.data:
            raise ValidationError('Indicator 1 and Indicator 2 can not be the same')
        else:
            result = ontologyComparision.indicator_validation(indicator2.data)
            if not result:
                raise ValidationError('Indicator 2 can not be found in the owl file(s)')
