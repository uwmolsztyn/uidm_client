from setuptools import setup

setup(
    name='uidm_client',
    version='0.10',
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=["uidm_client"],
    install_requires=[
        "requests"
    ],
)
