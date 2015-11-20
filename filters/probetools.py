import re


class WhiteListProber(set):
    """Probe documents based on some newline-delineated whitelist.

    This is useful if you only want results from a particular language
    and you have a list of the most common words of that language.
    Less is more; take about 20-or-so words.
    """

    r_tokenizer = re.compile(r'\w+([.,]\w+)*|\S+')

    def __init__(self, wlfile, ntypes, ntokens, mratio):
        """Loads the given white list and creates a probe filter from it.

        :param wlfile: (file) the white list file, a newline-delineated list of types
        :param ntypes: (int) the minimum number of types
        :param nntokens: (int) the minimum number of tokens
        :param mratio: (float) the minimum ratio of types to total tokens
        """
        set.__init__(self, [])
        self.wlfile = wlfile
        self.ntypes = ntypes
        self.ntokens = ntokens
        self.mratio = mratio
        self._parse_list()

    def _parse_list(self):
        """Parse a whitelist file into the set.

        :return: None
        """
        self.update(self.wlfile.readlines())

    def __call__(self, *args, **kwargs):
        """This is defined so that you may

        :param args:
        :param kwargs:
        :return:
        """
        assert len(args) == 1
        tokens = set(WhiteListProber.r_tokenizer.findall(args[0]))
