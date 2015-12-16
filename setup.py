try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'REST API for AWS S3 meant to be an interface to immutable artifact storage.',
    'author': 'Kyle Long',
    'url': 'none',
    'download_url': 'none',
    'author_email': 'uilwen@gmail.com',
    'version': '0.01',
    'install_requires': [
        'Flask',
        "gevent",
        "gunicorn",
        "PyYAML",
        'boto' 
    ],
    'tests_require': [
        'pyproctor',
        'mock'
    ],
    'packages': ['pyshelf'],
    'scripts': [],
    'name': 'pyshelf'
}

setup(**config)
