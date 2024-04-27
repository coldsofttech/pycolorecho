from setuptools import setup

import pycolorecho

setup(
    name=pycolorecho.__name__,
    version=pycolorecho.__version__,
    packages=[
        pycolorecho.__name__
    ],
    url='https://github.com/coldsofttech/pycolorecho',
    license='MIT',
    author=pycolorecho.__author__,
    description=pycolorecho.__description__,
    requires_python=">=3.10",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=[
        "color", "text-color", "text-background-color", "text-effect",
        "text-case", "terminal", "colorization", "style", "text"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)
