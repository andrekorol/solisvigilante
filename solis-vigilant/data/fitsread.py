import os
import urllib.error
import urllib.request
from astropy.io import fits


def download_from_url(url):
    """
    Downloads the file found at the given url

    :param url: url string of a file to be downloaded
    :returns: the name of the file downloaded from the given url
    :raises urllib.error.URLError: raises an exception when an invalid url is given as argument
    """
    filename = url.split('/')[-1]
    try:
        downloaded_file = urllib.request.urlretrieve(url, filename)
        urllib.request.urlcleanup()
    except urllib.error.URLError as e:
        urllib.request.urlcleanup()
        print(f'{url}: Name or service not known')
        raise e

    return downloaded_file[0]


class FitsFile(object):
    """Class for reading FITS files from an url"""
    def __init__(self, url):
        self.url = url
        self.filename = download_from_url(self.url)
        self.hdul = fits.open(self.filename)

    def print_fits_hdul_info(self):
        self.hdul.info()

    def close_hdul(self):
        self.hdul.close()


fits_test_file = FitsFile('http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_'
                          '20110809_083004_24.fit.gz')
fits_test_file.print_fits_hdul_info()
fits_test_file.close_hdul()

os.remove(fits_test_file.filename)
