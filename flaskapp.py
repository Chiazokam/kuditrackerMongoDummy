from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from wtforms import Form, validators, StringField, TextAreaField, DateField, IntegerField, SelectField, SubmitField
import mysql.connector as mariadb
from datetime import datetime
import pymysql  #Downloaded and imported

app = Flask(__name__)

def dbConnection():
    """Function to connect to the DB"""
    db_conn = mariadb.connect(user='mt3alqgu9u1xsctb',
                              password='trhx9bgb1i1au1sq',
                              database='a2b7jptfulz8wqhr',
                              port = 3306)
    cursor = db_conn.cursor()

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
        expense_date = date_format(request.form['expense_date'])
        #Escape characters that may cause an error when inserted into the db e.g, apostrophe
        expense_descr =  pymysql.escape_string(request.form['expense_descr'])
        expense_amt = pymysql.escape_string(request.form['expense_amt'])
        expense_cat = request.form['expense_cat']

        #Connect to mariaDB
        db_conn = mariadb.connect(user='root',
                                      password='root',
                                      database='kuditracker')
        cursor = db_conn.cursor()
        #Insert data into the db
        query = "INSERT INTO expenses (ExpenseDate, Description, Amount, Category) VALUES ('{}', '{}', '{}', '{}')".format(expense_date, expense_descr, expense_amt, expense_cat)
        cursor.execute(query)
        db_conn.commit()
        #Close connection
        cursor.close()
        return redirect(url_for("index"))
    return render_template('hello.html', form=form)

#=========================================
if __name__ == '__main__':
    app.run(debug=True)
