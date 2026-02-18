#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nawa Programming Language - Installer
نواة - لغة البرمجة العربية
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README_NAWA.md").read_text(encoding='utf-8')

setup(
    name='nawa-lang',
    version='1.0.0',
    author='Nawa Team',
    author_email='nawa.lang@example.com',
    description='Nawa - Advanced Arabic Programming Language | نواة - لغة البرمجة العربية المتقدمة',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nawa-lang/nawa',
    py_modules=['nawa'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: Arabic',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    keywords='arabic programming language nawa نواة برمجة عربي',
    project_urls={
        'Documentation': 'https://github.com/nawa-lang/nawa#readme',
        'Source': 'https://github.com/nawa-lang/nawa',
        'Tracker': 'https://github.com/nawa-lang/nawa/issues',
    },
    entry_points={
        'console_scripts': [
            'nawa=nawa:main',
        ],
    },
)
