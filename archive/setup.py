from setuptools import setup
from setuptools import find_packages
from pathlib import Path

# Metadata
PACKAGE_NAME = 'Micro'
DESCRIPTION = ''
URL = ''
AUTHOR = 'Zach Morris'
AUTHOR_EMAIL = 'zacharymorr@outlook..com'

# Package Data
REQUIRED_PYTHON = '>=3.7'

PACKAGES = find_packages()

PACKAGE_DATA = {
      '': ['*.ini']
}

DEPENDENCIES = [
]

CONSOLE_SCRIPTS = [
      'micro=micro.__main__:main',
]

# # Determine Version
# # Open and execute version.py, then retreive version from globals
# setup_py_path = Path(__file__).resolve()
# package_dir = setup_py_path.parent
# version_file_path = package_dir / 'Gouda' / 'version.py'
# with open(version_file_path, 'r') as version_file:
#     version = {}
#     exec(version_file.read(), version)

# VERSION = version['__version__']
VERSION = "0.0.0"

# Run Setup
setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      url=URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      python_requires=REQUIRED_PYTHON,
      install_requires=DEPENDENCIES,
      entry_points = {
            'console_scripts': CONSOLE_SCRIPTS
      }
)