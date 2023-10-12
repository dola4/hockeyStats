from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash

from models.Admin import Admin
from models.Player import Player

player_routes = Blueprint('player_routes', __name__)


@player_routes.route('/player_dasboard', methods=['GET', 'POST'])
def player_dasboard():
    if 'player' in session:
        return render_template('player_dashboard.html')
    else:
        return redirect(url_for('common_routes.login'))
    