from setuptools import find_packages
from setuptools import setup

setup(
    name='vd_carla_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('vd_carla_msgs', 'vd_carla_msgs.*')),
)
