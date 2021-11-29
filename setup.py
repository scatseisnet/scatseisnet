from setuptools import setup, find_packages

setup(
    name="scatseisnet",
    version="0.1.3",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["obspy", "parse", "nmmn", "click >= 8"],
    entry_points={"console_scripts": ["scatseisnet = scatseisnet.cli.cli:main",],},
)
