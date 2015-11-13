import collections
import urltools, urlparse


class CrawlerState(object):
    """The state of the crawler. """

    def __init__(self):
        """Creates a new ``CrawlerState'' instance. """
        self.pages = collections.deque()
        self.tags = collections.deque()
        self.url = None
        self.page = None

    def setpage(self, page):
        """Sets the page the crawler is pointing at.

        :param page: (str) a page URL
        """
        self.url = urlparse.urlparse(page)
        self.page = page

    def push(self, page):
        """Appends a page to the deque.

        :param page: (str) a page URL
        """
        self.pages.append(page)

    def pop(self):
        """Removes and returns a page from the deque.

        :return (str): the next page
        """
        self.page = self.pages.pop()
        return self.page

    def isactive(self):
        """Returns whether the crawler is active.

        :return (bool): whether the crawler is active
        """
        return True if len(self.tags) == 0 else self.tags[-1]['active']

    def isintag(self, tag):
        """Returns whether inside ``tag''.

        :param tag: (str) a tag to be inside of
        :return (bool): ``True'' if inside; ``False'' otherwise
        """
        for e in self.tags:
            if e['tag'] == tag:
                return True
        return False