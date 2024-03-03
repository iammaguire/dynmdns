from setuptools import setup, find_packages

setup(
    name='mdns-registrar',
    version='0.1.0',
    url='https://github.com/iammaguire/mdns-registrar',
    author='maggy',
    author_email='your-email@example.com',
    description='A simple library for managing mDNS records',
    packages=find_packages(),  
    install_requires=['zeroconf'],
)