import getopt
import sys

from src.download_files import download_files
from src.ImagenesRol import scrap_images


def main(argv):
    """
    Main function.
    """

    helpUsage = 'web_scrapping.py [-h ][-s | -d] \n'\
        '  -h show this message\n' \
        '  -s scrap the web\n' \
        '  -d download the data\n'
    download = False
    scrap = False

    try:
        opts, _ = getopt.getopt(argv, "hsd", [])
        if len(opts) < 1 or len(opts) > 3:
            raise getopt.GetoptError(msg='Incorrect param number')
    except getopt.GetoptError as err:
        print(f'Error in the execution: {err.msg}')
        print(helpUsage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpUsage)
            sys.exit()
        elif opt in ("-s"):
            scrap = True
        elif opt in ("-d"):
            download = True

    if scrap:
        scrap_images()
    if download:
        download_files()
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
