from setuptools import setup

setup(
    name="scatnet",
    version="0.1.0",
    entry_points={"console_scripts": ["scatnet = scatnet.cli.cli:main",],},
)
