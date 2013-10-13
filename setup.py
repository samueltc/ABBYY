try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ABBYY',
    version='0.2',
    author='Samuel Cossette',
    author_email='samueltc@gmail.com',
    packages=['ABBYY',],
    install_requires = [
        'requests>=1.2.3', 
        'lxml>=3.1.0'
        ],
    url='https://github.com/samueltc/ABBYY',
    license='LICENSE',
    description='ABBYY Cloud OCR API Wrapper.',
    long_description=open('README.rst').read(),
)
