from flask import render_template, request
from controller import utils
# from main import app
from controller import ontologyComparision
from flask import current_app


def result():
    if request.method == 'GET':
        return "We are not using this get method! Sorry"
    if request.method == 'POST':
        indicator_validate = utils.IndicatorValidator()
        if indicator_validate.validate_on_submit():
            current_app.config['INDICATOR_1'] = request.form['indicator1']
            current_app.config['INDICATOR_2'] = request.form['indicator2']
            current_app.config['METHOD'] = request.form['group']
            result, output = ontologyComparision.Comparision()
            if not result:
                return render_template('indicator.html', form=indicator_validate)
            else:
                if current_app.config['METHOD'] == 'valueRestriction':
                    return render_template('value_result.html', output=output)
                else:
                    return render_template('result.html', output=output)
        return render_template('indicator.html', form=indicator_validate)
