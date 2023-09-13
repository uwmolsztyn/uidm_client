from setuptools import setup, find_packages

setup(
    name='uidm_client',
    version='0.1',
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
)