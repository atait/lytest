from setuptools import setup
import os


def readme():
    with open('README.md', 'r') as fx:
      return fx.read()


setup(name='lytest',
      version='0.0.21',
      description='Regression testing for klayout and phidl',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/atait/lytest/',
      author='Alex Tait, Adam McCaughan, Sonia Buckley, Jeff Chiles, Jeff Shainline, Rich Mirin, Sae Woo Nam',
      author_email='atait@ieee.org',
      license='MIT',
      packages=['lytest'],
      install_requires=['pytest'],
      entry_points={'console_scripts': ['lytest=lytest.command_line:cm_main']},
      cmdclass={},
      )
