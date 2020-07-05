import numpy as np
import pytest

from wildfirepy.io.hdf import ReadH5
from wildfirepy.net.usgs import VIIRSBurntAreaDownloader

downloader = VIIRSBurntAreaDownloader()


@pytest.fixture
def file_path(tmpdir):
    return downloader.get_h5(year=2020, month=2, date=1,
                             hours=6, minutes=42, path=tmpdir)


@pytest.mark.remote_data
def test_readH5(file_path):
    reader = ReadH5(file_path)
    reader.tojson()
    components = reader.subDatasets()
    assert len(components) == 4
    assert components[2].name == 'Longitude'
    assert len(reader.json['groups']) == 9
    assert components[1].data[0][0] == np.float32(-66.592575)
