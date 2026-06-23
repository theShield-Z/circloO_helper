from setuptools import find_packages, setup

with open("README.md", 'r') as f:
    description = f.read()

setup(
    name='circloo_helper',
    version='1.0.0',
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
    long_description=description,
    long_description_content_type="text/markdown",
    # Unsure about making these optional installs
    # extras_require={
    #     "full": [...]
    #     "image_converter": [...]
    #     "video_converter": [...]
    # }
)
