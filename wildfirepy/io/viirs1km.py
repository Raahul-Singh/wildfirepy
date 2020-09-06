import h5py
from wildfirepy.net import Viirs1KMDownloader

__all__ = ['Viirs1KmLoader']


class Viirs1KmLoader:
    def __init__(self):
        self.Viirs1KMDownloader = Viirs1KMDownloader()

    def get_data(self, data):
        surface_data = h5py.File(data['surface'], 'r')
        fire_data = h5py.File(data['fire'], 'r')
        return {'surface': surface_data, 'fire': fire_data, 'datatype': 'Viirs1Km'}

    def list_all_keys(self, data):
        return list(data.keys())

    def get_hdfeos(self, data):
        return list(data['HDFEOS'])

    def get_grids(self, data):
        return list(data['HDFEOS']['GRIDS'])

    def get_1KM_surface_datafields(self, data):
        return list(data['HDFEOS']['GRIDS']['VNP_Grid_1km_2D']['Data Fields'])

    def get_firemask(self, data):
        return data['HDFEOS/GRIDS/VNP14A1_Grid/Data Fields/FireMask'][()]

    def get_fire_datafields(self, data):
        return list(data['fire']['HDFEOS']['GRIDS']['VNP14A1_Grid']['Data Fields'])
