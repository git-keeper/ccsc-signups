from re import sub
from flask import Flask, render_template, request, url_for, flash, redirect
import subprocess
from email_validator import validate_email, EmailNotValidError

def is_email_valid(email):
	try:
        # the check of deliverability takes too much time
		validate_email(email, check_deliverability=False)
		return True
	except EmailNotValidError:
		return False


app = Flask(__name__)
app.config['SECRET_KEY'] = '42a7f962441e4db32652894755a386455a56f7fb0b67629f'


@app.route('/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        if not fname:
            flash('First name is required')
        if not lname:
            flash('Last name is required')
        if not email:
            flash('Email is required')
        if not is_email_valid(email):
            flash('Invalid email address')
        else:
            print(['gkeep', 'add_faculty', lname, fname, email])
            result = subprocess.call(['gkeep', 'add_faculty', lname, fname, email])
            print(result)

            if result != 0:
                flash('Email address already registered as a user.')
            else:
                return redirect(url_for('response'))

    return render_template('index.html')


@app.route('/response/', methods=['GET'])
def response():
    return render_template('response.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
