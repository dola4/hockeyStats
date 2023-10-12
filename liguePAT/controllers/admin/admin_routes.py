from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash

from models.Admin import Admin
from models.Player import Player

admin_routes = Blueprint('admin_routes', __name__)


@admin_routes.route('/admin_dasboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('common_routes.login'))