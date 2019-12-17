#!/usr/bin/env python3
import os, os.path, sys, time, urllib, urllib.request
from smg_crConfig import ArchivoConfiguracion
##############################################################
# Requiere Python 3.x para su funcionamiento                 #
##############################################################

#---------------- Configuracion Interna----------------------#
""" Esta seccion es para la configuracion interna del programa
topeManga, es usada de forma interna para contar la cantidad de archivos que se han descargado satisfactoriamente.
De esta forma se evita al usuario de indicar cuantas paginas componen el capitulo, dejando de forma automatica al sw contar.
smg_Lib, es la ruta o librería en donde están almacenados los mangas.
"""

smg_version = "1.2.8"
topeManga = 0
smg_Lib = "Mngs"

#---------------- Configuracion Interna----------------------#
def presentacion():
        print("******************************************************")
        print("                 Mmanga Downloader                    ")
        print("                Version: " + smg_version + "          ")
        print("******************************************************")

def configurar(strCarpeta, strCap):
        """ Se encarga de crear la carpeta para el almacenamiento de las imagenes que componen el manga
        Como parametros recibe dos de tipo string, la primera es la carpeta principal que contendra el manga,
        la segunda es la carpeta oneshot o numero del capitulo de existir mas capitulos.
        Una de las mejoras incluidas en esta version, es la verificacion de la existencia antes de su creacion.
        Retorna 1 (true) si todo es correcto
        Retorno 0 (false) si hubo algún problema """
        
        retorno = 0
        try:
                #Se reemplazan los espacios por guiones
                strCarpeta = strCarpeta.replace(" ", "_")
                #Se genera la ruta usando el smg_Lib y el nombre del manga
                mkdirec = os.path.join(smg_Lib, strCarpeta)
                #Si la ruta no existe
                if not(os.path.exists(mkdirec) and os.path.isdir(mkdirec)):
                        #Se crea
                        os.mkdir(mkdirec)
                retorno = 1
        except OSError as error:
                #print("Error: " + error)
                retorno = 0
        return (retorno)
        
def procesar(urlMangaImg, strRutaCap):
        """ Se encarga de crear la URL con la imagen para descargarla posteriormente.
        Realiza la llamada de la funcion que se encarga de descargar la imagen y
        nuevamente repite el proceso hasta que no existen imagenes para su descarga, con
        lo cual, finaliza el ciclo.
        Requiere de dos parametros: url, y el lugar donde se dejara el archivo descargado.
        procesar siempre regresa 1 """
        salir = 1
        iprc = 1
        while (salir != 0):
                strNomFile = str(iprc).zfill(2) + ".jpg"
                #se procede a descargar
                if (descargarURL(urlMangaImg, iprc, os.path.join(strRutaCap, strNomFile)) == 1):
                        iprc = iprc + 1
                else:
                        #no hay nada más que descargar
                        salir = 0
        global topeManga
        topeManga = (iprc - 1)
        return(1)

def descargarURL(strRutaUrl, numContador, strNombre):
        """ Es el encargado de descargar el archivo de la web si es que la conexion tuvo exito.
        En esta version, se verifica en la carpeta del capitulo si ya existia el archivo a descargar previamente.
        en caso de existir, se salta al siguiente.
        2019-12-17-12.13
        strRutaUrl recibe sólamente hasta /chapters/1/
        la imagen se le concatenará desde numContador.
        Se trabajará en una versión para, si no encuentra el 01.jpg, intentar con 1.jpg.
        """
        retorno = 0
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name': 'Niño Rata', 'location': 'Quete', 'language': 'Python' }
        headers = {'User-Agent': user_agent}

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')

        try:
                if not(os.path.exists(strNombre) and os.path.isfile(strNombre)):
                        strIntento01 = strRutaUrl + str(numContador).zfill(2) + ".jpg"
                        strIntento02 = strRutaUrl + str(numContador) + ".jpg"
                        #print("Ruta 01: " + strIntento01)
                        #print("Ruta 02: " + strIntento02)
                        resp = 404
                        req = urllib.request.Request(strIntento01, data, headers)
                        try:
                                resp = urllib.request.urlopen(req).getcode()
                        except:
                                pass
                        if (resp == 200):
                                print("Descargando: " + strIntento01)
                                g = urllib.request.urlopen(req)
                                with open(strNombre, 'b+w') as f:
                                        f.write(g.read())
                                retorno = 1
                        else:
                                #Se realiza segundo intento
                                #print("Se detectó una anomalía en la fuerza. Segundo intento...")
                                req = urllib.request.Request(strIntento02, data, headers)
                                resp = urllib.request.urlopen(req).getcode()
                                if (resp == 200):
                                        print("Descargando: " + strIntento02)
                                        g = urllib.request.urlopen(req)
                                        with open(strNombre, 'b+w') as f:
                                                f.write(g.read())
                                        retorno = 1
                else:
                        print("Ya existe: " + strNombre + ". [Saltado]")
                        retorno = 1
        except:
            #print("Algo ocurrio en descargarURL: ")
            retorno = 0
        return(retorno)
    
