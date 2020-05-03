import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-check-migration-wtf',
    version='0.1',
    packages=find_packages(),
    description='A line of description',
    long_description=README,
    author='Antonio Irizar',
    author_email='antonioirizar@gmail.com',
    url='https://github.com/antonioIrizar/django-check-migration-wtf',
    license='GLP3',
    python_requires='>=3.7',
    install_requires=[
        'Django>=2.2,<2.3',
        'PyGithub>=1.50,<2',
    ]
)