"""Project setup script."""

import os
import subprocess

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
git_log = subprocess.Popen(["git", "log", "--pretty=format:%h%x09%s"],
                           stdout=subprocess.PIPE)

CHANGES, err = git_log.communicate()

requires = [
    "pylint==0.28.0",
    "pep8==1.4.6",
    "Twisted==14.0.0",
    ]

setup(name='Koodhz',
      version='0.0',
      description='Koodhz',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
                  "Programming Language :: Python",
      ],
      author='Nicolas Trippar',
      author_email='nicolas@trippar.com',
      url='',
      keywords='irc whatsapp bot',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      )
