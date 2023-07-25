"""
Contiene las vistas o controlador de la autenticación del usuario.
"""
from flask import (
    Blueprint,
    render_template,
    request,  # * OBTENEMOS DATOS DE LOS FORMULARIOS
    url_for,  # * FABRICAR URL
    redirect,  # * REDIRECCIONA A OTRA PAGINA
    flash  # * ENVIA UNA SERIE DE S DE ERROR A LAS PLANTILLAS
)

from werkzeug.security import (
    generate_password_hash,  # * ENVIAMOS DE MANERA ENCRIPTADA EL PASSWORD
    check_password_hash
)
from .models import User
from todor import db


# * CREAMOS OBJETO BLUEPRINT PARA "auth"
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        # * OBTENEMOS LOS DATOS COLOCADOS DEL FORMULARIO 
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        # * VALIDAMOS EN LA BASE DE DATOS QUE NO EXISTA EL NOMBRE DE USUARIO A REGISTRAR
        user_name = User.query.filter_by(username=username).first()

        if user_name == None:
            # * SI NO EXISTE EL USUARIO LO AGREGAMOS A LA BASE DE DATOS
            db.session.add(user)
            # * COMMIT PARA QUE SE HAGAN LOS CAMBIOS A LA BASE DE DATOS
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return f"El nombre de usuario {username} ya se encuentra registrado. Intenta nuevamente."

    return render_template('auth/register.html')


@bp.route('/login')
def login():
    return render_template('auth/login.html')
