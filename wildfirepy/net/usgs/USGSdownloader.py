from wildfirepy.net.util import URLOpenerWithRedirect
from wildfirepy.coordinates.util import SinusoidalCoordinate
from pathlib import Path
from urllib.error import HTTPError

__all__ = ['AbstractUSGSDownloader']

class AbstractUSGSDownloader:
    """
    Description
    -----------
    An Abstract Base Class Downloader for USGS products.
    """
    def __init__(self):
        self.base_url = 'https://e4ftl01.cr.usgs.gov/'
        self.url_opener = URLOpenerWithRedirect()
        self.has_files = False

    def _get_available_dates(self):
        """
        Returns dates for which data is available.
        """
        raise NotImplementedError

    def _get_files_from_date(self):
        """
        Returns names of all available files.
        """
        raise NotImplementedError

    def _get_available_jpg_files(self):
        """
        Returns names of available jpg files.
        """
        raise NotImplementedError

    def _get_available_xml_files(self):
        """
        Returns names of available xml files.
        """
        raise NotImplementedError

    def _get_available_h5_files(self):
        """
        Returns names of available h5 files.
        """
        raise NotImplementedError

    def _get_filename(self):
        """
        Returns name of file for given latitude and longitude.
        """
        raise NotImplementedError

    def _get_h5(self):
        """
        Downloads the `h5` file and stores it on the disk.
        """
        raise NotImplementedError

    def _get_xml(self):
        """
        Downloads the `xml` file and stores it on the disk.
        """
        raise NotImplementedError

    def _get_jpg(self):
        """
        Downloads the `jpg` file and stores it on the disk.
        """
        raise NotImplementedError

    def fetch(self, url, path='./', filename='temp.h5'):
        """
        Fetches data from `url`.
        Parameters
        ----------
        url: `str`
            URL to get the data from.
        path: `str`
            path to store the downladed file.
        filename: `str`
            name of the downladed file.
        Returns
        -------
        path: `str`
            Absolute path to the downloaded file.
        """
        data_folder = Path(path)
        filename = data_folder / filename
        try:
            response = self.url_opener(url)
            print("Download Successful!")
            print("Writing file!")
            with open(filename, 'wb') as file:
                file.write(response.read())
            response.close()
            return filename.absolute().as_posix()

        except HTTPError as err:
            output = format(err)
            print(output)
