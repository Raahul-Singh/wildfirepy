from wildfirepy.coordinates.util import SinusoidalCoordinate
from wildfirepy.net.usgs.usgs_downloader import AbstractUSGSDownloader
from wildfirepy.net.util import MODISHtmlParser

__all__ = ['ModisBurntAreaDownloader']


class Modis(AbstractUSGSDownloader):
    """
    An Abstract Base Class Downloader for MODIS products.
    """
    def __init__(self, data='MOTA', product=''):
        super().__init__()
        self.regex_traverser = MODISHtmlParser(product)
        self.converter = SinusoidalCoordinate()
        self.base_url += f"{data}/"

    def get_available_dates(self):
        """
        Returns dates for which data is available.
        """
        self.regex_traverser(self.base_url)
        return self.regex_traverser.get_all_dates()

    def get_files_from_date(self, year, month):
        """
        Returns names of all available files.
        Parameters
        ----------
        year: `int`
            Year for which filenames are to be retrieved.
        month: `int`
            Month for which filenames are to be retrieved.
        """
        month = str(month) if month > 9 else "0" + str(month)
        date = f"{str(year)}.{month}.01/"
        self.regex_traverser(self.base_url + date)
        self.has_files = True
        return self.regex_traverser.get_all_files()

    def get_available_jpg_files(self):
        """
        Returns names of available jpg files.
        """
        return self.regex_traverser.get_all_jpg_files()

    def get_available_xml_files(self):
        """
        Returns names of available xml files.
        """
        return self.regex_traverser.get_all_xml_files()

    def get_available_hdf_files(self):
        """
        Returns names of available hdf files.
        """
        return self.regex_traverser.get_all_hdf_files()

    def get_filename(self, latitude, longitude):
        """
        Returns name of file for given latitude and longitude.

        Parameters
        ----------
        latitude: `float`
            latitude of the observation.
        longitude: `float`
            longitude of the observation.
        """
        h, v = self.converter(latitude, longitude)
        return self.regex_traverser.get_filename(h, v)

    def get_hdf(self, *, year, month, latitude, longitude, **kwargs):
        """
        Downloads the `hdf` file and stores it on the disk.

        Parameters
        ----------
        year: `int`
            Year of the observation.
        month: `int`
            Month of the observation.
        latitude: `float`
            latitude of the observation.
        longitude: `float`
            longitude of the observation.
        kwargs: keyword arguments to be passed to `AbstractUSGSDownloader.fetch`

        Returns
        -------
        path: `str`
            Absolute path to the downloaded `hdf` file.
        """
        if not self.has_files:
            self.get_files_from_date(year, month)

        filename = self.get_filename(latitude, longitude)
        month = str(month) if month > 9 else "0" + str(month)
        date = f"{str(year)}.{month}.01/"
        url = self.base_url + date + filename
        return self.fetch(url=url, filename=filename, **kwargs)

    def get_xml(self, *, year, month, latitude, longitude, **kwargs):
        """
        Downloads the `xml` file and stores it on the disk.

        Parameters
        ----------
        year: `int`
            Year of the observation.
        month: `int`
            Month of the observation.
        latitude: `float`
            latitude of the observation.
        longitude: `float`
            longitude of the observation.
        kwargs: keyword arguments to be passed to `AbstractUSGSDownloader.fetch`

        Returns
        -------
        path: `str`
            Absolute path to the downloaded `xml` file.
        """
        if not self.has_files:
            self.get_files_from_date(year, month)

        filename = self.get_filename(latitude, longitude) + ".xml"

        month = str(month) if month > 9 else "0" + str(month)
        date = f"{str(year)}.{month}.01/"
        url = self.base_url + date + filename
        return self.fetch(url=url, filename=filename, **kwargs)

    def get_jpg(self, *, year, month, latitude, longitude, **kwargs):
        """
        Downloads the `jpg` file and stores it on the disk.

        Parameters
        ----------
        year: `int`
            Year of the observation.
        month: `int`
            Month of the observation.
        latitude: `float`
            latitude of the observation.
        longitude: `float`
            longitude of the observation.
        kwargs: keyword arguments to be passed to `AbstractUSGSDownloader.fetch`

        Returns
        -------
        path: `str`
            Absolute path to the downloaded `jpg` file.
        """
        if not self.has_files:
            self.get_files_from_date(year, month)

        filename = "BROWSE." + self.get_filename(latitude, longitude)[:-3] + "1.jpg"

        month = str(month) if month > 9 else "0" + str(month)
        date = f"{str(year)}.{month}.01/"
        url = self.base_url + date + filename
        return self.fetch(url=url, filename=filename, **kwargs)


class ModisBurntAreaDownloader(Modis):
    """
    MODIS Class for `MCD64A1`, i.e., Burnt Area.
    By default downloads data from the 6th collection.
    """
    def __init__(self, collection='006'):
        super().__init__(product="MCD64A1")
        self.base_url = self.base_url + f"MCD64A1.{collection}/"
