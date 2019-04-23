try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tools and scripts for analyzing data from the Sun',
    'author': 'Andre Rossi Korol',
    'url': 'https://github.com/andrekorol/Lib',
    'download_url': 'https://github.com/andrekorol/Lib',
    'author_email': 'anrobits@yahoo.com.br',
    'version': '0.1',
    'install_requires': ['numpy', 'astropy', 'matplotlib'],
    'packages': ['solisvigilante'],
    'scripts': ['Tools/cycle24.py', 'Tools/franciscos_plots.py', 'Tools/genfitsdb.py', 'Tools/plotdatafits.py',
                'Tools/plotfitsdb.py'],
    'name': 'solisvigilante'
}

setup(**config)
