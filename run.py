"""
Archivo principal para ejecutar nuestra aplicación.
"""
# * CREAMOS LA INSTANCIA DE LA FUNCION create_app
from todor import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
