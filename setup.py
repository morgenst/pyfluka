from setuptools import setup, find_packages

setup(
    name="pyfluka",
    version="prototype",
    packages=find_packages(),
    scripts=["analysistest/run.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['numpy>=1.0',
                      'matplotlib>=1.3.1',
                      'networkx>=1.11',
                      'PyYAML>=3.11',
                      'tabulate>=0.7.5',
                      'pint>=0.7.2'
                      'yamlordereddictloader>=0.1.0'],

    package_data={

    },

    # metadata for upload to PyPI
    author="Marcus Matthias Morgenstern",
    author_email="marcus.matthias.morgenstern@cern.ch",
    description="pyfluka package",
    license="MIT",
    keywords="FLUKA MC data analysis physics radiation protection",
    url="https://github.com/morgenst/pyfluka"
)