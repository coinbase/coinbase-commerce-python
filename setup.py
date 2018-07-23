"""Setup script for Coinbase Commerce API client.
Also installs included versions of third party libraries, if those libraries
are not already installed.
"""
from setuptools import setup
import coinbase_commerce

version = coinbase_commerce.__version__

packages = ['coinbase_commerce',
            'coinbase_commerce.api_resources',
            'coinbase_commerce.api_resources.base']

install_requires = ["requests>=2.14.0", ]

setup(
    name='coinbase_commerce',
    version=version,
    packages=packages,
    include_package_data=True,
    license='Apache 2.0',
    description='Coinbase Commerce API client library',
    url='https://github.com/adobrzhansky/coinbase-commerce-python',
    keywords=['api', 'coinbase commerce', 'client'],
    install_requires=install_requires,
    author='Coinbase, Inc.',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
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
