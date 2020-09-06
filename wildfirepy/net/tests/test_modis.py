import subprocess
from xml.dom import minidom

import pytest
from wildfirepy.net.usgs import ModisBurntAreaDownloader
from wildfirepy.net.util import MODISHtmlParser, URLOpenerWithRedirect

opener = URLOpenerWithRedirect()
downloader = ModisBurntAreaDownloader()


@pytest.fixture
def parser():
    return MODISHtmlParser(product="MCD64A1")


@pytest.fixture
def obs_coordinates():
    return {'latitude': 28.7041,
            'longitude': 77.1025}


@pytest.fixture
def obs_date():
    return {'year': 2020,
            'month': 2,
            'day': 1}


def get_cksum_size(file):
    result = subprocess.run(['cksum', file], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').split()
    return output


@pytest.mark.remote_data
def test_fetch(tmpdir, obs_date, obs_coordinates):

    hdf_file = downloader.get_hdf(year=obs_date['year'], month=obs_date['month'],
                                  latitude=obs_coordinates['latitude'],
                                  longitude=obs_coordinates['longitude'], path=tmpdir)
    xml_file = downloader.get_xml(year=obs_date['year'], month=obs_date['month'],
                                  latitude=obs_coordinates['latitude'],
                                  longitude=obs_coordinates['longitude'], path=tmpdir)

    xml_data = minidom.parse(xml_file)

    checksum_upstream = xml_data.getElementsByTagName('Checksum')[0].firstChild.nodeValue
    filesize_upstream = xml_data.getElementsByTagName('FileSize')[0].firstChild.nodeValue

    checksum, filesize, _ = get_cksum_size(hdf_file)

    assert checksum_upstream == checksum
    assert filesize_upstream == filesize


@pytest.mark.remote_data
def test_all_files_visible(parser):

    parser('https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.006/2020.02.01/')

    hdf_files = parser.get_all_hdf_files()
    xml_files = parser.get_all_xml_files()
    jpg_files = parser.get_all_jpg_files()

    assert len(hdf_files) == len(xml_files) == len(jpg_files)


@pytest.mark.remote_data
def test_filename_exists(parser):
    parser('https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.006/2020.02.01/')

    name = parser.get_filename(35, 10)

    assert name == 'MCD64A1.A2020032.h35v10.006.2020102114146.hdf'


@pytest.mark.remote_data
def test_filename_does_not_exists(parser):
    parser('https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.006/2020.02.01/')

    with pytest.raises(ValueError):
        parser.get_filename(35, 11)
