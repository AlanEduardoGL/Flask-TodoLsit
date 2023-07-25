"""
Contiene las vistas o controlador de la autenticación del usuario.
"""
from flask import (
    Blueprint,
    render_template,
    request,  # * OBTENEMOS DATOS DE LOS FORMULARIOS
    url_for,  # * FABRICAR URL
    redirect,  # * REDIRECCIONA A OTRA PAGINA
    flash,  # * ENVIA UNA SERIE DE MENSAJES DE ERROR A LAS PLANTILLAS HTML
    session,  # * PARA GUARDAR Y SABER SI UN USUARIO HA INICIADO SESION O NO
    g  # * OBJETO PARA ALMACENAR COKIES
)

from werkzeug.security import (
    generate_password_hash,  # * ENVIAMOS DE MANERA ENCRIPTADA EL PASSWORD
    check_password_hash  # * OBTENEMOS LA CONTRASEÑA DE LA BASE DE DATOS ENCRIPTADA
)
from .models import User
from todor import db


# * CREAMOS OBJETO BLUEPRINT PARA "auth"
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():

    # * VALIDAMOS QUE VENGA EN POST
    if request.method == 'POST':
        # * OBTENEMOS LOS DATOS COLOCADOS DEL FORMULARIO
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        # * VARIABLE DE ERROR
        massage_error = None

        # * VALIDAMOS EN LA BASE DE DATOS QUE NO EXISTA EL NOMBRE DE USUARIO A REGISTRAR
        user_name = User.query.filter_by(username=username).first()

        if user_name == None:
            # * SI NO EXISTE EL USUARIO LO AGREGAMOS A LA BASE DE DATOS
            db.session.add(user)
            # * COMMIT PARA QUE SE HAGAN LOS CAMBIOS A LA BASE DE DATOS
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            massage_error = f'El usuario "{username}" se encuentra registrado. Intenta nuevamente.'
            # * MANDMOS EL MENSAJE DE ERROR CON FLASH

        # * MANDAMOS MENSAJES DE ERROR EN CASO DE EXISTIR
        flash(massage_error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():

    # * VALIDAMOS QUE VENGA EN POST
    if request.method == 'POST':
        # * OBTENEMOS LOS DATOS COLOCADOS DEL FORMULARIO
        username = request.form['username']
        password = request.form['password']

        # * VARIABLE MENSAJE DE ERROR
        massage_error = None

        # * CONSULTAMOS EL "username" A LA BASE DE DATOS CON LA CONSULTA
        user = User.query.filter_by(username=username).first()

        # * VALIDAMOS QUE LOS DATOS INGRESADOS SEAN CORRECTOS
        if user == None or not check_password_hash(user.password, password):
            massage_error = f'El nombre de usuario y/o contraseña son incorrectos. Vuelve a intentarlo nuevamente.'
        else:
            # * SI LOS DATOS SON CORECTOS INICIAMOS SESION
            if massage_error is None:
                # * LIMPIAMOS CUALQUIER SESION INICIADA ANTERIORMENTE
                session.clear()
                # * RECUPERAMOS EL ID DE LA PERSONA QUE INICIO SESION
                session['user_id'] = user.id
                return redirect(url_for('todo.index'))

        # * MANDAMOS MENSAJE DE ERROR EN CASO DE EXISTIR
        flash(massage_error)

    return render_template('auth/login.html')


# * FUNCION PARA MANTENER LA SESION ACTIVA
@bp.before_app_request  # ! REGISTRAMOS ESTA FUNCION Y QUE SE EJECUTE EN CADA PETICION !
def load_logged_in_user():

    user_id = session.get('user_id')

    # * VALIDAMOS QUE SE INICIE UNA SESION
    if user_id != None:
        # * LA CONSULTA RETORNA UN USUARIO
        g.user = User.query.get_or_404(user_id)
    else:
        # * DE LO CONTRARIO SERA NULO
        g.user = None


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
