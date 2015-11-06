# -*- coding: utf-8 -*-

from __future__ import print_function
from HTMLParser import HTMLParser as BaseParser
import urllib, urlparse
import collections
import re


class URL(object):
    """Class is mostly for @classmethods relating to URLs """
    
    @classmethod
    def urlmatch(url,
        schemefilter=lambda s: True,
        weblocfilter=lambda w: True,
        pathfilter=lambda p: True,
        queryfilter=lambda q: True,
        fragfilter=lambda f: True
        ):
        """Tests whether the URL matches the specified filters.
        
        A URL is represented as:
            "[scheme] : [webloc]           [path] [query] [frag]"
        e.g.:
              http    :  www.example.com:80 /      ?q=cat  #anchor 
        
        :param schemefilter: (function) filter the scheme part
        :param weblocfilter: (function) filter the website part
        :param pathfilter: (function) filter the path part
        :param queryfilter: (function) filter the query part
        :param fragfilter: (function) filter the fragment part
        :returns: (bool) ``True'' if matches ; ``False'' otherwise
        """
        res = urlparse.urlparse(url)
        return schemefilter(res.scheme) and
            weblocfilter(res.netloc) and
            pathfilter(res.path) and
            queryfilter(res.query) and
            fragfilter(res.fragment)
        


class WebCorpusBuilder(object):
    """Crawls HTML pages on the web and scrapes text data.
    
    The ``WebCorpusBuilder'' crawls the internet recursively, using a set of simple filters to define its behavior.  The documentation of the filters is below:
    
    URL BASED FILTERS =====================================================
    
    schemefilter    Filter the scheme part of a URL (e.g. http, https)
                    (default: _ => True)
                        
    weblocfilter    Filter the website of the URL (e.g. www.example.com).
                    This includes the full path to the website including a
                    Possible port number (e.g. www.example.com:80), though 
                    This usually is not included. (default: _ => True)
                        
    pathfilter      Filter the path of a URL (e.g. /en/forum/).
                    This often can be used for sites where the URL path
                    Is indicative of the type of page (e.g. Wiki pages)
                    (default: _ => True)
                        
    queryfilter     Filter the query part of a URL (e.g. ?q=cat&s=kitten).
                    The query string is further parsed into a dictionary.
                    (default: _ => True)
                        
    fragfilter      Filter the fragment or anchor of a URL (e.g. #anchor) 
                    (default: _ => True)

                    
    DOCUMENT BASED FILTERS ================================================
                    
    tagfilter       Filter lowercased tag names in the document (e.g. body)
                    The second parameter to the filter is its associated
                    Attributes dictionary. (default: _, _ => True)
                    
    probefilter     Filter entire pages before recursively scraping links.
                    This is usually important to avoid fast growth of Web
                    Pages in the queue.  You might think of something
                    Creative to put here but usually less is more.
                    (default: _ => True)
    
    splitfilter     Filter entire pages and return a list of matches.
                    One could use ``re.findall'' to split results ;
                    Or, one could split the string on sentences using
                    The NLTK module (e.g.: ``nltk.tokenize.sent_tokenize'')
                    (default: _ => re.split(r'\n', _))
                    
    datafilter      Filter each element of the ``splitfilter''.
                    Your implementation should return a truth-value:
                    ``True'' if the data should be accepted ;
                    ``False'' otherwise. (default _ => True)
                    
    writefilter     Write data out to a file or data structure in
                    Any way that you wish.  This filter may return
                    A ``None'' type since its return value is never
                    Used. By default, the write filter prints the
                    Scrape output to stdout. (default _ => print(_))
    """
    
    def __init__(self):
        """Creates a new spider parser"""
        self.schemefilter = lambda p: True
        self.weblocfilter = lambda w: True
        self.pathfilter   = lambda p: True
        self.queryfilter  = lambda q: True
        self.fragfilter   = lambda f: True
        self.tagfilter    = lambda t, a: True
        self.probefilter  = lambda t: True
        self.splitfilter  = lambda p: re.split(r'\n', p)
        self.datafilter   = lambda d: True
        self.writefilter  = lambda d: print(d)
        self.htmlparser   = HTMLParser().init(self)
        self.pagequeue    = collections.deque()
    
    def _urlmatch(self, url):
        """Sugar to match a URL based on this web corpus builder.
        
        :param url: (str) a URL to match
        """
        return URL.urlmatch(url,
            schemefilter=self.schemefilter,
            weblocfilter=self.weblocfilter,
            pathfilter=self.pathfilter,
            queryfilter=self.queryfilter,
            fragfilter=self.fragfilter)
    
    def crawl(url, whilefilter=lambda wcb: len(wcb.pagequeue) > 0):
        """Begins crawling of the web.
        
        It will continue to crawl the web until the given termination conditions in ``termfilter'' are met.
        
        :param url: (str) a URL from which to start crawing
        :param whilefilter: (function) returns ``False'' to stop crawling
        """
        self.pagequeue.append(url)
        while whilefilter(self):
            url = self.pagequeue.pop()
            if self._urlmatch(url):
                res = urllib.urlopen(url)
                data = res.readall().decode("utf-8")
                if self.probefilter(data):
                    self.htmlparser.feed(data)


class HTMLParser(BaseParser):
    """Parses raw HTML and handles scraped text based on the policies defined in a ``WebCorpusBuilder'' object. """
    
    def init(self, webcorpusbuilder):
        """Initializes this parser.
        
        :param webcorpusbuilder: (WebCorpusBuilder)
        """
        self.wcb         = webcorpusbuilder
        self.handledata  = collections.deque([True])
        return self
        
    def handle_starttag(self, tag, attrs):
        """Handles the start of an HTML tag.
        
        :param tag: (str) a lowercased HTML tag name
        :param attrs: (dict) an attribute dictionary mapping,
            attribute name => attribute value
        """
        attrs = dict(attrs)
        handleon = self.wcb.tagfilter(tag, attrs)
        self.handledata.append(bool(handleon))
        print 'start %s' % tag
        if tag == 'a':
            attrs = dict(attrs)
            if 'href' in attrs:
                self.pagequeue.append(attrs['href'])
    
    def handle_endtag(self, tag):
        """Handles the end of a tag.
        
        :param tag: (str) a lowercased HTML tag name
        """
        print 'end %s' % tag
        self.handledata.pop()

    def handle_data(self, data):
        """Handles text data within an HTML tag.
        
        :param 
        """
        if self.handledata[-1]:
            pass


if __name__ == '__main__':
    pass