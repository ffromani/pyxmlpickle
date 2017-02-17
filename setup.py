import os.path
from distutils.core import setup


def version():
    # MUST fail if cannot open the source file
    with open('PKG-INFO', 'rt') as info:
        for line in info:
            if line.startswith('Version'):
                name, value = line.strip().split(':')
                return value.strip()


def description():
        return """
Pickle objects to/from XML
"""

setup(name='xmlpickle',
      version=version(),
      description='Pickle objects to/from XML',
      long_description=description(),
      platforms = [ 'posix' ],
      license = 'GPL2',
      author = 'Francesco Romani',
      author_email = 'fromani@redhat.com',
      url='https://github.com/fromanirh/pyxmlpickle',
      download_url='https://github.com/fromanirh/pyxmlpickle',
      py_modules=['xmlpickle'],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Classifier: Topic :: Software Development :: Libraries',
        'Classifier: Topic :: Utilities',
        'Operating System :: POSIX',
      ]
)
