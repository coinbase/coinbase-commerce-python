"""Setup script for Coinbase Commerce API client.
Also installs included versions of third party libraries, if those libraries
are not already installed.
"""
import os

from setuptools import setup

version_contents = {}
with open(os.path.join(os.path.dirname(__file__), 'coinbase_commerce', 'version.py')) as f:
    exec (f.read(), version_contents)

long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

packages = ['coinbase_commerce',
            'coinbase_commerce.api_resources',
            'coinbase_commerce.api_resources.base']

install_requires = ["requests>=2.14.0", "six>=1.9"]

setup(
    name='coinbase_commerce',
    version=version_contents['VERSION'],
    packages=packages,
    include_package_data=True,
    license='Apache 2.0',
    description='Coinbase Commerce API client library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/coinbase/coinbase-commerce-python',
    keywords=['api', 'coinbase commerce', 'client'],
    install_requires=install_requires,
    author='Coinbase, Inc.',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
