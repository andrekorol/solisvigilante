import os
from Lib.urlget import download_from_url
from Lib import fitsread

data_archives = "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2012/08/12/"
file_list = ["BLEN7M_20120812_140000_25.fit.gz", "BLEN7M_20120812_141500_25.fit.gz", "BLEN7M_20120812_143000_25.fit.gz",
             "BLEN7M_20120812_144500_25.fit.gz", "BLEN7M_20120812_150000_25.fit.gz", "BLEN7M_20120812_151500_25.fit.gz",
             "BLEN7M_20120812_153000_25.fit.gz", "BLEN7M_20120812_154500_25.fit.gz"]

for file in file_list:
    fits_file_path = download_from_url('/'.join([data_archives, file]))
    fits_filename = fits_file_path.split(os.sep)[-1]
    fits_file = fitsread.ECallistoFitsFile(fits_filename)
    fits_file.set_file_path()
    fits_file.set_hdul_dataset()
    fits_file.plot_freq_range_db_above_background(100, 350)
    fits_file.delete_file()
