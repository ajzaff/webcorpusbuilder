# -*- coding: utf-8 -*-

from __future__ import print_function

import urllib

from crawlertools import CrawlerState
from filters import filtertools
from parsertools import HTMLParser


class WebCorpusBuilder(object):
    """Crawls HTML pages on the web and scrapes text data.
    
    The ``WebCorpusBuilder'' crawls the internet recursively, using a set of simple filters to define its behavior.  The documentation of the filters is below:
    
    URL BASED FILTERS =====================================================
    
    urlfilter       Filter a URL (default: _ => True)
  

    DOCUMENT BASED FILTERS ================================================

    tagfilter       Filter lowercased tag names in the document (e.g. body).
                    (default: content tags only see: ``filtertools.tagfilter'')
                    
    probefilter     Filter entire pages before recursively scraping links.
                    This is usually important to avoid fast growth of Web
                    Pages in the queue.  You might think of something
                    Creative to put here but usually less is more.
                    If you are collecting web pages in a specific language
                    This could be a good place to apply the white-list.
                    (default: _ => True)
                    
    datafilter      Filter each element of the ``splitfilter''.
                    Your implementation should return a truth-value:
                    ``True'' if the data should be accepted ;
                    ``False'' otherwise. (default _ => True)

    TEXT PROCESSORS I/O ===================================================

    splitter        Split entire pages and return a list of matches.
                    One could use ``re.findall'' to split results ;
                    Or, one could split the string on sentences using
                    The NLTK module (e.g.: ``nltk.tokenize.sent_tokenize'')
                    (default: _ => [_])

    writer          Write data out to a file or data structure in
                    Any way that you wish.  This filter may return
                    A ``None'' type since its return value is never
                    Used. By default, the write filter prints the
                    Scrape output to stdout. (default _ => print(_))
                    
                    
    TRAVERSAL FUNCTIONS ===================================================

    visitor         Visitor triggered when visiting a webpage.
                    Function takes the URL of the page as argument.
                    Return value is ignored (default: _ => None).

    """
    
    def __init__(self):
        """Creates a new Web Corpus Builder. """
        self.urlfilter = lambda p: True
        self.tagfilter = filtertools.tagfilter
        self.probefilter = lambda t: True
        self.datafilter = lambda d: True
        self.visitor = lambda p: None
        self.splitter = lambda p: [p]
        self.writer = lambda d: print(d)
        self.parser = HTMLParser(self)
        self.crawler = CrawlerState()

    def feed(self, pages):
        """Feeds a set of pages to the crawler and crawls them.
        :param pages:
        :return:
        """
        if not hasattr(pages, '__iter__'):
            pages = [pages]
        for page in pages:
            self.crawler.setpage(page)
            self.crawl(page)

    def crawl(self, page):
        """Initiates crawling of the web once.

        Match the URL against preliminary filters
        First match the URL itself, if this passes,
        Read the contents of the page, then call
        The visit filter. If this passes, run the
        probe filter. If all these pass, then
        Finally, we feed text data to the parser.

        :param page: (str) a page URL to crawl
        """
        try:
            res = urllib.urlopen(page)
            data = res.read().decode("utf-8")
            self.visitor(page)
            if self.probefilter(data):
                self.parser.feed(data)
                for split in self.splitter(self.parser.resdata):
                    if self.datafilter(split):
                        self.writer(split)
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
        except UnicodeDecodeError as e:
            print('=== %s at %s' % (e, page))
        except UnicodeError as e:
            print('=== %s at %s' % (e, page))


#if __name__ == '__main__':
#    import re
#
#    sents = []
#
#    def writer(x):
#        global sents
#        x = x.replace('\n', ' ')
#        x = re.sub(r'(\[.*\])|(\(.*\))', ' ', x)
#        x = nltk.tokenize.word_tokenize(x)
#        sents.append(x)
#
#    import nltk
#    wcb = WebCorpusBuilder()
#    wcb.splitter = nltk.tokenize.sent_tokenize
#    wcb.writer = writer
#    wcb.feed('https://en.wikipedia.org/wiki/Cats')
#
#    for x in wcb.crawler.pages:
#        print(x)
#
#    #for x in sents:
#    #    print(x)