from setuptools import setup, find_packages

setup(
    name='mdns_registrar',
    version='0.1.0',
    url='https://github.com/iammaguire/dynmdns/mdns_registrar',
    author='maggy',
    author_email='your-email@example.com',
    description='A simple library for managing mDNS records',
    packages=find_packages(),  
    install_requires=['zeroconf'],
)