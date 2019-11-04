import os

from setuptools import setup, find_packages


def make_long_description():
    return open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(
    name="py3status-random-wallpaper",
    version="1.0",

    packages=find_packages(),
    install_requires=["py3status>=3.20"],

    entry_points={"py3status": ["module = py3status_randwallpaper.Py3status"]},

    author="Remy Chaput",
    author_email="rchaput.pro@gmail.com",
    description="py3status module to randomly set your wallpaper",
    long_description=make_long_description(),
    long_description_content_type="text/markdown",

    url="https://github.com/rchaput/py3status-random-wallpaper",
    license="Apache",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
