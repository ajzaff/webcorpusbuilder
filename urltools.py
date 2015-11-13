import urlparse


def urlfmtdefaults(
        url, defaultscheme='http',
        defaulthost=None, defaultpath=None):
    """Appends defaults to a URL if missing.

    :param url: (str)
    :param defaultscheme: (str)
    :param defaulthost: (str)
    :param defaultpath: (str)
    """
    res = urlparse.urlparse(url)
    scheme = defaultscheme if not res.scheme else res.scheme
    netloc = defaulthost if not res.hostname else res.hostname
    path = defaultpath if not res.path else res.path

    res = urlparse.ParseResult(
        scheme, netloc, path, '',
        res.query, res.fragment)
    return urlparse.urlunparse(res)