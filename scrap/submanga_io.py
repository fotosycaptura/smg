import bs4
import requests
import os
from varios import utilerias

class submanga:
        def __init__(self, version, home_mangas, opciones, listado_mangas):
                self.home_mangas = home_mangas
                self.opciones = opciones
                self.listado_mangas = listado_mangas
                self.version = version

        def __descargar_imagenes_del_capitulo(self, ruta_manga, url_del_capitulo, capitulo):
                Varios = utilerias.utilerias(self.version)
                resultado = requests.get(url_del_capitulo)
                sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
                capitulo_formateado = capitulo.zfill(3).replace('.', '-')

                imagenes = sopa.select(".wp-manga-chapter-img")
                # Se crean las carpetas respectivas para cada capítulo
                Varios.crear_carpeta_capitulo(ruta_manga, capitulo_formateado)

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

        def __get_capitulos(self, url_del_manga) -> list:
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

        def descargar_por_config(self):
                """ 
                Es el encargado de iniciar el proceso principal de recoleccion, ejecucion de todos los modulos
                En esta version, se corrigen los espacios para las carpetas dentro del manga, reemplazandolos con guiones bajos _ 
                """ 
                Varios = utilerias.utilerias(self.version)
                print(f"Opción deprecada para este conector. Se encontraron {len(self.listado_mangas)} mangas para descargar en config.ini...")
                if len(self.listado_mangas) > 0:
                        print("Procesando...")
                        for manga in self.listado_mangas:
                                url_base = manga['url_base']
                                if (url_base.startswith("https://www3.tumangaonline.site/manga/")):
                                        # Por cada manga se crea su carpeta, si es que no existía antes
                                        
                                        ruta_manga = Varios.crear_carpeta_manga(self.home_mangas, manga["nombre"])
                                        
                                        # Se obtienen los capítulos en formato["numero", "url"]
                                        listado_capitulos =  self.__get_capitulos(url_base)
                                        
                                        # Se procede con el ciclo para la descarga
                                        inicial = 1
                                        final = len(listado_capitulos)
                                        for capitulo, url_capitulo in listado_capitulos:
                                                Varios.printProgressBar(inicial, final, prefix = 'Descarga:', suffix = 'Completado', length = 30)
                                                inicial = inicial + 1
                                                if (len(capitulo) > 0):
                                                        self.__descargar_imagenes_del_capitulo(ruta_manga, url_capitulo, capitulo)
                                else:
                                        print(f'Url ({url_base}) no procesada.')
                        print("")
                        print("Finalizado. Presione [ENTER] para salir")
                        input("> ")

        def descargar_solo(self, home_mangas, url_manga):
                Varios = utilerias.utilerias(self.version)
                if(url_manga.startswith("https://www3.tumangaonline.site/manga/")):
                        nombre_manga = url_manga[25:].replace("/", "")
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