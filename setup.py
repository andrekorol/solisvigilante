try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tools and scripts for analyzing data from the Sun',
    'author': 'Andre Rossi Korol',
    'url': 'https://github.com/andrekorol/solis-vigilante',
    'download_url': 'https://github.com/andrekorol/solis-vigilante',
    'author_email': 'anrobits@yahoo.com.br',
    'version': '0.1',
    'install_requires': ['aplpy', 'astropy'],
    'packages': ['solis-vigilante'],
    'scripts': ['bin/solis-vigilante.py'],
    'name': 'solis-vigilante'
}

setup(**config)

string = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_20110809_' \
         '083004_24.fit.g'