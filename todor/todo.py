"""
Crearemos todas las vistas de nuestra lista de tareas.
"""
from flask import Blueprint, render_template, request, url_for, redirect, g
# * IMPORTAMOS EL DECORADOR
from todor.auth import login_required
# * IMPORTAMOS LOS MODELOS
from .models import User, Todo
# * IMPORTAMOS OBJETO DB PARA HACER CONSULTAS
from todor import db


# * CREAMOS OBJETO BLUEPRINT PARA "todo"
bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list')
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def index():
    # * CONSULTA PARA RECUPERAR LAS TAREAS EXISTENTES
    todos = Todo.query.all()

    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=['GET', 'POST'])
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def create():

    if request.method == 'POST':
        title = request.form['titulo_tarea_nueva']
        desc = request.form['descripcion_tarea']

        todo = Todo(g.user.id, title, desc)

        # * AGREGAMOS LOS DATOS INGRESADOS
        db.session.add(todo)
        # * COMMIT PARA REALIZAR CAMBIOS EN LA DATABASE
        db.session.commit()

        # * REDIRECCIONAMOS A LA LISTA DE MATERIALES
        return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


# * FUNCION PARA OBTENER LA TAREA CON EL ID USUARIO
def get_todo(id):
    # * CONSULTA PARA OBTENER LA TAREA A EDITAR
    todo = Todo.query.get_or_404(id)
    # print(type(todo))
    # print(todo.id)
    # print(todo.created_by)
    # print(todo.title)
    # print(todo.desc)
    return todo


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def edit(id):

    todo = get_todo(id)

    if request.method == 'POST':
        todo.title = request.form['titulo_tarea_nueva']
        todo.desc = request.form['descripcion_tarea']
        todo.state = True if request.form.get('state') == 'on' else False

        # * ACTUALIZAMOS CAMBIOS A LA DATABASE
        db.session.commit()

        # * REDIRECCIONAMOS A LA LISTA DE MATERIALES
        return redirect(url_for('todo.index'))
    else:
        return render_template('todo/update.html', todo=todo)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required  # * AGREGAMOS EL DECORADOR PARA QUE REQUIERA INICIAR SESION EN ESTA PANTALLA
def delete(id):

    todo = get_todo(id)

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('todo.index'))
