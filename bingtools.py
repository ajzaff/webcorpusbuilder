from corpustools import WebCorpusBuilder
import urllib, urlparse
import re


def bingurl(query, quotes=False, language=None, first=None):
    """Computes a bing search URL from a query.

    :param query: (str) the query string
    :param quotes: (bool) whether to quote the query string
    :param language: (str) an ISO 2-letter language code
    :param first: (int) the first result to search from
    """
    base = 'https://www.bing.com/search?q=%s'
    q = '"%s"' % query if quotes else '%s' % query
    cc = '' if not language else '&cc=%s' % language
    f = '' if not first else '&first=%d' % first
    return base % ('%s%s%s' % (urllib.quote(q), cc, f))


def bingsearch(query, quotes=False, language=None, results=50):
    """Collects the first ``limit'' links from a Bing query.

    :param query: (str) the query string to ask Bing
    :param quotes: (bool) whether to quote the query string
    :param language: (str) an ISO 2-letter language code
    :param results: (int) the result limit (default: 50)
    :return (list): a list of web pages from this query.
    """
    wcb = WebCorpusBuilder()
    wcb.urlfilter = lambda u:\
        not re.match(r'^.*//.*bing.com', u) and\
        not re.match(r'^.*//.*microsoft.com', u) and\
        not re.match(r'^.*//.*microsofttranslator.com', u) and\
        not re.match(r'^.*//.*dictionary.*', u)
    wcb.writer = lambda t: None

    i = 0
    while i < results:
        url = bingurl(query, quotes=quotes, language=language, first=i)
        wcb.feed(url)
        i = len(wcb.crawler.pages)
    return list(wcb.crawler.pages)[0:results]