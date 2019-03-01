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
    'install_requires': ['numpy', 'astropy', 'matplotlib'],
    'packages': ['solis-vigilante'],
    'scripts': ['bin/cycle24.py', 'bin/franciscos_plots.py', 'bin/genfitsdb.py', 'plotdatafits.py',
                'bin/plotfitsdb.py'],
    'name': 'solis-vigilante'
}

setup(**config)
