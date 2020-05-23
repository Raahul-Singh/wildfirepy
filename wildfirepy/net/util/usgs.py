import urllib
import urllib.request
from urllib.request import HTTPPasswordMgrWithDefaultRealm
from urllib.request import HTTPBasicAuthHandler, HTTPCookieProcessor
from http.cookiejar import CookieJar
import re

__all__ = ['URLOpenerWithRedirect', 'MODISHtmlParser', 'VIIRSHtmlParser']

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


class MODISHtmlParser:
    """
    Description
    -----------
    A Regex based HTML parser for USGS MODIS data server.
    When called with a URL, stores the HTML page as an `str`.
    """
    def __init__(self, product=''):
        self.url_opener = URLOpenerWithRedirect()
        self.product = product

    def __call__(self, url):
        self.html_content = self.url_opener(url).read().decode('cp1252')

    def get_all_hdf_files(self):
        """
        Returns list of all `hdf` files available for download.
        """
        return re.findall(r'' + f'href="({self.product}.*hdf)"', self.html_content)

    def get_all_jpg_files(self):
        """
        Returns list of all `jpg` files available for download.
        """
        return re.findall(r'href="(BROWSE.*jpg)"', self.html_content)

    def get_all_xml_files(self):
        """
        Returns list of all `xml` files available for download.
        """
        return re.findall(r'' + f'href="({self.product}.*hdf.xml)"', self.html_content)

    def get_all_files(self):
        """
        Returns list of all `xml` files available for download.
        """
        return self.get_all_hdf_files() + self.get_all_jpg_files() + self.get_all_xml_files()

    def get_all_dates(self):
        """
        Returns list of all `dates` from which files can be downloaded.
        """
        return re.findall(r'"(2.*)/"', self.html_content)

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

        match = list(filter(r.match, self.get_all_hdf_files()))
        if len(match) == 0:
            raise ValueError("No file exists for given coordinates.")

        return match[0]


class VIIRSHtmlParser:
    """
    Description
    -----------
    A Regex based HTML parser for USGS VIIRS data server.
    When called with a URL, stores the HTML page as an `str`.
    """
    def __init__(self, product=''):
        self.url_opener = URLOpenerWithRedirect()

    def __call__(self, url):
        self.html_content = self.url_opener(url).read().decode('cp1252')

    def get_filename(self, partial):
        return re.findall(r'' + f'>({partial}.*h5)', self.html_content)[0]
