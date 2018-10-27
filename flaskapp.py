from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from wtforms import Form, validators, StringField, TextAreaField, DateField, IntegerField, SelectField, SubmitField

app = Flask(__name__)

class ExpenseForm(Form):
    expense_date = DateField('Date: yyyy-mm-dd', [validators.DataRequired()])
    expense_descr = StringField('Description', [validators.length(max=20), validators.DataRequired()])
    expense_amt = IntegerField('Amount', [validators.DataRequired()])
    expense_cat = StringField('Category: business Or personal', [validators.DataRequired()])


@app.route('/')
def index():
    form = ExpenseForm(request.form)
    return render_template('hello.html', form=form)

#=========================================
if __name__ == '__main__':
    app.run(debug=True)
