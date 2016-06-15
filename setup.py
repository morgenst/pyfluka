from setuptools import setup, find_packages

setup(
    name="pyfluka",
    version="prototype",
    packages=find_packages(),
    scripts=["pyfluka/pyfluka-exec.py",
             "pyfluka/pyfluka_merge.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['nose-exclude>=0.4.1',
                      'numpy>=1.0',
                      'matplotlib>=1.3.1',
                      'networkx>=1.11',
                      'PyYAML>=3.11',
                      'tabulate>=0.7.5',
                      'pint==0.6',
                      'yamlordereddictloader>=0.1.0',
                      'coveralls>=1.1',
                      'Cython>=0.20',
                      'kivy>=1.9.0'],
    package_data={
        '': ['*.p', 'test_data/*'],
    },

    # metadata for upload to PyPI
    author="Marcus Matthias Morgenstern",
    author_email="marcus.matthias.morgenstern@cern.ch",
    description="pyfluka package",
    license="MIT",
    keywords="FLUKA MC data analysis physics radiation protection",
    url="https://github.com/morgenst/pyfluka"
)