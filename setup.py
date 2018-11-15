from setuptools import setup
import os


def readme():
    with open('README.md', 'r') as fx:
      return fx.read()


setup(name='lytest',
      version='0.0.8',
      description='Regression testing for klayout and phidl',
      long_description=readme(),
      author='Alex Tait, Adam McCaughan, Sonia Buckley, Jeff Chiles, Jeff Shainline, Rich Mirin, Sae Woo Nam',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lytest'],
      install_requires=['klayout', 'pytest', 'lygadgets', 'lyipc'],
      entry_points={'console_scripts': ['lytest=lytest.command_line:cm_main']},
      cmdclass={},
      )
