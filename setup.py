import os
from setuptools import setup, find_packages

def read(fname):
    """Returns a file as a string"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "LAN AUTH",
    version = "3.0",
    author = "Matt Parker",
    author_email = "mparker@lsucs.org.uk",
    description = ("LSUCS LAN party authentication system"),
    long_description = read("README.md"),

    license = "MIT",
    classifiers = [
        "Development Status :: 3 - Alpha"
        "Environment :: Web Environment",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
        "Topic :: System :: Networking :: Firewalls"
    ],

    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,

    install_requires=[
        'Flask>=0.10.1',
        'Flask-RESTful>=0.3.5',
        'SQLAlchemy>=1.0',
        'PyMySQL>=0.5',
        'requests>=2.9'
    ],

    entry_points = {
        'console_scripts': [
            'lanauth=lanauth.__main__:cli',
        ]
    }

)
