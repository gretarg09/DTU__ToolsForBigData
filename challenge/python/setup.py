from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("queries_GAG_cython.pyx")
)