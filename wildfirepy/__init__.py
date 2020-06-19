from pkg_resources import DistributionNotFound, get_distribution

from wildfirepy import coordinates, net

__all__ = ['net', 'coordinates']

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass  # package is not installed
