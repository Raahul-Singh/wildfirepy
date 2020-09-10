from wildfirepy.io import Viirs1KmLoader

__all__ = ['MapFactory']


class Io:
    def __init__(self):
        self.Viirs1KmLoader = Viirs1KmLoader()


class MapFactory(Io):
    def __init__(self, files, **kwargs):
        super().__init__()
        self.files = files
        self.kwargs = kwargs

    def load_data(self):
        if isinstance(self.files, dict) and len(self.files) == 2:
            if set(['surface', 'fire']) == self.files.keys():
                return self.Viirs1KmLoader.get_data(self.files)

        elif set(['latitude', 'longitude', 'obsdate']).issubset(self.kwargs):
            data = self.Viirs1KmLoader.Viirs1KMDownloader.get_data(**self.kwargs)
            return self.Viirs1KmLoader.get_data(data)
