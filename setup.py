""""
TODO: istall setup.py to fix relative import problems
pip install -e .
(-e for editable)
"""

from distutils.core import setup
from setuptools import find_packages

setup(name='compilers ast',
      version='1.0',
      description='src dir for compilers',
      author='Team 2',
      url='https://github.com/judithhershko/compilers/tree/main/src',
      packages=find_packages(include=['src', 'src.*'])
     )