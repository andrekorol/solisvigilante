import urllib.error
import urllib.request
from os.path import join, abspath
from shutil import move


def download_from_url(url, save_dir=None):
    """
    Downloads the file found at the given url

    :param url: url string of a file to be downloaded
    :param save_dir: directory to save downloaded file. If omitted, the file is saved in the current working directory
    :returns: absolute path of file downloaded from the given url
    :raises urllib.error.URLError: raises an exception when an invalid url is
    given as argument
    """
    try:
        downloaded_file = urllib.request.urlretrieve(url, url.split('/')[-1])
        filename = downloaded_file[0]

        if save_dir is not None:
            file_path = join(save_dir, filename)
            move(filename, file_path)
            urllib.request.urlcleanup()
            return abspath(file_path)

        urllib.request.urlcleanup()
        return abspath(filename)

    except urllib.error.URLError as e:
        urllib.request.urlcleanup()
        print("{}: Name or service not known".format(url))
        raise e
