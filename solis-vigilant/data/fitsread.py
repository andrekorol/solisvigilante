import gzip
import urllib.error
import urllib.request


def download_from_url(url):
    """Assumes: url is a string

    Returns the name of the file downloaded from the given url"""
    filename = url.split('/')[-1]
    try:
        downloaded_file = urllib.request.urlretrieve(url, filename)
        urllib.request.urlcleanup()
    except urllib.error.URLError:
        urllib.request.urlcleanup()
        print(f'{url}: Name or service not known')
        return
    return downloaded_file[0]


def decompress_gzip_file(filename):
    """Assumes: filename is a string

    Returns the name of the decompressed file"""
    file_extension = filename.split('.')[-1]
    if file_extension == 'gz':
        with gzip.open(filename, 'rb') as f:
            file_content = f.read()
        decompressed_file = '.'.join(filename.split('.')[:-1])
        with open(decompressed_file, 'wb') as f:
            f.write(file_content)
    else:
        print(f'{filename} is not a gzipped file')
        return
    return decompressed_file


class FitsFile(object):
    """Class for reading FITS files"""
    def __init__(self, filename):
        self.filename = filename


file = download_from_url('http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_'
                         '20110809_083004_24.fit.gz')
print(file)

decompressed_file_gz = decompress_gzip_file(file)
print(decompressed_file_gz)
