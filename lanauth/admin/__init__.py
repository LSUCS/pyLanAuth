from flask import Blueprint
from flask import current_app, redirect, render_template, request, \
                    session, url_for

from lanauth.db import open_session, to_dict
from lanauth.db.models import Authentications

app = Blueprint('admin', __name__, template_folder='templates')


@app.route('/')
def index():
    """
    Build admin page.

    Page displaying the current settings of the web app
    and current authenitcations in the database
    """
    if 'admin' in session:

        # Build page
        with open_session() as db_session:
            auths = db_session.query(Authentications).all()

            auth=[to_dict(entry) for entry in auths]
            print(auth)
            return render_template(
                'admin.html',
                settings=current_app.iniconfig,
                auths=auth
            )
    else:
        return redirect(url_for('.login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route to admin login page"""

    # Check if already logged in
    if 'admin' in session:
        return redirect(url_for('.index'))

    if request.method == 'GET':
        print("GET")
        return render_template('admin_login.html')
    else:
        print("POST")
        print(request)
        print(request.form)
        if request.form['password'] == current_app.iniconfig.get('flask', 'admin'):
            print("Setting session")
            session['admin'] = True
            return redirect(url_for('.index'))
        else:
            print("Failed login")
            return redirect(url_for('.login'))

@app.route('/logout')
def logout():
    if 'admin' in session:
        del session['admin']

    return redirect(url_for('.login'))
