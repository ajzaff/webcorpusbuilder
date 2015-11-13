import urlparse


def urlmatch(url,
             schemefilter=lambda s: True,
             weblocfilter=lambda w: True,
             pathfilter=lambda p: True,
             queryfilter=lambda q: True,
             fragfilter=lambda f: True
             ):
    """Tests whether the URL matches the specified filters.

    A URL is represented as:
        "[scheme] :// [webloc]           [path] [query] [frag]" (e.g.:
          http    ://  www.example.com:80 /      ?q=cat  #anchor )

    :param schemefilter: (function) filter the scheme part
    :param weblocfilter: (function) filter the website part
    :param pathfilter: (function) filter the path part
    :param queryfilter: (function) filter the query part
    :param fragfilter: (function) filter the fragment part
    :returns: (bool) ``True'' if matches ; ``False'' otherwise
    """
    res = urlparse.urlparse(url)
    return schemefilter(res.scheme) and \
        weblocfilter(res.netloc) and \
        pathfilter(res.path) and \
        queryfilter(res.query) and \
        fragfilter(res.fragment)


def urlstem(url,
            clipscheme=True,
            clipwebloc=False,
            clippath=False,
            clipquery=True,
            clipfrag=True
            ):
    """Stems the URL by clipping certain parts of it.

    :param url: (str) a URL
    :param clipscheme: (bool)
    :param clipwebloc: (bool)
    :param clippath: (bool)
    :param clipquery: (bool)
    :param clipfrag: (bool)
    :return: (str) a processed URL string
    """
    res = urlparse.urlparse(url)
    res = urlparse.ParseResult(
        '' if clipscheme else res.scheme,
        '' if clipwebloc else res.netloc,
        '' if clippath else res.path, '',
        '' if clipquery else res.query,
        '' if clipfrag else res.fragment)
    return urlparse.urlunparse(res)


def urlfmtdefaults(url,
                   defaultscheme='http',
                   defaulthost=None,
                   defaultpath=None
                   ):
    """Appends defaults to a URL if missing.

    :param url: (str)
    :param defaultscheme: (str)
    :param defaulthost: (str)
    """
    res = urlparse.urlparse(url)
    res = urlparse.ParseResult(
        defaultscheme if res.scheme == '' else res.scheme,
        res.netloc,
        res.path, '',
        res.query,
        res.fragment)
    url = urlparse.urlunparse(res)
    res = urlparse.urlparse(url)
    res = urlparse.ParseResult(
        res.scheme,
        defaulthost if res.netloc == '' else res.netloc,
        res.path, '',
        res.query,
        res.fragment)
    return urlparse.urlunparse(res)