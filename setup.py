
### 3. Optional: Create a `setup.py` File for a More Advanced Installation

from setuptools import setup, find_packages

setup(
    name='unarchive',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        # Example: 'requests', 'numpy',
    ],
    entry_points={
        'console_scripts': [
            'unarchive=extractor:main',
        ],
    },
)
