from setuptools import setup
from codecs import open
from os import path

if __name__ == '__main__':

    # Get directory of this setup.py
    this_dir = path.abspath(path.dirname(__file__))
    # Read the text of README.rst and let that be the long_description
    with open(path.join(this_dir,'README.rst')) as rme_fp:
        long_desc = rme_fp.read()
        
    metadata = dict(
        name         = 'marketxtradermodel',
        use_scm_version=True, # Deduce version from git tag.
        description = 'Reproduced implementation of market model described in Bakker et al, Physica A 2010.',
        long_description  = long_desc,
        license      = 'Apache 2.0',
        packages     = ['marketxtradermodel'],
        author       = 'Lukas Ahrenberg',
        author_email = 'lukas@ahrenberg.se',
        url = 'https://github.com/ahrenberg/marketxtradermodel',
        setup_requires  = ['setuptools_scm'], # To deduce version from git, quite useful for now. 
        install_requires = ['numpy','networkx'],
        python_requires = '>=2.7, !=3.0.*, !=3.1.*, >=3.2, <4',
        )

    setup(**metadata)
