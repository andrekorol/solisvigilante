import json
import os
from lib.urlget import download_from_url
from lib import fitsread
from sys import exit

with open("events.json") as json_file:
    json_str = json_file.read()
    json_data = json.loads(json_str)

plots_dir = "databases"
data_archives = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto'
# year = "2011"
# event = json_data[year]["4"]
# print(event)
# month = event.split('_')[1][4:6]
# day = event.split('_')[1][-2:]
# fits_url = f'{data_archives}/{year}/{month}/{day}/{event}.fit.gz'
# fits_filename = download_from_url(fits_url)
# fits_file = fitsread.ChromosphericEvaporationFitsFile(fits_filename)
# fits_file.set_file_path()
# fits_file.set_hdul_dataset()
# fits_file.plot_db_above_background(True)
# # exit(0)
# os.rename(f'{event}.png', f'{plots_dir}/{year}/{event}.png')
# fits_file.set_fits_linear_regression()
# fits_file.set_fits_linear_regression_function()
# # fits_file.set_front_velocity(7.910, 7.931) "1"
# # fits_file.set_front_velocity(8.0132, 8.10938) "2"
# # fits_file.set_front_velocity(10.0092, 10.1799) "3"
# fits_file.set_front_velocity(22.5961, 22.6078)
# print(fits_file.get_front_velocity())
# print(fits_file.get_front())
# os.remove(fits_filename)
#
# exit(0)

for year in json_data:
    if not os.path.isdir(f'{plots_dir}/{year}'):
        os.makedirs(f'{plots_dir}/{year}')
    for event in json_data[year].values():
        month = event.split('_')[1][4:6]
        day = event.split('_')[1][-2:]
        fits_url = f'{data_archives}/{year}/{month}/{day}/{event}.fit.gz'
        fits_filename = download_from_url(fits_url)
        fits_file = fitsread.ECallistoFitsFile(fits_filename)
        fits_file.set_file_path()
        fits_file.set_hdul_dataset()
        fits_file.plot_db_above_background(True)
        os.rename(f'{event}.png', f'{plots_dir}/{year}/{event}.png')
        os.remove(fits_filename)
