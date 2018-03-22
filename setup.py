from setuptools import setup

setup(
    name='critter',
    packages=['critter'],
    include_package_data=True,
    install_requires=[
        'flask',
        'firebase-admin'
    ]
)