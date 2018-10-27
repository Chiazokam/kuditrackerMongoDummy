from flask import Flask, render_template

app = Flask(__name__)
#moment = Moment(app)

@app.route('/')
def index():
    return render_template('hello.html')

#=========================================
if __name__ == '__main__':
    app.run(debug=True)
