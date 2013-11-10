# -*- coding: utf-8 -*-
import codecs
import os.path
import sys
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
__author__ = "flanker"


commands = filter(lambda x: x[0:1] != '-', sys.argv)

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
if os.path.isfile(readme):
    with codecs.open(readme, 'r', encoding='utf-8') as fd:
        long_description = fd.read()
else:
    long_description = ''

entry_points = {"console_scripts": ["pythonnest-manage = pythonnest.djangoproject.manage:main", ], }


version_filename = os.path.join(os.path.dirname(__file__), 'VERSION')
with codecs.open(version_filename, 'r', encoding='utf-8') as fd:
    version = fd.read()

setup(
    name='pythonnest',
    version=version,
    description='Pypi emulator and cloning tool .',
    long_description=long_description,
    author="flanker",
    author_email="flanker@19pouces.net",
    license="CeCILL-B",
    url="http://19pouces.net/PythonNest.html",
    entry_points=entry_points,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='pythonnest.tests',
    ext_modules=[],
    cmdclass={},
    install_requires=['setuptools>=0.7', 'django', 'South', 'rpc4django', ],
    setup_requires=[ 'setuptools>=0.7',  'django',  'South', ],
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 ]
)