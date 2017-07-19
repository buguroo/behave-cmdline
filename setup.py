# -*- coding: utf-8 -*-
"""
behave-cmdline
"""
from setuptools import setup, find_packages
import os

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()

VERSION = '0.0.4'

setup(name='behave-cmdline',
      version=VERSION,
      description="Behave steps for command line program testing",
      long_description=README,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Testing'
      ],
      keywords='bdd testing behave command line',
      author='Roberto Abdelkader Martínez Pérez',
      author_email='robertomartinezp@gmail.com',
      url='https://github.com/buguroo/behave-cmdline',
      license='LGPLv3',
      packages=["behave_cmdline",
                "behave_cmdline.steps",
                "behave_cmdline.steps.stepcollection",
                "behave_cmdline.steps.naturalsearch"],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ])
