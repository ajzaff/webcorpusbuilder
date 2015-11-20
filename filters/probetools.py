import re


class ListProber(set):
    """Probe documents based on some newline-delineated white/black list.

    This is useful if you only want results from a particular language
    and you have a list of the most common words of that language.
    Less is more; take about 20-or-so words.

    Black list feature might be used for undesired items such as
    spam terms.
    """

    r_tokenizer = re.compile(r'\w+')

    def __init__(self, lfile, types, tokens, ratio, accept_behavior=True):
        """Loads the given white list and creates a probe filter from it.

        :param lfile: (file) the white list file, a newline-delineated list of types
        :param types: (int) the minimum number of types
        :param tokens: (int) the minimum number of tokens
        :param ratio: (float) the minimum ratio of types to total tokens
        :param accept_behavior: (bool) whether to return    ``True'' or ``False'' on match
        """
        set.__init__(self, [])
        self.accept_behavior = accept_behavior
        self.lfile = lfile
        self.types = types
        self.tokens = tokens
        self.ratio = ratio
        self._parse_list()

    def _parse_list(self):
        """Parse a list file into the set.

        :return: None
        """
        self.update(self.lfile.readlines())

    def probe(self, document):
        """Accept or reject a document based on the probe filter.

        :param document: (str) a raw document possibly containing HTML.
        :return: ``True'', ``False'' depends on ``accept_behavior''.
        """
        tokens = ListProber.r_tokenizer.findall(document)
        matched_types = 0
        matched_tokens = 0
        num_tokens = len(tokens)
        if num_tokens == 0:
            return False # reject in every case
        for tok in tokens:
            if tok in self:
                matched_types += 1
                matched_tokens += 1
        if matched_tokens >= self.tokens and\
            matched_types >= self.types and\
            matched_tokens / num_tokens >= self.ratio:
            return self.accept_behavior
        else
            return not self.accept_behavior


    def __call__(self, *args, **kwargs):
        """Accept or reject a document based on the probe filter / ``accept_behavior''

        This is defined so that you may call this set
        directly on the contents of a document and accept or reject it.

        :param args:
        :param kwargs:
        :return:
        """
        assert len(args) == 1
        return self.probe(args[0])

