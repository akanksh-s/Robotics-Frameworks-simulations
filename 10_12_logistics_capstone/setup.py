from setuptools import setup
import os
from glob import glob

package_name = 'rof_ex10_12'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robot',
    maintainer_email='robot@fau.de',
    description='EU_10-12 Practical Task – Logistics state machine and YOLO perception',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'logistics_task_sm   = rof_ex10_12.logistics_task_sm:main',
            'yolo_subscriber     = rof_ex10_12.yolo_subscriber:main',
        ],
    },
)
