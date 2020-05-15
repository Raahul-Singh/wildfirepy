from wildfirepy.net.usgs.USGSdownloader import AbstractUSGSDownloader
from wildfirepy.net.util.usgs import VIIRSHtmlParser
import datetime

__all__ = ['VIIRSBurntAreaDownloader']

class Viirs(AbstractUSGSDownloader):
    """
    Description
    -----------
    An Abstract Base Class Downloader for VIIRS products.
    """
    def __init__(self, product=''):
        super().__init__()
        self.product = product
        self.base_url += "VIIRS/" f'{self.product}.001/'
        self.regex_traverser = VIIRSHtmlParser(product=product)

    def _get_nearest_time(self, hours, minutes):
        
        if not 0 <= minutes < 60:
            raise ValueError("Minutes must be between 0 and 60")

        if not 0 <= hours < 24:
            raise ValueError("Hours must be between 0 and 24")

        minutes = minutes - minutes % 6
        minutes = str(minutes) if minutes > 9 else f"0{str(minutes)}"
        hours = str(hours) if hours > 9 else f"0{str(hours)}"

        return f'{hours}{minutes}'

    def _get_date(self, year, month, date):
        """

        """
        dt = f'{year}.{month}.{date}'
        fmt = f'%Y.%m.%d'
        dt = datetime.datetime.strptime(dt, fmt)

        julian_day = dt.timetuple().tm_yday

        month = str(dt.month) if dt.month > 9 else f'0{str(dt.month)}'
        date = str(dt.day) if dt.day > 9 else f'0{dt.day}'

        return f'{year}.{month}.{date}', julian_day

    def get_h5(self, *, year, month, date, hours, minutes, **kwargs):
        """
        Downloads the `h5` file and stores it on the disk.
        
        Parameters
        ----------
        year: `int`
            Year of the observation.
        month: `int`
            Month of the observation.
        date: `int`
            Date of observation.
        hours: `int`
            Hour of observation. UTC time.
        minutes: `int`
            Minute of observation. UTC time. 
        kwargs: `dict`
            keyword arguments to be passed to `AbstractUSGSDownloader.fetch`

        Returns
        -------
        path: `str`
            Absolute path to the downloaded `h5` file.
        """
        date, julian_day = self._get_date(year=year, month=month, date=date)
        time = self._get_nearest_time(hours=hours, minutes=minutes)

        self.regex_traverser(self.base_url + date)

        filename = f"{self.product}.A{year}{'%03d' % julian_day}.{time}.001."
        filename = self.regex_traverser.get_filename(filename)
        url = self.base_url + date + '/' + filename
        return self.fetch(url=url, filename=filename, **kwargs)

    def get_xml(self, *, year, month, date, hours, minutes, **kwargs):
        """
        Downloads the `xml` file and stores it on the disk.
        
        Parameters
        ----------
        year: `int`
            Year of the observation.
        month: `int`
            Month of the observation.
        date: `int`
            Date of observation.
        hours: `int`
            Hour of observation. UTC time.
        minutes: `int`
            Minute of observation. UTC time. 
        kwargs: `dict`
            keyword arguments to be passed to `AbstractUSGSDownloader.fetch`

        Returns
        -------
        path: `str`
            Absolute path to the downloaded `xml` file.
        """
        date, julian_day = self._get_date(year=year, month=month, date=date)
        time = self._get_nearest_time(hours=hours, minutes=minutes)

        filename = f"{self.product}.A{year}{'%03d' % julian_day}.{time}.001."
        filename = self.regex_traverser.get_filename(filename) + '.xml'
        url = self.base_url + date + '/' + filename
        return self.fetch(url=url, filename=filename, **kwargs)


class VIIRSBurntAreaDownloader(Viirs):
    """
    Description
    -----------
    VIIRS Class for `VNP03MODLL`, i.e., Burnt Area.
    """
    def __init__(self):
        super().__init__(product="VNP03MODLL")
