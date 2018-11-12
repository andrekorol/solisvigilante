import os
from lib.urlget import download_from_url
from lib import fitsread


events_per_year = {'2014': ['BLEN7M_20140610_081500_24', 'BLEN7M_20140610_081500_25',
                   'BLEN7M_20140610_091500_24', 'BLEN7M_20140610_091500_25',
                   'DARO-HF_20140610_113000_58'],
          '2016': ['GLASGOW_20160128_114501_59',
                   'GLASGOW_20160721_110000_59',
                   'BLENSW_20160723_050000_01', 'BLENSW_20160723_050000_02', 'BLENSW_20160723_051500_01',
                   'BLENSW_20160723_051500_02', 'BLENSW_20160723_053000_01', 'BLENSW_20160723_053000_02',
                   'BLENSW_20160723_054500_01', 'BLENSW_20160723_054500_02',
                   'MRT3_20160807_035250_59']}

plots_dir = 'francisco_plots'
data_archives = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto'

for year in events_per_year:
    if not os.path.isdir(f'{plots_dir}/{year}'):
        os.makedirs(f'{plots_dir}/{year}')
    for event in events_per_year[year]:
        month = event.split('_')[1][4:6]
        day = event.split('_')[1][-2:]
        fits_url = f'{data_archives}/{year}/{month}/{day}/{event}.fit.gz'
        fits_filename = download_from_url(fits_url)
        fits_file = fitsread.ECallistoFitsFile(fits_filename)
        fits_file.set_file_path()
        fits_file.set_hdul_dataset()
        fits_file.plot_db_above_background()
        os.rename(f'{event}.png', f'{plots_dir}/{year}/{event}.png')
        os.remove(fits_filename)
