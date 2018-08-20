import aplpy
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
    """Main entry point to the FITS file format"""
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def open(filename):
        hdul = fits.open(filename)
        return hdul

    @staticmethod
    def edit(filename):
        hdul = fits.open(filename, 'update')
        return hdul

    @staticmethod
    def close(hdul):
        hdul.close()


url_list = ['http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'
            '2011/08/09/BLEN7M_20110809_083004_24.fit.gz',
            'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'
            '2011/08/09/BLEN7M_20110809_083005_25.fit.gz']

for url_link in url_list:
    fits_filename = download_from_url(url_link)
    gc = aplpy.FITSFigure(fits_filename)
    gc.show_colorscale()
    gc.save(fits_filename.split('.')[0] + '.png')
    os.remove(fits_filename)
