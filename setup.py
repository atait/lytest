from setuptools import setup
import os

# Autoinstall into klayout
try:
    from lygadgets import postinstall_pure
except (ImportError, ModuleNotFoundError):
    print('\033[95mlygadgets not found, so klayout package not linked.')
    print('Please download lygadgets from the klayout Package Manager\033[0m')
    my_postinstall = dict()
else:
    setup_dir = os.path.dirname(os.path.realpath(__file__))
    pkg_dir = os.path.join(setup_dir, 'lytest')
    my_postinstall = {'install': postinstall_pure(pkg_dir)}


def readme():
    with open('README.md', 'r') as fx:
      return fx.read()


setup(name='lytest',
      version='0.0.1',
      description='Regression testing for klayout and phidl',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lytest'],
      install_requires=['phidl', 'pytest'],
      entry_points={},
      cmdclass=my_postinstall,
      )
