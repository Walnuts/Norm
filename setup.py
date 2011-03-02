try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'a non-orm. abstracting away sql statements, but\
                using regular python data structures',
        'author': 'Walnuts',
        'url': 'http://walnuts.github.com/norm/',
        'download_ur': 'http://walnuts.github.com/norm/norm.tar.gz',
        'author_email': 'modulo.w@gmail.com',
        'version': '0.1',
        'install_requires': ['nose'],
        'packages': ['norm'],
        'scripts': [],
        'name': 'Norm',
        }

setup(**config)

