from setuptools import setup, find_packages

setup(
    name="scatseisnet",
    version="0.1.6",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["matplotlib", "numpy", "obspy", "scikit-learn"],
)
