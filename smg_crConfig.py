#!/usr/bin/env python3
import os, os.path, sys
##############################################################
# Requiere Python 3.x para su funcionamiento                 #
##############################################################
class ArchivoConfiguracion():
    def leerConfigArchivo():
        """ Esta clase se encarga solamente de leer el archivo de
        links. Si por alguna razon viene la linea comentada con // al
        comienzo, debiera no entregar esas lineas """
        f = open("smg_config.txt", "r")
        lineas = f.readlines()
        f.close()
        if (len(lineas) > 0):
            lineas2 = lineas
            i = 0
            tope = len(lineas)
            while (i < tope):
                encontrado = 0
                linea = lineas[i].split(",")
                if (len(linea) < 3):
                    lineas2.remove(lineas[i])
                    encontrado = 1
                if (encontrado == 0 and linea[0].find("//") > -1):
                    lineas2.remove(lineas[i])
                    encontrado = 1
                    
                if (encontrado == 1):
                    i = 0
                    tope = tope - 1
                else:
                    i = i + 1
        return(lineas2)
    def crearConfigArchivo():
        try:
            if not (os.path.exists("smg_config.txt")):
                file = open("smg_config.txt", "w")
                file.write("//<-- Línea de comentario" + os.linesep)
                file.write("//Capítulos, Nombre Manga, URL" + os.linesep)
                file.write("//01, Mi Manga, http://www....")
                file.close()
                print("Archivo de configuración creado.")
                print("Modifíquelo para su uso.")
        except:
            print("No se pudo crear el archivo. ¿Medio de solo lectura?")
    #leerConfigArchivo()
