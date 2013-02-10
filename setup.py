#!/usr/bin/env python

import pmgmt

version = pmgmt.__version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = ['pmgmt']
requires = [
        'flask==0.9',
        'numpy'
        ]


setup(
        name='parameter_mgmt',
        version=version,
        description='Application to manage marine parameters in ION',
        long_description=open('README.md').read(),
        author='Luke Campbell',
        author_email='lcampbell@asascience.com',
        url='https://github.com/lukecampbell/parameter_mgmt.git',
        packages=packages,
        package_data={'':['LICENSE']},
        include_package_data=True,
        install_requires=requires,
        license=open("LICENSE").read(),
        classifiers=(
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ),
#        entry_points = {
#            'console_scripts': [
#                'flaskmonitord = flaskmonitor.webapp:launch'
#                ],
#            },
        )



