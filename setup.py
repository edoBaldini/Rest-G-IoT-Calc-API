from setuptools import setup, find_packages

setup(
    name='IoT Green Calculator',

    keywords='rest restful api flask swagger openapi flask-restplus',
    url='https://github.com/edoBaldini/IoTGreenCalc',
    author="Edoardo Baldini",

    packages=find_packages(),

    install_requires=['flask-restplus==0.9.2', 'Flask==1.1.1', 'Flask-Cors==3.0.7'],
)
