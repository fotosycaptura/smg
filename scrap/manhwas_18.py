import bs4
import requests
import os
from varios import utilerias
import numpy as np

class manhwas_18:
    def __init__(self, version, home_mangas, opciones, listado_mangas):
                self.home_mangas = home_mangas
                self.opciones = opciones
                self.listado_mangas = listado_mangas
                self.version = version

    def __descargar_imagenes_del_capitulo(self, ruta_manga, nombre_manga, url_del_capitulo, capitulo):
        Varios = utilerias.utilerias(self.version)
        cookies = {'aep_usuc_f': 'site=rus&c_tp=USD&region=IE&b_locale=ru_RU'}
        s = requests.Session()

        s.headers.update({'referer': url_del_capitulo})
        r = s.get(url_del_capitulo, headers=Varios.get_headers(), cookies=cookies)

       
        resultado = r # requests.get(url_del_capitulo, headers=get_headers())
        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
        capitulo_formateado = capitulo.replace('.', '-')
        capitulo_formateado = capitulo_formateado.replace('?', '')
        
        capitulo_formateado = capitulo_formateado.replace(nombre_manga, '')
        capitulo_formateado = capitulo_formateado.strip()
        # Se crean las carpetas respectivas para cada capítulo
        # print(f'Creando {ruta_manga} y dentro {capitulo_formateado}')
        Varios.crear_carpeta_capitulo(ruta_manga, capitulo_formateado)
        # Se descargan las imagenes
        contador_imagen = 0

        imagenes = sopa.findAll('img')
        #print(str(imagenes[4]).find('data-src'))

        for imagen in imagenes:
            if (str(imagen).find('data-src') > 0):
                # Se extrae la imagen (url y nombre)
                nombre_file = str(imagen['data-src'])
                # print(imagen['src'])
                nombre_file = str(contador_imagen).zfill(3) + '.jpg'
                # Se forma la ruta donde quedará finalmente
                ruta = os.path.join(ruta_manga, capitulo_formateado, nombre_file)
                ruta = os.path.abspath(ruta)
                # Se verifica si la imagen ya existía previamente
                if not(os.path.exists(ruta)):
                    # Se extrae la imagen de forma binaria de la web
                    imagen_save = s.get(imagen['src'], headers=Varios.get_headers(), cookies=cookies)
                    # Se guarda la imagen en disco
                    f = open (ruta, 'wb')
                    f.write(imagen_save.content)
                    f.close()
            contador_imagen = contador_imagen + 1

    def __get_capitulos(self, url_del_manga) -> list:
        print(f"url del manga: {url_del_manga}")
        # Se obtienen los números de capítulos y sus urls
        resultado = requests.get(url_del_manga)
        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
        capitulos = sopa.select('.chapter-name')
        listado = []
        for capitulo in capitulos:
            titulo = capitulo.getText()
            listado.append([titulo.strip(), capitulo['href']])
        return listado
    
    def descargar_solo(self, url_manga):
                Varios = utilerias.utilerias(self.version)
                if(url_manga.startswith("https://manhwa18.cc/webtoon/")):
                        
                        # Se busca el nombre del manga en cuestión a descargar
                        resultado = requests.get(url_manga)
                        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
                        manhwas = sopa.select('h1')
                        nombre_manga = manhwas[0].getText().replace('18+', '').strip()
                
                        print(f"Descargando {nombre_manga}")
                        ruta_manga = Varios.crear_carpeta_manga(self.home_mangas, nombre_manga)
                        lst_capitulos_del_manga = self.__get_capitulos(url_manga)
                        lst_capitulos_del_manga.sort()
                        # Se procede con el ciclo para la descarga
                        inicial = 1
                        final = len(lst_capitulos_del_manga)
                        for capitulo, url_capitulo in lst_capitulos_del_manga:
                                Varios.printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                                inicial = inicial + 1
                                if (len(capitulo) > 0):
                                        #print(f'La llamada es {ruta_manga}, {url_capitulo}')
                                        self.__descargar_imagenes_del_capitulo(ruta_manga, nombre_manga, 'https://manhwa18.cc' + url_capitulo, capitulo)
                print("")
                print("Finalizado. Presione [ENTER] para salir")
                input("> ")