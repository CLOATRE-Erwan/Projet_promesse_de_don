from flask import Flask, render_template, url_for, request, flash, redirect
# from werkzeug.exceptions import abort
from conn_don import Conn_don

                                
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        name = request.form['name']
        firstname = request.form['firstname']
        adress = request.form['adress']
        mail = request.form['mail']
        somme = request.form['somme']
        valide = 'valide' in request.form 

        if not name or not firstname or not adress or not mail or not somme or not valide:
            flash('Missing arguments!', 'danger')
        else:
            donation = int(somme)
            Conn_don.insert(name, firstname, adress, mail, donation)
            return redirect(url_for('index'))
    return render_template('from.html')

@app.route('/donor', methods=('GET', 'POST'))
def donor():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        if not mail or not password :
            flash('Missing arguments!', 'danger')
        else:
            user = Conn_don.find_user(mail, password)
            if not user:
                flash("Email or Password does not exist", 'danger')
            else:
                if user[0]['role'] == 'admin':
                    dons = Conn_don.get_don()
                    total = Conn_don.total()
                    return render_template('donor.html', dons=dons, total=total)
                else:
                    flash("You don't have the permission", 'danger')
    
    return render_template('login.html')

@app.route('/panel')
def panel():
    return render_template('panel.html')