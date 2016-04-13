[![Build Status](https://travis-ci.org/morgenst/pyfluka.svg?branch=master)](https://travis-ci.org/morgenst/pyfluka)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.md)
[![Coverage Status](https://coveralls.io/repos/github/morgenst/pyfluka/badge.svg?branch=master)](https://coveralls.io/github/morgenst/pyfluka?branch=master)
# pyfluka

A tool aiming for comprehensive analysis of FLUKA simulations in a generic way.

## Dependencies

The following additional libraries are required:

- coveralls (https://pypi.python.org/pypi/coveralls)
- numpy, scipy (http://docs.scipy.org/doc/numpy/index.html)
- matplotlib (http://matplotlib.org/)
- networkx (https://networkx.github.io/)
- pint (https://pypi.python.org/pypi/Pint/)
- PyYAML (https://pypi.python.org/pypi/PyYAML)
- tabulate (https://pypi.python.org/pypi/tabulate)
- yamlordereddictloader (https://pypi.python.org/pypi/yamlordereddictloader/0.1.0)
- setuptools (https://pypi.python.org/pypi/setuptools)

By default they are installed automatically as long as setuptools is available

## Installation

Installation is quite easy. Just run:

```bash
python setup.py install --prefix=/path/where/to/install
```

## Run

Executing pyfluka simply works via

```bash
pyfluka -i input_file_list -o output_directory -c config_file
```

## Help
 
For help run:
 
```bash
pyfluka -h
```