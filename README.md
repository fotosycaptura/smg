# Smg
Manga downloader desde consola de fácil uso.

Se puede usar desde GNU/Linux como también Windows (al menos en teoría XD)

## Modo de uso

Para descargar un manga en particular:
```bash
smg.py url-manga
```
Para visualizar la ayuda 
```bash
smg.py -h
```
Para descargar un listado de mangas agregados en el config.ini:
```bash
smg.py -c
```
Esta aplicación requiere de:

* Requiere Python 3.9 en adelante
* bs4
* requests
* lxml
* configparser


Hay un archivo con los packages requeridos listos para instalar utilizando la orden:

```bash
pip install -r requirements.txt
```

## Archivo de configuración
El archivo de configuración se debe de llamar **config.ini**.
La estructura del archivo que se debe de crear para la configuración es la siguiente
```ini
; config.ini
[DEFAULT]
ruta_mangas = c:\Mangas\

[MANGAS]
listado_mangas = [
        {
            "nombre" : "manga-genial",
            "url_base" : "https://sitio-del-manga/manga-especifico/"
        }
    ]
[LEIDOS]
listado = [
    "nombre-manga-1",
    "nombre-manga-2"
    ]
```
### [DEFAULT]
**ruta_mangas**: indica la ruta física donde se guardarán los mangas. Esta ruta es absoluta y sin comillas.

### [MANGAS]

**listado_mangas**: es una lista en formato json que indica el nombre del manga, url a descargar.

### [LEIDOS]
**listado**: es una lista - array - que indica el nombre del manga ya leído, para no tener que desplegarlo en el módulo de __Leer_manga.py__
## Consideraciones
* Intente no utilizar caracteres especiales en el archivo de configuración.
* Probado en Windows 10/11
* Probado en OSX
* Probado en GNU/Linux

Cualquier duda o consulta no duden en consultar.

