from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'px4_multi_vehicle'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hrishikesh',
    maintainer_email='iischrishikesh@gmail.com',
    description='PX4 Multi Vehicle Simulation',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'friendly_drone_node = px4_multi_vehicle.friendly_drone_node:main',
            'friendly_node = px4_multi_vehicle.friendly_node:main',
            'enemy_drone_node = px4_multi_vehicle.enemy_drone_node:main',
        ],
    },
)