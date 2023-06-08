import configparser
from flask import Flask, url_for, render_template, request, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flaskext.markdown import Markdown
from flask_cors import CORS
import os, pathlib, sys, html

"""
Creado en python 3.11
"""

"""
Configuración Interna

Esta seccion es para la configuracion interna del programa
smg_Lib, es la ruta o librería en donde están almacenados los mangas.
Está definida en config.ini en el parámetro ruta_mangas
"""
config = configparser.ConfigParser()
config.read('config.ini') 
home_mangas = config['DEFAULT']['ruta_mangas']
"""
Fin de la definición de configuración
"""

MANGA_FOLDER = os.path.abspath(home_mangas)

app = Flask(__name__, template_folder="templates")
app.config['MANGA_FOLDER'] = MANGA_FOLDER
CORS(app)

Markdown(app)

@app.route('/')
def principal():
    content = ""
    with open("./markdown/bienvenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    listado = get_listado()
    return render_template('index.html', contenido=content, listado=listado)

@app.route('/ver')
def ver():
    page = request.args.get('manga', default = '*', type = str)

    listado = get_imagenes(page)
    return render_template('ver.html', contenido=page, listado=listado) 

@app.route('/<path:path>')
def static_file(path):
    print(path, file=sys.stderr)
    return app.send_static_file(path)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def get_listado():
    lisado_directorios = []
    if not os.path.exists(app.config['MANGA_FOLDER']):
        return (lisado_directorios)
    for dirs in os.listdir(app.config["MANGA_FOLDER"]):
        if (dirs != 'Otros'):
            lisado_directorios.append([dirs])
    lisado_directorios.sort()
    return (lisado_directorios)

def get_imagenes(nombre_manga):
    imagenes = []
    ruta = os.path.join(app.config['MANGA_FOLDER'], nombre_manga)
    directorio = pathlib.Path(ruta)
    for direct in directorio.iterdir():
        for fichero in direct.iterdir():
            # La ruta para html debe de ser relativa, no absoluta
            ruta_relativa =  nombre_manga + "/" + direct.name + "/"
            encodeado = html.unescape("Mngs/" + ruta_relativa + fichero.name)
            imagenes.append(encodeado)
    return (imagenes)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
