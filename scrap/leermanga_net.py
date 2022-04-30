import bs4
import requests
import os
from varios import utilerias

class leermanga_net:
        def __init__(self, version, home_mangas, opciones, listado_mangas):
                self.home_mangas = home_mangas
                self.opciones = opciones
                self.listado_mangas = listado_mangas
                self.version = version

        def __descargar_imagenes_del_capitulo(self, ruta_manga, url_del_capitulo, capitulo):
                Varios = utilerias.utilerias(self.version)
                resultado = requests.get(url_del_capitulo, Varios.get_headers())
                sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
                capitulo_formateado = capitulo.zfill(3).replace('.', '-')

                imagenes = sopa.select(".img-fluid")
                # Se crean las carpetas respectivas para cada capítulo
                Varios.crear_carpeta_capitulo(ruta_manga, capitulo_formateado)

                # Se descargan las imagenes
                numeracion = 1
                for imagen in imagenes:
                        # Se extrae la imagen (url y nombre)
                        nombre_file = str(imagen['data-src'])
                        nombre_file = nombre_file[nombre_file.rindex('/')+1:]

                        extension = nombre_file[nombre_file.find('.'):]
                        nombre_file = str(numeracion).zfill(3) + extension 

                        # Se forma la ruta donde quedará finalmente
                        ruta = os.path.join(ruta_manga, capitulo_formateado, nombre_file)
                        ruta = os.path.abspath(ruta)
                        
                        # Se verifica si la imagen ya existía previamente
                        if not(os.path.exists(ruta)):
                                # Se extrae la imagen de forma binaria de la web
                                imagen_save = requests.get(imagen['data-src'].strip(), Varios.get_headers())
                        
                                # Se guarda la imagen en disco
                                f = open (ruta, 'wb')
                                f.write(imagen_save.content)
                                f.close()
                        numeracion = numeracion + 1

        def __get_capitulos(self, url_del_manga) -> list:
                """
                Se obtienen los números de capítulos y sus urls
                """
                Varios = utilerias.utilerias(self.version)
                directorio_capitulos = requests.get(url_del_manga, headers=Varios.get_headers())
                sopa_ini = bs4.BeautifulSoup(directorio_capitulos.text, 'lxml')
                all_capitulos = sopa_ini.select(".wp-manga-chapter")
                listado = []
                for item in all_capitulos:
                        qItem = item.find('a')
                        if (len(qItem['href']) > 1):
                                listado.append([qItem.text.strip(), qItem['href']])
                # Listado tendría el "número" de capítulo, y la url del capítulo
                return listado
                

        def descargar_solo(self, home_mangas, url_manga):
                Varios = utilerias.utilerias(self.version)
                if(url_manga.startswith("https://leermanga.net/manga/")):
                        nombre_manga = url_manga[27:].replace("/", "")
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
                                        self.__descargar_imagenes_del_capitulo(ruta_manga, url_capitulo, capitulo)
                print("")
                print("Finalizado. Presione [ENTER] para salir")
                input("> ")