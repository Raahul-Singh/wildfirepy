WildfirePy
=====

![](https://github.com/wildfirepy/wildfirepy/workflows/Python%20application/badge.svg)
![](https://github.com/wildfirepy/wildfirepy/workflows/Python%20package/badge.svg)

WildfirePy is an open-source Python library for Wildfire GIS data analysis.

Installation
------------

Use git to grab the latest version of WildfirePy:

    git clone https://github.com/wildfirepy/wildfirepy.git

Done! In order to enable WildfirePy to be imported from any location you must make
sure that the library is somewhere in your PYTHONPATH environmental variable.
For now the easiest thing is to install it locally by running,
```
pip install -e .
```
from the directory you just
downloaded. 

Usage
-----

Here is a quick example of downloanding some burnt area information from MODIS:

```python
>>> from wildfirepy.net.usgs import ModisBurntAreaDownloader
>>> import matplotlib.pyplot as plt
>>> dl = ModisBurntAreaDownloader()
>>> jpg_file = dl.get_jpg(year=2020, month=2, latitude=28.7041, longitude=77.1025)
>>> plt.imshow(plt.imread(jpg_file))
>>> plt.show()
```

Getting Help
------------

For more information or to ask questions about WildfirePy, check out:

 * IRC: #wildfirepy on [Riot](https://riot.im/app/#/room/!jWUOIxirCHymPQkpXb:matrix.org)

Contributing
------------

If you would like to get involved, start by joining the IRC chat room named `#wildfirepy` on [Riot](https://riot.im/app/#/room/!jWUOIxirCHymPQkpXb:matrix.org).
You may follow our [LinkedIn](https://www.linkedin.com/company/wildfirepy/) and [Twitter](https://twitter.com/wildfirepy) handle as well!

Help is always welcome so let us know what you like to work on, or check out the [issues page](https://github.com/wildfirepy/wildfirepy/issues) for a list of some known outstanding items.
