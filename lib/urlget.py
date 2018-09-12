import urllib.error
import urllib.request


def download_from_url(url):
    """
    Downloads the file found at the given url

    :param url: url string of a file to be downloaded
    :returns: the name of the file downloaded from the given url
    :raises urllib.error.URLError: raises an exception when an invalid url is
    given as argument
    """
    filename = url.split('/')[-1]
    try:
        downloaded_file = urllib.request.urlretrieve(url, filename)
        urllib.request.urlcleanup()
    except urllib.error.URLError as e:
        urllib.request.urlcleanup()
        print(f'{url}: Name or service not known')
        raise e

    return downloaded_file[0]
