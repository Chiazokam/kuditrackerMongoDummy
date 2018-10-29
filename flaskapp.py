from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from wtforms import Form, validators, StringField, TextAreaField, DateField, IntegerField, SelectField, SubmitField
from datetime import datetime
import pymongo
from pymongo import MongoClient # Database connector

app = Flask(__name__)


#Create function to change date to a date object
def date_format(date_string):
    """Function to return date object"""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Incorrect date format, should be in yyyy-mm-dd format")


class ExpenseForm(Form):
    expense_date = DateField('Date: yyyy-mm-dd', [validators.DataRequired()])
    expense_descr = StringField('Description', [validators.length(max=20), validators.DataRequired()])
    expense_amt = IntegerField('Amount', [validators.DataRequired()])
    expense_cat = StringField('Category: business Or personal', [validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ExpenseForm(request.form)

    if request.method == 'POST':
        expense_date = request.form['expense_date']
        #Escape characters that may cause an error when inserted into the db e.g, apostrophe
        expense_descr = request.form['expense_descr']
        expense_amt = request.form['expense_amt']
        expense_cat = request.form['expense_cat']

        client = MongoClient('localhost', 27017)    #Configure the connection to the database
        db = client.kuditracker    #Select the database

        expense = {
           "Date": "06/08/18",
           "Description": expense_descr,
           "Amount(NGN)": expense_amt,
           "Category": expense_cat
           }
        db.expenses.insert_one(expense)
        print(expense)

        return redirect(url_for("index"))
    return render_template('hello.html', form=form)

@app.route('/business')
def business():
    client = MongoClient('localhost', 27017)    #Configure the connection to the database
    db = client.kuditracker    #Select the database
    queryRows = db.expenses.find({"Category": "Business"}, {"_id":1, "Date":1, "Description":1 }).pretty()
    for eachRow in queryRows:
        print(eachRow['Description'])
    return render_template("business.html")

@app.route('/personal')
def personal():
    client = MongoClient('localhost', 27017)    #Configure the connection to the database
    db = client.kuditracker    #Select the database

    return render_template("personal.html")
#=========================================
if __name__ == '__main__':
    app.run(debug=True)
