import os
from setuptools import setup


def read(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fileobj:
        return fileobj.read()


setup(
    name='Funk',
    version='0.5.0',
    description='A mocking framework for Python',
    long_description=read("README.rst"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='https://github.com/mwilliamson/funk',
    packages=['funk'],
    keywords="mock",
    install_requires=["precisely>=0.1.1"],
    python_requires='>=3.5',
    license='BSD License'
)
