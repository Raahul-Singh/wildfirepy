from pathlib import Path
from datetime import datetime
from urllib.error import HTTPError
from wildfirepy.net.snpp import Viirs1KMParser, URLOpenerWithRedirect
from wildfirepy.coordinates.util import SinusoidalCoordinate

__all__ = ['Viirs1KMDownloader']

path = Path(__file__).parent.parent.parent / "data/VIIRS1KM"

class Viirs1KM:
    def __init__(self, product: str):
        """
        Base Class for VIIRS 1KM products.

        Parameters
        ----------
        product : str
            Product name
        """
        self.product = product
        self.base_url = 'https://e4ftl01.cr.usgs.gov/VIIRS/' + f'{self.product}.001/'

        self.regex_traverser = Viirs1KMParser(self.product, self.base_url)
        self.converter = SinusoidalCoordinate()
        self.url_opener = URLOpenerWithRedirect()

    def get_filename(self, latitude: float, longitude: float):
        """
        Returns name of file for given latitude and longitude.

        Parameters
        ----------
        latitude: float
            latitude of the observation.
        longitude: float
            longitude of the observation.
        """
        h, v = self.converter(latitude, longitude)
        return self.regex_traverser.get_filename(h, v)

    def get_h5(self, *, obsdate: str, latitude: float, 
               longitude: float, fmt: str= "%Y-%m-%d", **kwargs):
        """
        Downloads the `h5` file and stores it on the disk.

        Parameters
        ----------
        obsdate : str
            The date of observation.
        latitude: float
            latitude of the observation.
        longitude: float
            longitude of the observation.
        fmt : str, optional
            The format in which the obsdate is given,
            by default "%Y-%m-%d"

        Returns
        -------
        filepath : str
            path to the downloaded h5 file.
        """
        obsdate = datetime.strptime(obsdate, fmt)
        date = obsdate.strftime("%Y.%m.%d") + '/'
        self.regex_traverser(self.base_url + date)

        filename = self.get_filename(latitude, longitude)
        url = self.base_url + date + filename
        return self.fetch(url=url, filename=filename, **kwargs)

    def get_xml(self, *, obsdate: str, latitude: float, 
                longitude: float, fmt: str= "%Y-%m-%d", **kwargs):
        """
        Downloads the `xml` file and stores it on the disk.

        Parameters
        ----------
        obsdate : str
            The date of observation.
        latitude: float
            latitude of the observation.
        longitude: float
            longitude of the observation.
        fmt : str, optional
            The format in which the obsdate is given,
            by default "%Y-%m-%d"

        Returns
        -------
        filepath : str
            path to the downloaded xml file.
        """
        obsdate = datetime.strptime(obsdate, fmt)
        date = obsdate.strftime("%Y.%m.%d") + '/'
        self.regex_traverser(self.base_url + date)

        filename = self.get_filename(latitude, longitude) + ".xml"
        url = self.base_url + date + filename
        return self.fetch(url=url, filename=filename, **kwargs)

    def get_jpg(self, *, obsdate: str, latitude: float, 
                longitude: float, fmt: str= "%Y-%m-%d", **kwargs):
        """
        Downloads the `jpg` file and stores it on the disk.

        Parameters
        ----------
        obsdate : str
            The date of observation.
        latitude: float
            latitude of the observation.
        longitude: float
            longitude of the observation.
        fmt : str, optional
            The format in which the obsdate is given,
            by default "%Y-%m-%d"

        Returns
        -------
        filepath : str
            path to the downloaded jpg file.
        """
        self.obsdate = datetime.strptime(obsdate, fmt)
        self.base_url += self.obsdate.strftime("%Y.%m.%d") + '/'

        filename = "BROWSE." + self.get_filename(latitude, longitude)[:-3] + "1.jpg"

        url = self.base_url + filename
        return self.fetch(url=url, filename=filename, **kwargs)

    def fetch(self, url, path=str(path), filename='temp.h5'):
        """
        Fetches data from url.

        Parameters
        ----------
        url : str
            URL to get the data from.
        path : str
            path to store the downladed file,
            by default stores in ~wildfirepy/data/VIIRS1KM
        filename : str
            name of the downladed file.

        Returns
        -------
        path : str
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


class VNP14A1(Viirs1KM):
    """
    Class for VNP14A1 product, i.e., Thermal Anomalies/Fire.
    """
    def __init__(self):
        super().__init__(product='VNP14A1')


class VNP09GA(Viirs1KM):
    """
    Class for VNP09GA product, i.e., daily surface reflectance.
    """
    def __init__(self):
        super().__init__(product='VNP09GA')


class Viirs1KMDownloader():

    def __init__(self):
        self.surface_client = VNP09GA()
        self.fire_client = VNP14A1()

    def get_data(self, *, obsdate: str, latitude: float, 
                longitude: float, fmt: str= "%Y-%m-%d", **kwargs):
        
        surface = self.surface_client.get_h5(obsdate=obsdate, latitude=latitude, longitude=longitude, **kwargs)
        
        fire_data = self.fire_client.get_h5(obsdate=obsdate, latitude=latitude, longitude=longitude, **kwargs)

        return {'surface' : surface,
                'fire data' : fire_data}

