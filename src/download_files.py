import itertools
import os
from tqdm import tqdm
import urllib
import urllib.request
import errno
import concurrent.futures


class download_files():

    def __init__(self):
        self.out_file = 'c:\\ImagenesRol\\datos.csv'
        self.errores = list()
        self._main()

        if len(self.errores)>0:
            print('Errors founded:\n')
            print(self.errores)
        print('\n\nThe end for now :3\nA vast world awaits, choose your favorite armour and the sharpest weapon...\n\"There and Back Again\"\nHappy game\n\n')

    def _main(self):
        datos = list()
        datos.append(dict())
        i = 0
        max_elem = 1000
        parte = 0
        total = 0

        with open(self.out_file, 'r') as the_file:
            the_file.readline()

            for line in tqdm(the_file, desc='Read file'):
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
            executor.map(self.download_data, datos)

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

    def download_element(self, element):
        try:
            ruta_imagen = element[0]
            url = element[1]
            self.create_folder(os.path.dirname(ruta_imagen))
            if not os.path.exists(ruta_imagen):
                self.descarga_fichero(ruta_imagen, url)
        except:
            self.errores.append(element[0])

    def download_data(self, datos_descarga):
        for k, v in tqdm(datos_descarga.items(), desc='Descarga'):
            try:
                ruta_imagen = k
                url = v
                self.create_folder(os.path.dirname(ruta_imagen))
                if not os.path.exists(ruta_imagen):
                    self.descarga_fichero(ruta_imagen, url)
            except:
                self.errores.append(k)

    def descarga_fichero(self, ruta_imagen, url):
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

    def create_folder(self, path: str):
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
    download_files()
