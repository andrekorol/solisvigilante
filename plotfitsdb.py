from data.urlget import download_from_url
from data import fitsplot
import os


sample_url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_' \
    'Callisto/2011/08/09/BLEN7M_20110809_083004_24.fit.gz'
print(sample_url)

fits_filename = download_from_url(sample_url)

fits_file_path = fitsplot.GetFitsPath()

fitsplot.PlotFitsdB(fits_file_path)

os.remove(fits_filename)
