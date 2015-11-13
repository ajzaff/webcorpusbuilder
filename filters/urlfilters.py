class URLFilter(object):
    """Defines a base URL filter. """

    def __call__(self, url):
        """Apply the instance function.

        :param url: (str)
        :return: (bool)
        """
        return True