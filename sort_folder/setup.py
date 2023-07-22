from setuptools import setup, find_namespace_packages
from pathlib import Path

description = Path().joinpath('README.md').read_text()
setup(
    name='Sort_folder',
    version='0.0.1',
    description='Sort files',
    long_description=description,
    author='Semochkin Oleksandr',
    url='https://github.com/AlexSentex/go-it-hw-7.git',
    requires=find_namespace_packages(),
    license='MIT',
    entry_points={'console_scripts': ["sort_folder = sort_folder.Homework:main"]}
)