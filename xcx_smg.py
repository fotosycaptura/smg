#!/usr/bin/env python3
import os, os.path, sys, time, urllib, urllib.request
from xcx_smg_crConfig import ArchivoConfiguracion
##############################################################
# Programa desarrollado por XavierConX                       #
# Informar bugs o sugerencias a charsxavier@gmail.com        #
# Requiere Python 3.x para su funcionamiento                 #
##############################################################

#---------------- Configuracion Interna----------------------#
""" Esta seccion es para la configuracion interna del programa
OS sirve para indicar si es ejecutado desde plataforma Linux o Win32
Se debe sustituir Win32 por Linux si desea que funciona de forma adecuada en este sistema operativo.
topeManga, es usada de forma interna para contar la cantidad de archivos que se han descargado satisfactoriamente.
De esta forma se evita al usuario de indicar cuantas paginas componen el capitulo, dejando de forma automatica al sw contar.
"""

OS = "Win32"
smg_version = "1.2.5"
topeManga = 0

#---------------- Configuracion Interna----------------------#
def presentacion():
        print("******************************************************")
        print("             XCX Submanga Downloader                  ")
        print("                Version: " + smg_version + "          ")
        print("******************************************************")

def configurar(strCarpeta, strCap):
        """ Se encarga de crear la carpeta para el almacenamiento de las imagenes que componen el manga
        Como parametros recibe dos de tipo string, la primera es la carpeta principal que contendra el manga,
        la segunda es la carpeta oneshot o numero del capitulo de existir mas capitulos.
        Una de las mejoras incluidas en esta version, es la verificacion de la existencia antes de su creacion """
        
        retorno = 0
        try:
                strCarpeta = strCarpeta.replace(" ", "_")
                ordenCrearCarpeta = "mkdir " + strCarpeta
                if not(os.path.exists(strCarpeta) and os.path.isdir(strCarpeta)):
                        os.system(ordenCrearCarpeta)
                separador = "/"
                if (OS != "Linux"):
                        separador = "\\"
                os.system(ordenCrearCarpeta + separador + strCap.replace(" ", "_"))
                retorno = 1
        except:
                retorno = 0
        return (retorno)
        
def procesar(urlMangaImg, strRutaCap):
        """ Se encarga de crear la URL con la imagen para descargarla posteriormente.
        Realiza la llamada de la funcion que se encarga de descargar la imagen y
        nuevamente repite el proceso hasta que no existen imagenes para su descarga, con
        lo cual, finaliza el ciclo.
        Requiere de dos parametros: url, y el lugar donde se dejara el archivo descargado. """
        salir = 1
        iprc = 1
        while (salir != 0):
                strURL = urlMangaImg + str(iprc) + ".jpg"
                strNomFile = str(iprc) + ".jpg"
                if (descargarURL(strURL, strRutaCap + strNomFile) == 1):
                        iprc = iprc + 1
                else:
                        salir = 0
        global topeManga
        topeManga = (iprc - 1)
        return(1)

def descargarURL(strRutaUrl, strNombre):
        """ Es el encargado de descargar el archivo de la web si es que la conexion tuvo exito.
        En esta version, se verifica en la carpeta del capitulo si ya existia el archivo previamente.
        en caso de existir, se salta al siguiente. """
        retorno = 0
        try:
                if not(os.path.exists(strNombre) and os.path.isfile(strNombre)):
                        if (urllib.request.urlopen(strRutaUrl).getcode() == 200):
                                print("Descargando: " + strRutaUrl) # + " en: " + strNombre)
                                urllib.request.urlretrieve(strRutaUrl, strNombre)
                                retorno = 1
                else:
                        print("Ya existe: " + strNombre + ". [Saltado]")
                        retorno = 1
        except:
                retorno = 0
        return(retorno)

def run():
        """ Es el encargado de iniciar el proceso principal de recoleccion, ejecucion de todos los modulos
            En esta version, se corrigen los espacios para las carpetas dentro del manga, reemplazandolos con guiones bajos _ """ 
        presentacion()
        print("Leyendo archivo de configuracion...")
        try:
                xcxConfig = ArchivoConfiguracion.leerConfigArchivo()
        except:
                print("Hubo un problema al intentar leer los datos.")
                exit()
        print("Cargando...")
        if (len(xcxConfig) > 0):
                print("Se encontraron " + str(len(xcxConfig)) + " mangas en el archivo de configuracion para descargar.")
                for i in xcxConfig:
                        lArreglo = i.split(",")
                        if (len(lArreglo) == 3):
                                print("Procesando ", lArreglo[1], " capitulo ", lArreglo[0])
                                print("Creando carpetas")
                                if (configurar(lArreglo[1].lstrip(" "), lArreglo[0]) == 1):
                                        strURL = lArreglo[2].replace(" ", "")
                                        strURL = strURL.replace("\n", "")
                                        strRutaCap = lArreglo[1].lstrip(" ")
                                        strSeparador = "/"
                                        if (OS != "Linux"):
                                                strSeparador = "\\"
                                        strRutaCap = strRutaCap.replace(" ", "_") + strSeparador + lArreglo[0].replace(" ", "_") + strSeparador
                                        print("Comprobando...")
                                        if (procesar(strURL, strRutaCap) == 1):
                                                print("...")
                                        else:
                                                print("La operación no pudo ser completada... :(")
                                                break
                                else:
                                        print("Hubo un problema en el modulo de [configurar] para la creacion de carpetas")
                        else:
                                print("No se pudo procesar una de las lineas del archivo de configuracion. ¿Estan correctas las lineas?")
        print("Finalizado. Presione [ENTER] para salir")
        input("> ")
        

# Para ejecutar desde la linea de comandos
if __name__ == '__main__':
        run()
