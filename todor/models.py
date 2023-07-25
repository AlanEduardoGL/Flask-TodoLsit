"""
Contiene todos los modelos del data de la aplicación. Base de datos y Tablas.
"""
from todor import db


# ! @audit CLASE USERS
# * LA CLASE USERS REPRESENTA EL NOMBRE (tabla) DE LA BASE DE DATOS
class User(db.Model):

    # * ESTOS ATRIBUTOS REPRESENTAN LAS COLUMNAS DE LA BASE DE DATOS
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    # * METODO CONSTRUCTOR
    def __init__(self, username, password):

        self.username = username
        self.password = password

    # * METODO PARA OBTENER DATOS Y SER REPRESENTADOS POR EL NOMBRE DE USUARIO
    def __repr__(self):
        return f"<User: {self.username} >"


# ! @audit CLASE TODO
# * LA CLASE TODO REPRESENTA EL NOMBRE (tabla) DE LA BASE DE DATOS
class Todo(db.Model):

    # * ESTOS ATRIBUTOS REPRESENTAN LAS COLUMNAS DE LA BASE DE DATOS
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default=False)

    # * METODO CONSTRUCTOR
    def __init__(self, created_by, title, desc, state=False):

        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.state = state

    # * METODO PARA OBTENER DATOS Y SER REPRESENTADOS POR EL TITULO DE LA TAREA
    def __repr__(self):
        return f"<Todo: {self.title} >"
