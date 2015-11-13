from HTMLParser import HTMLParser as BaseParser
import urltools


class HTMLParser(BaseParser):
    """Parses raw HTML and handles scraped text based on the policies defined in a ``WebCorpusBuilder'' object. """

    def __init__(self, webcorpusbuilder):
        """Initializes this parser.

        :param webcorpusbuilder: (WebCorpusBuilder)
        """
        BaseParser.__init__(self)
        self.wcb = webcorpusbuilder
        self.resdata = u''

    def handle_starttag(self, tag, attrs):
        """Handles the start of an HTML tag.

        :param tag: (str) a lowercased HTML tag name
        :param attrs: (dict) an attribute dictionary mapping,
            attribute name => attribute value
        """
        attrs = dict(attrs)
        active = self.wcb.tagfilter(tag, self.wcb.crawler)
        self.wcb.crawler.tags.append({'tag': tag, 'active': active})
        if tag == 'a':
            if 'href' in attrs: # Normalize the URL and push it on the queue.
                href = attrs['href']
                base = self.wcb.crawler.url.netloc
                path = self.wcb.crawler.url.path
                page = urltools.urlfmtdefaults(
                    href, defaulthost=base, defaultpath=path)
                if self.wcb.urlfilter(page):
                    self.wcb.crawler.push(page)

    def handle_endtag(self, tag):
        """Handles the end of a tag.

        :param tag: (str) a lowercased HTML tag name
        """
        self.wcb.crawler.tags.pop()

    def handle_data(self, data):
        """Handles text data within an HTML tag.

        :param data: (str) text in within the tag
        """
        if self.wcb.crawler.isactive():
            self.resdata += data