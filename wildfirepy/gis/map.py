import h5py
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure

from wildfirepy.gis.mapfactory import MapFactory

__all__ = ['Map']


class Map(MapFactory):

    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)
        if data is None and len(kwargs) == 0:
            raise ValueError

        self.data = self.load_data()

    def _get_all_objects(self, data):
        h5_objs = []
        data.visit(h5_objs.append)
        return h5_objs

    def _get_all_datasets(self, data):
        grids = self.Viirs1KmLoader.get_grids(data)
        h5_objs = self._get_all_objects(data)
        all_datasets = [obj for grid in grids for obj in h5_objs if isinstance(data[obj], h5py.Dataset) and grid in obj]
        return all_datasets

    def get_all_fire_objects(self):
        return self._get_all_objects(self.data['fire'])

    def get_all_surface_objects(self):
        return self._get_all_objects(self.data['surface'])

    def get_all_fire_datasets(self):
        return self._get_all_datasets(self.data['fire'])

    def get_all_surface_datasets(self):
        return self._get_all_datasets(self.data['surface'])

    def get_surface_rgb(self):
        all_datasets = self.get_all_surface_datasets()
        r = self.data['surface'][[a for a in all_datasets if 'M5' in a][0]]  # M5 = Red
        g = self.data['surface'][[a for a in all_datasets if 'M4' in a][0]]  # M4 = Green
        b = self.data['surface'][[a for a in all_datasets if 'M3' in a][0]]  # M3 = Blue
        n = self.data['surface'][[a for a in all_datasets if 'M7' in a][0]]  # M7  = NIR
        return r, g, b, n

    def get_attributes_of_rgb(self, color):
        return list(color.attrs)

    def get_scale_value(self, color):
        return color.attrs['Scale'][0]

    def get_fill_value(self, color):
        return color.attrs['_FillValue'][0]

    def get_scaled_stacked_rgb(self):
        r, g, b, n = self.get_surface_rgb()
        scaleFactor = self.get_scale_value(r)
        fillValue = self.get_fill_value(r)
        red = r[()] * scaleFactor
        green = g[()] * scaleFactor
        blue = b[()] * scaleFactor
        n[()] * scaleFactor
        rgb = np.dstack((red, green, blue))
        rgb[rgb == fillValue * scaleFactor] = 0
        return rgb

    def apply_contrast_stretch_gamma_correction(self, rgb):
        p2, p98 = np.percentile(rgb, (2, 98))                               # Calculate 2nd,98th percentile for updating min/max vals
        rgbStretched = exposure.rescale_intensity(rgb, in_range=(p2, p98))  # Perform contrast stretch on RGB range
        rgbStretched = exposure.adjust_gamma(rgbStretched, 0.5)             # Perform Gamma Correction
        return rgbStretched

    def get_corrected_rgb_image(self):
        firemask = self.Viirs1KmLoader.get_firemask(self.data['fire'])
        rgb = self.get_scaled_stacked_rgb()
        rgbStretched = self.apply_contrast_stretch_gamma_correction(rgb)
        fig = plt.figure(figsize=(15, 15), dpi=100)                           # Set the figure size
        ax = plt.Axes(fig, [0, 0, 1, 1])
        ax.set_axis_off()  # Turn off axes
        fig.add_axes(ax)

        firemask[firemask != 9] = 0
        pts = list(zip(np.where(firemask != 0)[0], np.where(firemask != 0)[1]))

        ax.imshow(rgbStretched)  # Plot a natural color RGB

        for i, j in pts:
            plt.annotate('Fire!', xy=(j, i), xycoords='data',
                         xytext=(0.5, 0.5), textcoords='figure fraction',
                         arrowprops=dict(arrowstyle="->"))
        plt.show()
