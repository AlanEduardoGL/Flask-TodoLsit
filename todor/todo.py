"""
Crearemos todas las vistas de nuestra lista de tareas.
"""
from flask import Blueprint, render_template

# * CREAMOS OBJETO BLUEPRINT PARA "todo"
bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list')
def index():
    return render_template('todo/index.html')


@bp.route('/edit')
def edit():
    return 'Editar Tarea.'


@bp.route('/create')
def create():
    return 'Crear Tarea.'
