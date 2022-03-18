
import configparser
import bs4
import requests
import os
import json
"""
Creado en python 3.9
"""

"""
Configuración Interna

Esta seccion es para la configuracion interna del programa
smg_Lib, es la ruta o librería en donde están almacenados los mangas.
Está definida en config.ini en el parámetro ruta_mangas
"""
smg_version = "1.3.0"
config = configparser.ConfigParser()
config.read('config.ini') 
home_mangas = config['DEFAULT']['ruta_mangas']
opciones = config.get('MANGAS','listado_mangas')
listado_mangas = json.loads(opciones)

"""
Fin de la definición de configuración
"""

def presentacion():
        print("******************************************************")
        print("                 Mmanga Downloader                    ")
        print("                Version: " + smg_version + "          ")
        print("******************************************************")

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
    
def run():
        """ 
        Es el encargado de iniciar el proceso principal de recoleccion, ejecucion de todos los modulos
        En esta version, se corrigen los espacios para las carpetas dentro del manga, reemplazandolos con guiones bajos _ 
        """ 
        presentacion()
        print(f"Se encontraron {len(listado_mangas)} mangas para descargar...")
        print("Procesando...")
        for manga in listado_mangas:
                url_base = manga['url_base'] + '{}/'
                # Por cada manga se crea su carpeta, si es que no existía antes
                ruta_manga = os.path.join(home_mangas, manga['nombre'])
                print(f"Creando carpeta en {ruta_manga}")
                if not(os.path.exists(ruta_manga) and os.path.isdir(ruta_manga)):
                        os.mkdir(os.path.abspath(ruta_manga))

                # Por cada capítulo se procede a descargar las imagenes
                for n in range(1, (manga['total_capitulos'] + 1)):
                        resultado = requests.get(url_base.format(n))
                        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
                        imagenes = sopa.select(".wp-manga-chapter-img")
                        capitulo = str(n).zfill(2)
                        # Se crean las carpetas respectivas para cada capítulo
                        if not(os.path.exists(os.path.join(ruta_manga, capitulo)) and os.path.isdir(os.path.join(ruta_manga, capitulo))):
                             print(f"Creando carpeta para el capítulo {capitulo}")
                             os.mkdir(os.path.join(ruta_manga, capitulo))
                        print(f"Descargando imágenes del capítulo {capitulo}")
                        # Variables para la barra de proceso
                        inicial = 1
                        final = len(imagenes)
                        # Se muetra la barra de progreso
                        printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                        for imagen in imagenes:
                                # Se extrae la imagen (url y nombre)
                                nombre_file = str(imagen['data-src'])
                                nombre_file = nombre_file[nombre_file.rindex('/')+1:]
                                
                                # Se forma la ruta donde quedará finalmente
                                ruta = os.path.join(ruta_manga, capitulo, nombre_file)
                                ruta = os.path.abspath(ruta)
                                
                                # Se verifica si la imagen ya existía previamente
                                if not(os.path.exists(ruta)):
                                        # Se extrae la imagen de forma binaria de la web
                                        imagen_save = requests.get(imagen['data-src'])
                                
                                        # Se guarda la imagen en disco
                                        f = open (ruta, 'wb')
                                        f.write(imagen_save.content)
                                        f.close()

                                        # Se muestra la barra de progreso
                                        printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                                else:
                                        # No se descarga nada, pero igual se muestra avance en la barra
                                        printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                                inicial = inicial + 1
                        print("")
        print("")
        print("Finalizado. Presione [ENTER] para salir")
        input("> ")
        

# Para ejecutar desde la linea de comandos
if __name__ == '__main__':
        run()
