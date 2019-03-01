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
    'packages': ['solis-vigilante'],
    'scripts': ['bin/solis-vigilante.py'],
    'name': 'solis-vigilante'
}

setup(**config, install_requires=['numpy', 'astropy', 'matplotlib'])
