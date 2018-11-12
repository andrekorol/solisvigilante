from lib.urlget import download_from_url
from lib import fitsread
import os


#  sample_url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_' \
#    'Callisto/2011/08/09/BLEN7M_20110809_083004_24.fit.gz'

sample_url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2013/05/15/SSRT_20130515_013000_59.fit.gz'
print(sample_url)

fits_file = download_from_url(sample_url)

fits_file = fitsread.ChromosphericEvaporationFitsFile(fits_file)
fits_file.set_file_path()
fits_file.set_hdul_dataset()
fits_file.set_fits_linear_regression()
fits_file.set_fits_linear_regression_function()
#  fits_file.set_front_velocity(8.622, 8.681) #  For BLEN7M
fits_file.set_front_velocity(1.5823, 1.6792) #  For SSRT
print(fits_file.get_front_velocity())
fits_file.plot_db_above_background(True)
print(fits_file.get_front())

# os.remove(fits_filename)
