import pytest
import subprocess
from xml.dom import minidom
from wildfirepy.net.usgs import VIIRSBurntAreaDownloader
from wildfirepy.net.util import URLOpenerWithRedirect, VIIRSHtmlParser

opener = URLOpenerWithRedirect()
downloader = VIIRSBurntAreaDownloader()


@pytest.fixture
def parser():
    return VIIRSHtmlParser()


@pytest.fixture
def obs_time():
    return {'hours': 6,
            'minutes': 42}


@pytest.fixture
def obs_date():
    return {'year': 2020,
            'month': 2,
            'date': 1}


def get_cksum_size(file):
    result = subprocess.run(['cksum', file], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').split()
    return output


@pytest.mark.remote_data
def test_fetch(tmpdir, obs_date, obs_time):

    hdf_file = downloader.get_h5(year=obs_date['year'], month=obs_date['month'],
                                 date=obs_date['date'], hours=obs_time['hours'],
                                 minutes=obs_time['minutes'], path=tmpdir)
    xml_file = downloader.get_xml(year=obs_date['year'], month=obs_date['month'],
                                  date=obs_date['date'], hours=obs_time['hours'],
                                  minutes=obs_time['minutes'], path=tmpdir)

    xml_data = minidom.parse(xml_file)

    checksum_upstream = xml_data.getElementsByTagName('Checksum')[0].firstChild.nodeValue
    filesize_upstream = xml_data.getElementsByTagName('FileSize')[0].firstChild.nodeValue

    checksum, filesize, _ = get_cksum_size(hdf_file)

    assert checksum_upstream == checksum
    assert filesize_upstream == filesize
