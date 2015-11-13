tag_blacklist = {
    'base', 'meta', 'link',
    'style', 'script', 'br',
    'hr', 'img', 'map', 'area',
    'object', 'param', 'col',
    'input', 'head'}


def tagfilter(tag, crawler):
    """A default tag filter.

    :param tag: (str) a tag name
    """
    if crawler.isintag('body'):
        return tag not in tag_blacklist
    else:
        return False
