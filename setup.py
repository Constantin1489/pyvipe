#!/usr/bin/env python3
from setuptools import setup

setup(
    name = 'pyvipe',
    version = '0.1.1',
    description='edit pipe with your editor.',
    author='Constantin Hong',
    author_email='hongconstantin@gmail.com',
    url='https://github.com/Constantin1489/pyvipe',
    maintainer='Constantin Hong',
    maintainer_email='hongconstantin@gmail.com',
    readme = "README.md",
    packages = ['pyvipe'],
    python_requires='>=3.9',
    project_urls = {
        'Documentation': 'https://github.com/Constantin1489/pyvipe#readme',
        'Source': 'https://github.com/Constantin1489/pyvipe',
        'Tracker': 'https://github.com/Constantin1489/pyvipe/issues',
        },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        "Topic :: Utilities",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        ],
    entry_points = {
        'console_scripts' : [
            'pyvipe = pyvipe.__main__:main'
        ]
    })

