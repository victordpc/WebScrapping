import itertools
import os
from tqdm import tqdm
import urllib
import urllib.request
import errno
import concurrent.futures


out_file = 'c:\\ImagenesRol\\datos.csv'
errores = list()


def main():
    datos = list()
    datos.append(dict())
    i = 0
    max_elem = 1000
    parte = 0
    total = 0

    with open(out_file, 'r') as the_file:
        the_file.readline()

        for line in tqdm(the_file,desc='Read file'):
            total += 1
            line = line.split(';')
            ruta_imagen = line[0]
            url = line[1]

            if i == max_elem:
                i = 0
                parte += 1
                datos.append(dict())

            (datos[parte])[ruta_imagen] = url
            i += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(download_data, datos)

    # dict_data=dict()
    # with open(out_file, 'r') as the_file:
    #     the_file.readline()

    #     for line in tqdm(the_file,desc='Read file'):
    #         total += 1
    #         line = line.split(';')
    #         ruta_imagen = line[0]
    #         url = line[1]

    #         dict_data[ruta_imagen] = url
    #         i += 1

    # with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    #     executor.map(download_element, dict_data.items())

def download_element(element):
    try:
        ruta_imagen = element[0]
        url = element[1]
        create_folder(os.path.dirname(ruta_imagen))
        if not os.path.exists(ruta_imagen):
            descarga_fichero(ruta_imagen, url)
    except:
        errores.append( element[0])


def download_data(datos_descarga):
    for k, v in tqdm(datos_descarga.items(), desc='Descarga'):
        try:
            ruta_imagen = k
            url = v
            create_folder(os.path.dirname(ruta_imagen))
            if not os.path.exists(ruta_imagen):
                descarga_fichero(ruta_imagen, url)
        except:
            errores.append(k)


def descarga_fichero(ruta_imagen, url):
    img = urllib.request.urlopen(url)
    manf = open(ruta_imagen, "wb")
    tam = 0
    while True:
        info = img.read(100000)
        if len(info) < 1:
            break
        tam = tam + len(info)
        manf.write(info)
    manf.close()


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


if __name__ == "__main__":
    main()
    print('Errores encontrados \n')
    print(errores)
    print('\n\nFin\n\n')
