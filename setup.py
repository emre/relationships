from setuptools import setup

setup(
    name='relationships',
    version='0.0.2',
    packages=['relationships'],
    url='http://github.com/emre/relationships',
    license='MIT',
    author='Emre Yilmaz',
    author_email='hello@emre.sh',
    description='redis backed user relationships',
    install_requires=['redis'],

)

