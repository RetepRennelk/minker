from setuptools import setup, find_packages

setup( 
    name = 'minker',
    version = '0.1',
    description = 'minker / mind // thinking /// mincer',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'minker = minker.minker:main',
        ],
    })
