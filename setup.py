from setuptools import setup
import pathlib


setup(
    name='matchlib',
    author='qweeze',
    author_email='qweeeze@gmail.com',
    version='0.2.1',
    description='A tool for partial comparison of (nested) data structures',
    long_description=(pathlib.Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/qweeze/matchlib',
    packages=['matchlib'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
