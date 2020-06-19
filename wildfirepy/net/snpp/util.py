import re
import urllib
import urllib.request
from http.cookiejar import CookieJar
from urllib.request import (HTTPBasicAuthHandler, HTTPCookieProcessor,
                            HTTPPasswordMgrWithDefaultRealm)

__all__ = ['URLOpenerWithRedirect', 'Viirs1KMParser']

class URLOpenerWithRedirect:
    """
    Description
    -----------
    A `urllib` based URL opener for URLs that require Login Authentication
    and lead to redirects.
    Creates a minimal opener with a HTTP Password Manager, and a HTTP CookieJar

    Parameters
    ----------
    username: `str`
        The login username required to open the URL.
    password: `str`
        The login password required to open the URL.
    top_level_url: `str`
        Base URL that leads to the login redirects.

    Returns
    -------
    response: `http.client.HTTPResponse`
        When called with a URL, authenticates the domain from `top_level_url`
        and returns the corresponding response object for the URL.

    Examples
    --------
    >>> opener = URLOpenerWithRedirect()
    >>> response = opener(url)

    >>> username = "MyName"
    >>> password = "MyPassword"
    >>> top_level_url = "https://top_level_url.com/"
    >>> opener = URLOpenerWithRedirect(username=username, password=password, top_level_url=top_level_url)
    >>> response = opener(url)
    """
    def __init__(self, *, username='RaahulSingh', password='WildFire_Bad.100',
                 top_level_url="https://urs.earthdata.nasa.gov/"):

        auth_manager = HTTPPasswordMgrWithDefaultRealm()
        auth_manager.add_password(None, top_level_url, username, password)
        handler = HTTPBasicAuthHandler(auth_manager)
        self.opener = urllib.request.build_opener(handler, HTTPCookieProcessor(CookieJar()))
        # TODO: Get an organisation username and password.

    def __call__(self, url):
        return self.opener.open(url)


class Viirs1KMParser:
    def __init__(self, product, url):
        self.url_opener = URLOpenerWithRedirect()
        self.product = product
        self.html_content = self.url_opener(url).read().decode('cp1252')

    def __call__(self, url):
        self.html_content = self.url_opener(url).read().decode('cp1252')
 
    def get_all_h5_files(self):
        """
        Returns list of all `h5` files available for download.
        """
        return re.findall(r'' + f'href="({self.product}.*h5)"', self.html_content)

    def get_filename(self, h, v):
        """
        Returns full name of the file based on the Sinusoidal Grid coordinates.
        Parameters
        ----------
        h: `int`
            Sinusoidal grid longitude
        v: `int`
            Sinusoidal grid latitude
        References
        ----------
        [1] https://modis-land.gsfc.nasa.gov/MODLAND_grid.html
        """
        h = str(h) if h > 9 else "0" + str(h)
        v = str(v) if v > 9 else "0" + str(v)

        r = re.compile(r'.*' + f'.(h{h}v{v}).')

        match = list(filter(r.match, self.get_all_h5_files()))
        if len(match) == 0:
            raise ValueError("No file exists for given coordinates.")

        return match[0]
