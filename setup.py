import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-check-migration-wtf',
    version='1.0.0',
    packages=find_packages(),
    description='A line of description',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Antonio Irizar',
    author_email='antonioirizar@gmail.com',
    url='https://github.com/antonioIrizar/django-check-migration-wtf',
    license='GLP3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
    ],
    keywords='django postgres postgresql migrations',
    python_requires='>=3.6',
    install_requires=[
        'Django>=2.2,<3.1',
        'PyGithub>=1.50,<2',
    ]
)
