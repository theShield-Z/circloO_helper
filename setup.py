from setuptools import find_packages, setup

with open("README.md", 'r') as f:
    description = f.read()

setup(
    name='circloo_helper',
    version='1.1.1',
    url='https://github.com/theShield-Z/circloO_helper',
    packages=find_packages(),
    description='Build and edit circloO levels using Python',
    author='Shield Z',
    install_requires=[
        'numpy',
        'tripy',
        'numba',
        'pyperclip',
    ],
    extras_require={
        "all": ['matplotlib', 'pillow', 'imageio', 'imageio-ffmpeg', 'svgpathtools-light', 'mido'],
        "video": ['imageio', 'imageio-ffmpeg', 'pillow'],
        "image": ['pillow'],
        "show_img": ['matplotlib'],
        "svg": ['svgpathtools-light'],
        "audio": ['mido'],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
