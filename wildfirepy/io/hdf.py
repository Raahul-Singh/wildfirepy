import h5py
from h5json import Hdf5db
from h5json.h5tojson.h5tojson import DumpJson
from munch import munchify

__all__ = ['ReadH5']


class ReadH5:
    """
    A class to make read objects for h5 files.

    Parameters
    ----------
    filepath: `str`
        Path to the hdf file.
    """

    def __init__(self, filepath='/'):
        self.path = filepath
        self.name = filepath.split('/')[-1]
        self.json = None

    def tojson(self):
        db = Hdf5db(self.path, dbFilePath=self.path, app_logger=None)
        # `options_dict` is used to surpress data outputs.
        # If both set to `False`, operations takes a lot of time to copy all
        # Dataset values to json.
        options_dict = {'D': True, 'd': False}
        args = munchify(options_dict)
        dumper = DumpJson(db, app_logger=None, options=args)
        dumper.dumpFile()
        self.json = dumper.json
        return self.json

    def subDatasets(self):
        """
        Returns
        -------
        `list`
            A list of munchified subdataset objects.
        """
        if self.json is None:
            print('Use <obj>.tojson() method to convert HDF File to json first!')
            return
        dsetnames = list()
        h5file = h5py.File(self.path, "r")
        dsets = self.json['datasets']
        subdsets = list()
        for i in dsets:
            dsetnames.append(i)
        for name in dsetnames:
            dset_dict = {}
            dset_dict['metadata'] = dsets[name]
            dset_dict['name'] = dsets[name]['alias'][0].split('/')[-1]
            dset_dict['data'] = h5file[dsets[name]['alias'][0]][...]
            subdsets.append(munchify(dset_dict))
        return subdsets
