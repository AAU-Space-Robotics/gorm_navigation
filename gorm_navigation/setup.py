from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'gorm_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), 
         glob(os.path.join('launch', '*launch.py'))),
        # Include config files
        (os.path.join('share', package_name, 'config'),
         glob(os.path.join('config', '*.yaml'))),
        # Include README
        ('share/' + package_name, ['README.md']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anton Bjørndahl Mortensen',
    maintainer_email='antonbm2008@gmail.com',
    description='Navigation package for GORM rover including RL-based autonomous navigation',
    tests_require=['pytest'],
    license='GNU Affero General Public License v3',
    entry_points={
        'console_scripts': [
            'rl_navigation_node = gorm_navigation.rl_navigation_node:main',
            'goal_publisher_node = gorm_navigation.goal_publisher_node:main',
        ],
    },
)
