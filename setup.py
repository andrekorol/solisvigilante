try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tools and scripts for analyzing data from the Sun',
    'author': 'Andre Rossi Korol',
    'url': 'https://github.com/andrekorol/solis-vigilant',
    'download_url': 'https://github.com/andrekorol/solis-vigilant',
    'author_email': 'anrobits@yahoo.com.br',
    'version': '0.1',
    'install_requires': ['astropy'],
    'packages': ['solis-vigilant'],
    'scripts': ['bin/solis-vigilant.py'],
    'name': 'solis-vigilant'
}

setup(**config)
