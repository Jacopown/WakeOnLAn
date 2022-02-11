from importlib.metadata import entry_points
from setuptools import setup

setup(
    name='WoLTool',
    version='1.0',
    author='Jacopown',
    description='A simple tool for wake-on-lan',
    scripts=['wol.py'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'wol=wol:wake',
        ]
    },

)
