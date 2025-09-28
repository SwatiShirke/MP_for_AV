from setuptools import find_packages
from setuptools import setup

setup(
    name='vd_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('vd_msgs', 'vd_msgs.*')),
)
