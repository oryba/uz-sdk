try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

with open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md'
), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='UZ SDK',
    version='0.0.3',
    author='Oleh Rybalchenko',
    author_email='rv.oleg.ua@gmail.com',
    url='https://github.com/oryba/uz-sdk',
    description='UZ API wrapper',
    download_url='https://github.com/oryba/uz-sdk/archive/master.zip',
    license='MIT',

    packages=['uz_sdk'],
    install_requires=['requests'],
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ]
)
