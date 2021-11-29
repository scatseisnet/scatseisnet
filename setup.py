from setuptools import setup, find_packages

setup(
    name="scatnet",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["obspy", "parse", "nmmn", "click >= 8"],
    entry_points={"console_scripts": ["scatnet = scatnet.cli.cli:main",],},
)