def crearCarpetaCapitulo(strRutaCapitulo):
    if not(os.path.exists(strRutaCapitulo) and os.path.isdir(strRutaCapitulo)):
        os.mkdir(strRutaCapitulo)
    
def run():
        """ Es el encargado de iniciar el proceso principal de recoleccion, ejecucion de todos los modulos
            En esta version, se corrigen los espacios para las carpetas dentro del manga, reemplazandolos con guiones bajos _ """ 
        presentacion()
        print("Leyendo archivo de configuracion...")
        try:
                xcxConfig = ArchivoConfiguracion.leerConfigArchivo()
        except:
                print("Hubo un problema al intentar leer los datos.")
                print("Creando archivo de datos inicial")
                ArchivoConfiguracion.crearConfigArchivo()
                exit()
        print("Cargando...")
        if (len(xcxConfig) > 0):
                print("Se encontraron " + str(len(xcxConfig)) + " mangas en el archivo de configuracion para descargar.")
                for i in xcxConfig:
                        lArreglo = i.split(",")
                        if (len(lArreglo) == 3):
                                #Procesando "Nombre manga capítulo número"
                                #Habría que analizar si en lArreglo[0] no viene un guión.
                                #De ser asi, significa que habría que iterar entre el primer dígito hasta el último dígito
                                #es decir (cap inicial ... capítulo final)
                                lMasCap = str(lArreglo[0]).split("-")
                                if (len(lMasCap) == 2):
                                        #Se procede a iterar
                                        print("Se descargará el manga entre capítulos: " + str(lMasCap[0]) + " hasta " + str(lMasCap[1]))
                                        for intCapActual in(range(int(lMasCap[0]), int(lMasCap[1]) + 1)):
                                                print("Procesando manga: " + lArreglo[1] + " capitulo " + str(intCapActual).zfill(2) + "/" + str(lMasCap[1]))
                                                print("Creando carpetas")
                                                if (configurar(lArreglo[1].lstrip(" "), intCapActual) == 1):
                                                        #Se extrae la url sin espacios
                                                        strURL = lArreglo[2].replace(" ", "")
                                                        #se extrae los enters o retornos
                                                        strURL = strURL.replace("\n", "")
                                                        #Se genera la carpeta del capítulo dentro de la librería de mangas
                                                        strRutaCapi = os.path.join(smg_Lib, lArreglo[1].lstrip(" "))
                                                        #Se genera la ruta de la carpeta del capítulo
                                                        strRutaCapi = strRutaCapi.replace(" ", "_") 
                                                        strRutaCapi = os.path.join(strRutaCapi, str(intCapActual).zfill(2))
                                                        print("Comprobando...")
                                                        #Se crea la carpeta del capítulo
                                                        crearCarpetaCapitulo(strRutaCapi)
                                                        #No olvidar que hay que agregar el n del cap a strUrl
                                                        strURL = strURL + str(intCapActual) + "/"
                                                        procesar(strURL, strRutaCapi)
                                else:
                                        print("Procesando manga: " + lArreglo[1] + " capitulo " + lArreglo[0])
                                        print("Creando carpetas")
                                        if (configurar(lArreglo[1].lstrip(" "), lArreglo[0]) == 1):
                                                
                                                strURL = lArreglo[2].replace(" ", "")
                                                strURL = strURL.replace("\n", "")
                                                strRutaCap = os.path.join(smg_Lib, lArreglo[1].lstrip(" "))
                                                strRutaCap = strRutaCap.replace(" ", "_")
                                                strRutaCap = os.path.join(strRutaCap, lArreglo[0].replace(" ", "_"))
                                                
                                                print("Comprobando...")
                                                #Se crea la carpeta del capítulo
                                                crearCarpetaCapitulo(strRutaCap)
                                                #No olvidar que hay que agregar el n del cap a strUrl
                                                intCapActual = int(lArreglo[0])
                                                strURL = strURL + str(intCapActual) + "/"
                                                procesar(strURL, strRutaCap)
                                                print("...")
                                        else:
                                                print("Hubo un problema en el modulo de [configurar] para la creacion de carpetas")
                        else:
                                print("No se pudo procesar una de las lineas del archivo de configuracion. ¿Estan correctas las lineas?")
        print("Finalizado. Presione [ENTER] para salir")
        input("> ")
        

# Para ejecutar desde la linea de comandos
if __name__ == '__main__':
        run()
