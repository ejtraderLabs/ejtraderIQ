"""The python wrapper for IQ Option API package setup."""
from setuptools import (setup, find_packages)


setup(
    name="ejtraderIQ",
    version="1.0.7",
    packages=find_packages(),
    install_requires=["pylint","requests","websocket-client==0.56"],
    include_package_data = True,
    description="IQ Option API for python",
    long_description="IQ Option API for python",
    url="https://github.com/ejtraderLabs/ejtraderIQ",
    author="Emerson Pedroso",
    author_email="emerson@ejtrader.com",
    zip_safe=False
)
