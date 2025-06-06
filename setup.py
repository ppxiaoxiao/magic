#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        try:
            with open(readme_path, 'r') as f:
                return f.read()
        except:
            return "Python 2 compatible magic library wrapper"

setup(
    name='magic',
    version='1.0.0',
    description='Python 2 compatible magic library wrapper using ctypes',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='xiaoxiao_zhang',
    
    packages=find_packages(),
    py_modules=['magic_wrapper', 'magic'],
    
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    
    keywords='magic file-type detection python2 ctypes libmagic',
    
    license='MIT',
    
    install_requires=[
       
    ],
    
    extras_require={
        'dev': [
            'wheel',
            'twine',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'py2-magic=magic_wrapper:main',
        ],
    },
    
    include_package_data=True,
    
    platforms=['Linux', 'Unix'],
) 