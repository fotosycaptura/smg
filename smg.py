
import configparser
import bs4
import requests
import os
import json
import re
import sys, getopt
"""
Creado en python 3.9
"""

"""
Configuración Interna

Esta seccion es para la configuracion interna del programa
smg_Lib, es la ruta o librería en donde están almacenados los mangas.
Está definida en config.ini en el parámetro ruta_mangas
"""
smg_version = "1.3.1"
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
        print("                 Manga Downloader                     ")
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

def crear_carpeta_manga(nombre_manga):
        """
        Crea la carpeta que contendrá los capítulos del manga
        Y retorna la ruta física donde serán alojados
        """
        ruta_manga = os.path.join(home_mangas, nombre_manga)
        #print(f"Creando carpeta en {ruta_manga}")
        if not(os.path.exists(ruta_manga) and os.path.isdir(ruta_manga)):
                os.mkdir(os.path.abspath(ruta_manga))
        return ruta_manga

def crear_carpeta_capitulo(ruta_manga, capitulo):
        if not(os.path.exists(os.path.join(ruta_manga, capitulo)) and os.path.isdir(os.path.join(ruta_manga, capitulo))):
                os.mkdir(os.path.join(ruta_manga, capitulo))

def get_capitulos(url_del_manga):
        # Se obtienen los números de capítulos y sus urls
        directorio_capitulos = requests.post(url_del_manga + 'ajax/chapters/')
        sopa_ini = bs4.BeautifulSoup(directorio_capitulos.text, 'lxml')
        all_capitulos = sopa_ini.find_all('a')
        listado = []
        for item in all_capitulos:
                if (len(item['href']) > 1):
                        listado.append([item.text.strip(), item['href']])
        # Listado tendría el "número" de capítulo, y la url del capítulo
        return listado

def descargar_imagenes_del_capitulo(ruta_manga, url_del_capitulo, capitulo):
        resultado = requests.get(url_del_capitulo)
        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
        capitulo_formateado = capitulo.zfill(3).replace('.', '-')

        imagenes = sopa.select(".wp-manga-chapter-img")
        # Se crean las carpetas respectivas para cada capítulo
        crear_carpeta_capitulo(ruta_manga, capitulo_formateado)
        
        # Se descargan las imagenes
        for imagen in imagenes:
                # Se extrae la imagen (url y nombre)
                nombre_file = str(imagen['data-src'])
                nombre_file = nombre_file[nombre_file.rindex('/')+1:]
                
                # Se forma la ruta donde quedará finalmente
                ruta = os.path.join(ruta_manga, capitulo_formateado, nombre_file)
                ruta = os.path.abspath(ruta)
                
                # Se verifica si la imagen ya existía previamente
                if not(os.path.exists(ruta)):
                        # Se extrae la imagen de forma binaria de la web
                        imagen_save = requests.get(imagen['data-src'])
                
                        # Se guarda la imagen en disco
                        f = open (ruta, 'wb')
                        f.write(imagen_save.content)
                        f.close()

def descargar_por_config():
        """ 
        Es el encargado de iniciar el proceso principal de recoleccion, ejecucion de todos los modulos
        En esta version, se corrigen los espacios para las carpetas dentro del manga, reemplazandolos con guiones bajos _ 
        """ 
        print(f"Se encontraron {len(listado_mangas)} mangas para descargar en config.ini...")
        print("Procesando...")
        for manga in listado_mangas:
                url_base = manga['url_base']
                # Por cada manga se crea su carpeta, si es que no existía antes
                ruta_manga = crear_carpeta_manga(manga["nombre"])
                
                # Se obtienen los capítulos en formato["numero", "url"]
                listado_capitulos = get_capitulos(url_base)
                
                # Se procede con el ciclo para la descarga
                inicial = 1
                final = len(listado_capitulos)
                for capitulo, url_capitulo in listado_capitulos:
                        printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                        inicial = inicial + 1
                        if (len(capitulo) > 0):
                                descargar_imagenes_del_capitulo(ruta_manga, url_capitulo, capitulo)
        print("")
        print("Finalizado. Presione [ENTER] para salir")
        input("> ")

def modo_de_uso():
        print('Permite descargar un manga de ---Manga')
        print('Modo de uso:')
        print('smg.py url-manga     - Descarga el manga en cuestión.')
        print('smg.py -c            - Descarga listado de mangas definidos en config.ini')
        print('smg.py -h            - Muestra esta ayuda.')

def descargar_solo(url_manga):
        if(url_manga.startswith("https://submanga.io/manga/")):
                nombre_manga = url_manga[25:].replace("/", "")
                print(f"Descargando {nombre_manga}")
                ruta_manga = crear_carpeta_manga(nombre_manga)
                lst_capitulos_del_manga = get_capitulos(url_manga)
                # Se procede con el ciclo para la descarga
                inicial = 1
                final = len(lst_capitulos_del_manga)
                for capitulo, url_capitulo in lst_capitulos_del_manga:
                        printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                        inicial = inicial + 1
                        if (len(capitulo) > 0):
                                descargar_imagenes_del_capitulo(ruta_manga, url_capitulo, capitulo)
        print("")
        print("Finalizado. Presione [ENTER] para salir")
        input("> ")

def verifica_argumentos(argv):
        presentacion()
        try:
                opts, args = getopt.getopt(argv,"hc")

                for opt, args in opts:
                        if opt == '-h':
                                modo_de_uso()
                                sys.exit()
                        if opt == '-c':
                                descargar_por_config()
                if (len(args) > 0):
                        descargar_solo(args[0])
        except getopt.GetoptError:
                print('smg.py -h para mayor información')
                sys.exit(2)

# Para ejecutar desde la linea de comandos
if __name__ == '__main__':
        verifica_argumentos(sys.argv[1:])
