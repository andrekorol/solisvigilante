import os
from lib import fitsread

top = os.getcwd()
for root, dirs, files in os.walk(top):
    for file in files:
        extension = os.path.splitext(os.path.abspath(file))[1]
        if extension == '.gz':
            fits_file = fitsread.ECallistoFitsFile(file)
            fits_file.set_file_path()
            fits_file.set_hdul_dataset()
            fits_file.plot_db_above_background()
