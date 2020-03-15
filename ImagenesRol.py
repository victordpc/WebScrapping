from bs4 import BeautifulSoup
import errno
import os
from tqdm import tqdm
import urllib
import urllib.request

data = dict()
data['Mapping Objects'] = '/index.php?/category/2'
data['Maps'] = '/index.php?/category/54'

baseUrl = 'http://rpgmapshare.com/piwigo/gallery'
urlDescarga = 'http://rpgmapshare.com/piwigo/gallery/action.php?id={numero}&part=e&download'
destPath = 'c:\\ImagenesRol'
out_file = 'c:\\ImagenesRol\\datos.csv'
datos_descarga = list()


def main():
    get_data()


def get_data():
    for k, v in tqdm(data.items(),desc='Descarga'):
        procesarPagina(v, k)

    header_data = ['Ruta', 'Enlace']

    with open(out_file, 'w') as the_file:
        header_data.append('\n')
        header_text = ';'.join(header_data)
        the_file.write(header_text)

        for line in tqdm(datos_descarga, desc='Guardando datos'):
            line.append('\n')
            line = list(map(lambda x: str(x), line))
            text = ';'.join(line)
            the_file.write(text)


def procesarPagina(url, ruta) -> list:
    html = urllib.request.urlopen(joinUrl(baseUrl, url))
    soup = BeautifulSoup(html.read(), 'html.parser')

    content = soup.findAll("ul", {"class": "thumbnailCategories"})
    if len(content) != 0:
        procesarColeccion(soup, ruta)

    content = soup.find_all("ul", {"class": "thumbnails"})
    if len(content) != 0:
        procesarElementos(soup, ruta)


def procesarColeccion(soup, ruta):
    content = soup.findAll("ul", {"class": "thumbnailCategories"})[0]
    content = list(filter(lambda x: x != '\n', content))

    for enlace in tqdm(content, desc=ruta):
        url = enlace.a.get("href", None)
        carpeta = enlace.text.strip().split('\n')[0].strip().replace(' ', '_')
        procesarPagina(url, os.path.join(ruta, carpeta))


def procesarElementos(soup, ruta):
    carpeta_actual = os.path.join(destPath, ruta)
    create_folder(carpeta_actual)

    content = soup.find_all("ul", {"class": "thumbnails"})[0]
    content = list(filter(lambda x: x != '\n', content))

    for elemento in tqdm(content):
        name = elemento.text.strip().replace(' ', '_').replace(
            '/', '_').replace('\\', '_').replace(':', '_').replace(
            '?', '_').replace('*', '_').replace('\n', '_').replace(
            '\'', '_').replace('\"', '_')
        url = elemento.a.get("href", None).split('/')[1]
        url = urlDescarga.format(numero=url)
        img = urllib.request.urlopen(url)

        extension = '.png'
        for cabecera in img.headers._headers:
            if cabecera[0] == 'Content-Type':
                if cabecera[1].find('/') != -1:
                    if cabecera[1].split('/')[1] == 'png':
                        extension = '.png'
                    elif cabecera[1].split('/')[1] == 'jpeg':
                        extension = '.jpg'
                    elif cabecera[1].split('/')[1] == 'zip':
                        extension = '.zip'
                    elif cabecera[1].split('/')[1] == 'pdf':
                        extension = '.pdf'
                    elif cabecera[1].split('/')[1] == 'gif':
                        extension = '.gif'
                    else:
                        print(cabecera)
                else:
                    print(cabecera)

        ruta_imagen = os.path.join(
            carpeta_actual, name + extension)

        datos_descarga.append([ruta_imagen, url])

    content = soup.find_all("span", {"class": "navPrevNext"})

    for elemento in content:
        if elemento.text.upper().find('Next'.upper()) != -1:
            if elemento.a != None:
                url = elemento.a.get("href", None)
                procesarPagina(url, ruta)


def create_folder(path: str):
    '''
    Create folder.

    Create folder recived, if obtains a relative path, try to create 
    it in the current directory if not exists, if the folder already
    exists do nothing.

    Parameters
        path,   path of the objetive folder
    '''

    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def joinUrl(first, second):
    resultado = ''
    if first[-1] != '/' and second[0] != '/':
        resultado = first + '/' + second
    elif first[-1] == '/' and second[0] == '/':
        resultado = first[:-1] + second
    elif first[-1] != '/' or second[0] != '/':
        resultado = first + second
    return resultado


if __name__ == "__main__":
    main()
