import os
import urllib.error
import urllib.request
from astropy.io import fits


def download_from_url(url):
    """Assumes: url is a string

    Returns the name of the file downloaded from the given url"""
    filename = url.split('/')[-1]
    try:
        downloaded_file = urllib.request.urlretrieve(url, filename)
        urllib.request.urlcleanup()
    except urllib.error.URLError:
        urllib.request.urlcleanup()
        print(f'{url}: Name or service not known')
        return
    return downloaded_file[0]


class FitsFile(object):
    """Class for reading FITS files"""
    def __init__(self, filename):
        self.filename = filename

    def print_fits_hdul_info(self):
        with fits.open(self.filename) as hdul:
            hdul.info()


file = download_from_url('http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_'
                         '20110809_083004_24.fit.gz')
print(file)

fits_test_file = FitsFile(file)
fits_test_file.print_fits_hdul_info()

os.remove(file)
