from setuptools import find_packages, setup

setup(
    name='circloo_helper',
    version='0.0.25',
    packages=find_packages(),
    description='Build and edit circloO levels using Python',
    author='Shield Z',
    install_requires=[
        'setuptools~=75.8.2',
        'numpy~=2.2.4',
        'matplotlib~=3.10.1',
        'pillow~=11.1.0',
        'opencv-python~=4.11.0.86',
    ],
)
