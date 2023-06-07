import configparser
import json
import sys, getopt
from varios import utilerias
from scrap import submanga_io, leermanga_net, manhwas_net
"""
Creado en python 3.11
"""

"""
Configuración Interna

Esta seccion es para la configuracion interna del programa
smg_Lib, es la ruta o librería en donde están almacenados los mangas.
Está definida en config.ini en el parámetro ruta_mangas
"""
smg_version = "1.3.3"
config = configparser.ConfigParser()
config.read('config.ini') 
home_mangas = config['DEFAULT']['ruta_mangas']
opciones = config.get('MANGAS','listado_mangas')
listado_mangas = json.loads(opciones)

"""
Fin de la definición de configuración
"""
def verifica_argumentos(argv):
        Varios = utilerias.utilerias(smg_version)
        submanga = submanga_io.submanga(smg_version, home_mangas, opciones, listado_mangas)
        Varios.presentacion()
        try:
                opts, args = getopt.getopt(argv,"hc")
                for opt, args in opts:
                        if opt == '-h':
                                Varios.modo_de_uso()
                                sys.exit()
                        if opt == '-c':
                                submanga.descargar_por_config()
                if (len(args) > 0):
                        if(args[0].startswith("https://www3.tumangaonline.site/manga/")):
                                submanga.descargar_solo(home_mangas, args[0])
                        elif(args[0].startswith("https://leermanga.net/manga/")):
                                leerManga = leermanga_net.leermanga_net(smg_version, home_mangas, opciones, listado_mangas)
                                leerManga.descargar_solo(home_mangas, args[0])
                        elif(args[0].startswith('https://www.manhwas.net/manga/')):
                                leer_manhwas = manhwas_net.manhwas_net(smg_version, home_mangas, opciones, listado_mangas)
                                leer_manhwas.descargar_solo(args[0])
        except getopt.GetoptError:
                print('smg.py -h para mayor información')
                sys.exit(2)

# Para ejecutar desde la linea de comandos
if __name__ == '__main__':
        verifica_argumentos(sys.argv[1:])
