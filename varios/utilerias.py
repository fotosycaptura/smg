import os
class utilerias:
    def __init__(self, version):
         self.version = version
    # Print iterations progress
    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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

    def presentacion(self):
        print("******************************************************")
        print("                 SAbManga Downloader                  ")
        print("                Version: " + self.version + "         ")
        print("******************************************************")

    def modo_de_uso(self):
        print('Permite descargar un manga de ---Manga')
        print('Modo de uso:')
        print('smg.py url-manga     - Descarga el manga en cuestión.')
        print('smg.py -c            - Descarga listado de mangas definidos en config.ini (Deprecado)')
        print('smg.py -h            - Muestra esta ayuda.')

    def crear_carpeta_manga(self, home_mangas, nombre_manga) -> str:
        """
        Crea la carpeta que contendrá los capítulos del manga
        Y retorna la ruta física donde serán alojados
        """
        nombre_manga_filtrado = nombre_manga.replace('?', '')
        nombre_manga_filtrado = nombre_manga_filtrado.replace(':', '')
        ruta_manga = os.path.join(home_mangas, nombre_manga_filtrado)
        # print(f"Creando carpeta en {ruta_manga}")
        if not(os.path.exists(ruta_manga) and os.path.isdir(ruta_manga)):
                os.mkdir(os.path.abspath(ruta_manga))
        return ruta_manga

    def crear_carpeta_capitulo(self, ruta_manga, capitulo):
        if not(os.path.exists(os.path.join(ruta_manga, capitulo)) and os.path.isdir(os.path.join(ruta_manga, capitulo))):
                os.mkdir(os.path.join(ruta_manga, capitulo))

    def get_headers(self):
        return {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'}