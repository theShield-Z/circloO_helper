from setuptools import find_packages, setup

setup(
    name='circloo_helper',
    version='2.0.11',
    packages=find_packages(),
    description='Build and edit circloO levels using Python',
    author='Shield Z',
    install_requires=[
        'setuptools',
        'numpy',
        'matplotlib',
        'pillow',
        'opencv-python',
        'svgpathtools-light',
        'pyperclip',
        'tripy',
        'numba',
    ],
    # Unsure about making these optional installs
    # extras_require={
    #     "full": [...]
    #     "image_converter": [...]
    #     "video_converter": [...]
    # }
)
