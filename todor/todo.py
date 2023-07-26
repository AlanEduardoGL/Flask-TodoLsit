"""
Crearemos todas las vistas de nuestra lista de tareas.
"""
from flask import Blueprint, render_template
# * IMPORTAMOS EL DECORADOR
from todor.auth import login_required
# * IMPORTAMOS LOS MODELOS
from .models import User, Todo
# * IMPORTAMOS OBJETO DB PARA HACER CONSULTAS
from .__init__ import db


# * CREAMOS OBJETO BLUEPRINT PARA "todo"
bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list')
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def index():
    # * CONSULTA PARA RECUPERAR LAS TAREAS EXISTENTES
    todos = Todo.query.all()

    return render_template('todo/index.html', todos=todos)


@bp.route('/edit')
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def edit():
    return 'Editar Tarea.'


@bp.route('/create')
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def create():
    return 'Crear Tarea.'
