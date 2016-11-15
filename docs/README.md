Documentation
=============

Documentation is generated using sphinx: <https://sphinx-doc.org>

The documentation can be build using make and sphinx.
To build the documentation ensure that "sphinx" and "make" are installed::

    # Install make using the package manager (Ubuntu/Debian)
    apt-get install make

    # Install sphinx & sphinx read the docs theme from pip
    pip3 install sphinx sphinx_rtd_theme

From the docs folder build the documentation ::

    # Build html documentation
    make html

The built documentation can then be found under **_build/html**


