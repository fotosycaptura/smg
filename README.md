# Smg
Manga downloader desde consola de fácil uso.

Se puede usar desde GNU/Linux como también Windows.

* Requiere Python 3.9
* bs4
* requests
* json

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
```
### [DEFAULT]
**ruta_mangas**: indica la ruta física donde se guardarán los mangas. Esta ruta es absoluta y sin comillas.

### [MANGAS]

**listado_mangas**: es una lista en formato json que indica el nombre del manga, url a descargar.

## Consideraciones
* Intente no utilizar caracteres especiales en el archivo de configuración.
* Probado en Windows 10/11


Cualquier duda o consulta no duden en consultar.

