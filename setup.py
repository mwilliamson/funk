from distutils.core import setup

setup(
    name='Funk',
    version='0.3',
    description='A mocking framework for Python',
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/funk',
    packages=['funk'],
    install_requires=[
        "six>=1.4.1,<2.0",
    ],
    license='BSD License'
)
