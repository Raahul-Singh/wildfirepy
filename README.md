WildfirePy
=====

![Python application](https://github.com/wildfirepy/wildfirepy/workflows/Python%20application/badge.svg)
![Python Online Tests](https://github.com/wildfirepy/wildfirepy/workflows/Python%20Online%20Tests/badge.svg)
![Codestyle](https://github.com/wildfirepy/wildfirepy/workflows/Codestyle/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/wildfirepy/badge/?version=latest)](https://wildfirepy.readthedocs.io/en/latest/?badge=latest)

WildfirePy is an open-source Python library for Wildfire GIS data analysis.

Installation
------------

Use git to grab the latest version of WildfirePy::

    git clone https://github.com/wildfirepy/wildfirepy.git

Done! In order to enable WildfirePy to be imported from any location you must make
sure that the library is somewhere in your PYTHONPATH environmental variable.
For now the easiest thing is to install it locally by running the following::

    pip install -e .

at the root of the directory you have just downloaded.

Usage
-----

Here is a quick example of downloanding some burnt area information from MODIS::

    >>> from wildfirepy.net.usgs import ModisBurntAreaDownloader
    >>> import matplotlib.pyplot as plt
    >>> dl = ModisBurntAreaDownloader()
    >>> jpg_file = dl.get_jpg(year=2020, month=2, latitude=28.7041, longitude=77.1025)
    >>> plt.imshow(plt.imread(jpg_file))
    >>> plt.show()

Getting Help
------------

For more information or to ask questions about WildfirePy, check out:

 * IRC: #wildfirepy on [Element](https://app.element.io/#/room/#wildfirepy:matrix.org)

Contributing
------------

If you would like to get involved, start by joining the IRC chat room named `#wildfirepy` on [Element](https://app.element.io/#/room/#wildfirepy:matrix.org).
You may follow our [LinkedIn](https://www.linkedin.com/company/wildfirepy/) and [Twitter](https://twitter.com/wildfirepy) handle as well!

Contribution is always welcome so do let us know what you would like to work on, and you can do so via our IRC.
Alternatively, do check out our [issues tracker](https://github.com/wildfirepy/wildfirepy/issues) for a list of some known outstanding items, or open new issues if you have encountered a bug, have a feature request, or got some question(s) regarding our project you would like to discuss.
