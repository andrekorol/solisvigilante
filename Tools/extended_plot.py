import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Lib.urlget import download_from_url
from Lib import fitsread

data_archives = "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-" \
                "20yy_Callisto/2012/08/12/"
file_list = ["BLEN7M_20120812_140000_25.fit.gz",
             "BLEN7M_20120812_141500_25.fit.gz",
             "BLEN7M_20120812_143000_25.fit.gz",
             "BLEN7M_20120812_144500_25.fit.gz",
             "BLEN7M_20120812_150000_25.fit.gz",
             "BLEN7M_20120812_151500_25.fit.gz",
             "BLEN7M_20120812_153000_25.fit.gz",
             "BLEN7M_20120812_154500_25.fit.gz"]

file_path_list = []
for file in file_list:
    file_path_list.append(download_from_url('/'.join([data_archives, file])))


fitsread.ECallistoFitsFile.plot_fits_files_list(file_path_list, 100, 450,
                                                'Insert Title Here', 'pt',
                                                'plot_extendido')
