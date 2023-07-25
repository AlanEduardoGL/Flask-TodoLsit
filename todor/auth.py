"""
Contiene las vistas o controlador de la autenticación del usuario.
"""
from flask import Blueprint
from flask import render_template
from . import models

# * CREAMOS OBJETO BLUEPRINT PARA "auth"
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register')
def register():
    return render_template('auth/register.html')


@bp.route('/login')
def login():
    return render_template('auth/login.html')
