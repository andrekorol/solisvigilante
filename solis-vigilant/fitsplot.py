from data import fitsread
import aplpy
import os

url_list = ['http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'
            '2011/08/09/BLEN7M_20110809_083004_24.fit.gz',
            'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'
            '2011/08/09/BLEN7M_20110809_083005_25.fit.gz',
            'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'
            '2012/07/31/BLEN7M_20120731_151359_25.fit.gz']

for url_link in url_list:
    fits_filename = fitsread.download_from_url(url_link)
    fig = aplpy.FITSFigure(fits_filename)
    fig.show_colorscale()
    fig.save(fits_filename.split('.')[0] + '.png')
    os.remove(fits_filename)
