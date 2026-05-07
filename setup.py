from setuptools import find_packages, setup

setup(
    name='circloo_helper',
    version='2.0.2',
    packages=find_packages(),
    description='Build and edit circloO levels using Python',
    author='Shield Z',
    install_requires=[
        'setuptools~=75.8.2',
        'numpy~=2.2.4',
        'matplotlib~=3.10.1',
        'pillow~=11.1.0',
        'opencv-python~=4.11.0.86',
        'svgpathtools-light~=1.6.2',
        'pyperclip~=1.11.0',
    ],
    # Unsure about making these optional installs
    # extras_require={
    #     "full": [...]
    #     "image_converter": [...]
    #     "video_converter": [...]
    # }
)
