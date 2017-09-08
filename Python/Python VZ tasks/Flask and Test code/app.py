
#import the Flask class from the flask module
from flask import Flask , render_template, redirect, url_for, request

# create the application object
app = Flask(__name__)


# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template("home.html")
    # return {'hello': 'world'}


@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect (url_for('home'))

    return render_template("login.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)





