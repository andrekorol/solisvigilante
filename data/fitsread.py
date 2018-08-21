from astropy.io import fits


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
