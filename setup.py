# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


version = '0.1.0'
setup(

  name = 'secretcli',

  version = version,
  packages=find_packages(),

  description = '',
  long_description=long_description,
  python_requires='>=3',

  author = 'Robert Hafner',
  author_email = 'tedivm@tedivm.com',
  url = 'https://github.com/tedivm/secretcli',
  download_url = "https://github.com/tedivm/secretcli/archive/v%s.tar.gz" % (version),
  keywords = '',

  classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',

    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',

    'Programming Language :: Python :: 3',
    'Environment :: Console',
  ],

  install_requires=[
    'boto3>=1.9,<2.0',
    'click>=6.0,<8.0',
    'requests',
    'pyyaml'
  ],

  extras_require={
    'dev': [
      'pypandoc',
      'twine',
      'wheel'
    ],
  },

  entry_points={
    'console_scripts': [
      'secretcli=secretcli.secretcli:cli',
    ],
  },

)
