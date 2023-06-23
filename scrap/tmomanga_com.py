import bs4
import requests
import os
from varios import utilerias
import numpy as np

class tmomanga_com:
    def __init__(self, version, home_mangas, opciones, listado_mangas):
                self.home_mangas = home_mangas
                self.opciones = opciones
                self.listado_mangas = listado_mangas
                self.version = version

    def __descargar_imagenes_del_capitulo(self, ruta_manga, url_del_capitulo, capitulo):
        Varios = utilerias.utilerias(self.version)
        resultado = requests.get(url_del_capitulo, headers=Varios.get_headers())
        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

        #imagenes = sopa.select(".tab-content")
        imagenes = sopa.find("div", {"id": "images_chapter"})
        
        # Se descargan las imagenes
        contador_imagen = 0
        for imagen in imagenes.select('img'):
                # Se extrae la imagen (url y nombre)
                nombre_file = str(imagen['data-src'])
                # print(imagen['data-src'])
                nombre_file = str(contador_imagen).zfill(3) + '.jpg'
                if (imagen['data-src'] != '/discord.jpg'):
                    # Se forma la ruta donde quedará finalmente
                    ruta = os.path.join(ruta_manga, capitulo, nombre_file)
                    ruta = os.path.abspath(ruta)
                    
                    # Se verifica si la imagen ya existía previamente
                    if not(os.path.exists(ruta)):
                            # Se extrae la imagen de forma binaria de la web
                            imagen_save = requests.get(imagen['data-src'], Varios.get_headers())
                    
                            # Se guarda la imagen en disco
                            f = open (ruta, 'wb')
                            f.write(imagen_save.content)
                            f.close()
                contador_imagen = contador_imagen + 1

    def __get_capitulos(self, url_del_manga, nombre_manga) -> list:
        Varios = utilerias.utilerias(self.version)
        print(f"url del manga: {url_del_manga}")
        # Se obtienen los números de capítulos y sus urls
        resultado = requests.get(url_del_manga, headers=Varios.get_headers())
        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
        #capitulos = sopa.find("div", {"id": "chapterlist"})
        capitulos = sopa.select('.sub-chap.list-chap')
        #print(capitulos[0].select('a')[0]['href'])
        listado = []
        for capitulo in capitulos:
            cap = capitulo.select('a')
            for item in cap:
                #print(item['href'])
                #print(item.getText().strip())
                nombre_capitulo = item.getText().strip().replace(nombre_manga, '').strip()
                # nombre_capitulo = nombre_capitulo.replace('.', '')
                nombre_capitulo = nombre_capitulo.replace('-', '')
                nombre_capitulo = nombre_capitulo.replace('?', '')
                #nombre_capitulo = nombre_capitulo.replace('.', '')
                nombre_capitulo = nombre_capitulo.replace('Capítulo', '').strip()
                url = item['href']
                try:
                    nombre_float = float(nombre_capitulo)
                    if (nombre_float.is_integer()):
                        listado.append([str(int(nombre_float)).zfill(2), url])
                    else:
                        listado.append([str(nombre_float).zfill(4), url])
                except:
                    pass
        return listado
    
    def descargar_solo(self, url_manga):
        Varios = utilerias.utilerias(self.version)
        if(url_manga.startswith("https://tmomanga.com/manga/")):
            # Se busca el nombre del manga en cuestión a descargar
            resultado = requests.get(url_manga, headers=Varios.get_headers())
            sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
            manhwas = sopa.select('h1')
            #print(f"Test: {manhwas}")
            nombre_manga = manhwas[0].getText()
            print(f"Descargando {nombre_manga}")
            ruta_manga = Varios.crear_carpeta_manga(self.home_mangas, nombre_manga)
            lst_capitulos_del_manga = self.__get_capitulos(url_manga, nombre_manga)
            lst_capitulos_del_manga.sort()
            # print(lst_capitulos_del_manga)
            # Se procede con el ciclo para la descarga
            inicial = 1
            final = len(lst_capitulos_del_manga)
            for capitulo, url_capitulo in lst_capitulos_del_manga:
                    # Por cada capítulo:
                    # - Crear carpeta del capítulo, si es necesario
                    # - para el capítulo, descargar las imagenes, si es necesario
                    Varios.printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                    inicial = inicial + 1
                    if (len(capitulo) > 0):
                        Varios.crear_carpeta_capitulo(ruta_manga, capitulo)
                        self.__descargar_imagenes_del_capitulo(ruta_manga, url_capitulo, capitulo)
        print('Finalizado.')
        input("> ")