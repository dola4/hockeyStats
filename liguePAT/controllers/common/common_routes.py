from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash

from models.Admin import Admin
from models.Player import Player

common_routes = Blueprint('common_routes', __name__)


@common_routes.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        player = Player.find_one_by_email(email)
        admin = Admin.find_one_by_email(email)
        if player:
            if check_password_hash(player.password, password):
                session['player'] = player.to_dict()
                return redirect(url_for('player_routes.player_dashboard'))
            else:
                return render_template('login.html', error="Invalid password")
        elif admin:
            if check_password_hash(admin.password, password):
                session['admin'] = admin.to_dict()
                return redirect(url_for('admin_routes.admin_dashboard'))
            else:
                return render_template('login.html', error="Invalid password")
        else:
            return render_template('login.html', error="Invalid email")


    return render_template('login.html')
