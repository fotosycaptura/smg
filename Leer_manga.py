import configparser
from flask import Flask, url_for, render_template, request, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flaskext.markdown import Markdown
from flask_cors import CORS
import os, pathlib, sys, html
from natsort import natsorted
import json
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
opciones = config.get('MANGAS','listado_mangas')
LEIDOS = config.get('LEIDOS', 'listado')
"""
Fin de la definición de configuración
"""

MANGA_FOLDER = os.path.abspath(home_mangas)

app = Flask(__name__, template_folder="templates")
app.config['MANGA_FOLDER'] = MANGA_FOLDER
app.config['MANGAS_LEIDOS'] = LEIDOS
CORS(app)

Markdown(app)

@app.route('/')
def principal():
    content = ""
    with open("./markdown/bienvenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    listado = get_listado()
    content = content + " Desplegando mangas sin leer."
    return render_template('index.html', contenido=content, listado=listado)

@app.route('/todos')
def todos():
    content = ""
    with open("./markdown/bienvenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    listado = get_listado_todos()
    content = content + " Desplegando **todos** los mangas."
    return render_template('index.html', contenido=content, listado=listado)

@app.route('/acerca-de')
def acercade():
    content = ""
    with open("./markdown/acercade.md", "r", encoding="utf-8") as f:
        content = f.read()
    return render_template('acercade.html', contenido=content)

@app.route('/ver')
def ver():
    page = request.args.get('manga', default = '*', type = str)

    listado = get_imagenes(page)
    pagina = request.args.get('page', default=0, type=int)
    return render_template('ver.html', contenido=page, listado=listado, pagina=pagina) 

@app.route('/marcar')
def marcar_leido():
    """
    Encargado de marcar el manga como leído para quitar de la lista
    """
    # Obtiene el parámetro de pagina

    page = request.args.get('pagina', default = '*', type = str)

    # Lee configuración del archivo.
    config = configparser.ConfigParser()
    config.read('config.ini') 
    home_mangas = config['DEFAULT']['ruta_mangas']
    listado_mangas = config.get('MANGAS','listado_mangas')
    listado_leidos = json.loads(config.get('LEIDOS', 'listado'))
    
    # Se agrega el nuevo manga "ya leído"

    listado_leidos.append(page)

    # Se setea valores que irán al archivo de configuración    
    config['DEFAULT']['ruta_mangas'] = home_mangas
    config['MANGAS']['listado_mangas'] = listado_mangas
    config['LEIDOS']['listado'] = json.dumps(listado_leidos)

    # Se guarda en el archivo de configuración.
    with open('config.ini', 'w') as configfile:    # save
        config.write(configfile)
    
    app.config['MANGAS_LEIDOS']
    config.read('config.ini') 
    home_mangas = config['DEFAULT']['ruta_mangas']
    opciones = config.get('MANGAS','listado_mangas')
    LEIDOS = config.get('LEIDOS', 'listado')
    app.config['MANGAS_LEIDOS'] = LEIDOS
    # Se redirecciona a la raíz del sitio.
    return redirect('/')

@app.route('/<path:path>')
def static_file(path):
    print(path, file=sys.stderr)
    return app.send_static_file(path)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def bl_si_leido(str1, lst) -> bool:
    """
    Se encarga de revisar si existe el nombre del manga str1 en lst
    Regresa False si es encontrado para indicar que no lo incluya más adelante
    """
    if str1 in lst:
        return False
    return True

def get_listado():
    """
    Obtiene las carpetas dentro del directorio especificado en MMANGA_FOLDER
    y estos serán usados como nombres de los mangas.
    Una vez leídos, filtra aquellos que ya se encuentran en el config.ini para
    no desplegar aquellos mencionados en listado dentro de LEIDOS.
    """
    listado_directorios = []
    if not os.path.exists(app.config['MANGA_FOLDER']):
        return (listado_directorios)
    for dirs in os.listdir(app.config["MANGA_FOLDER"]):
        if (dirs != 'Otros'):
            if (dirs != '.DS_Store'):
                if (dirs.find('.zip') < 0):
                    if bl_si_leido(dirs, app.config['MANGAS_LEIDOS']):
                        listado_directorios.append([dirs])
    listado_directorios.sort()
    listado_directorios_ordenados = natsorted(listado_directorios, key=str)
    return (listado_directorios_ordenados)

def get_listado_todos():
    """
    Obtiene las carpetas dentro del directorio especificado en MMANGA_FOLDER
    y estos serán usados como nombres de los mangas.
    """
    listado_directorios = []
    if not os.path.exists(app.config['MANGA_FOLDER']):
        return (listado_directorios)
    for dirs in os.listdir(app.config["MANGA_FOLDER"]):
        if (dirs != 'Otros'):
            if (dirs != '.DS_Store'):
                if (dirs.find('.zip') < 0):
                    listado_directorios.append([dirs])
    listado_directorios.sort()
    listado_directorios_ordenados = natsorted(listado_directorios, key=str)
    return (listado_directorios_ordenados)

def bl_filtrar(str) -> bool:
    """
    Sirve para filtrar por aquellos elementos dentro del directorio que no sean imagenes
    """
    filtro = ['.zip', '.DS_Store', '.info', '.rar', '.db', '#']
    for item in filtro:
        if str.find(item) >= 0:
            return False
    return True

def get_imagenes(nombre_manga):
    """
    Obtiene las imagenes de cada subcarpeta especificada en la carpeta "nombre_manga"
    Se extraen las imagenes y se ordenan en orden correlativo natural.
    Se dejan fuera aquellos archivos que están especificados en bl_filtrar
    """
    imagenes = []
    paginacion = []
    ruta = os.path.join(app.config['MANGA_FOLDER'], nombre_manga)
    directorio = pathlib.Path(ruta)
    for direct in directorio.iterdir():
        if os.path.isdir(direct):
            if (bl_filtrar(direct.name)):
                for fichero in direct.iterdir():
                    # La ruta para html debe de ser relativa, no absoluta
                    if (bl_filtrar(fichero.name)):
                        ruta_relativa =  nombre_manga + "/" + direct.name + "/"
                        encodeado = html.unescape(home_mangas + "/" + ruta_relativa + fichero.name)
                        imagenes.append(encodeado)
                imagenes_ordenadas = natsorted(imagenes, key=str)
                paginacion.append(imagenes_ordenadas)
                imagenes = []
        else:
            # La ruta para html debe de ser relativa, no absoluta
            if (bl_filtrar(direct.name)):
                ruta_relativa =  nombre_manga + "/" + direct.name
                encodeado = html.unescape(home_mangas + "/" + ruta_relativa)
                imagenes.append(encodeado)
    if (len(imagenes) > 0):
        imagenes_ordenadas = natsorted(imagenes, key=str)
        paginacion.append(imagenes_ordenadas)
    paginacion.sort()
    #print(paginacion, file=sys.stderr)
    return (paginacion)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
