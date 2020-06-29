from email import message_from_string

from babel.messages.catalog import Catalog, Message, DEFAULT_HEADER
from babel.util import distinct, odict

from pybabel_utils import PY2, logger, text_type

try:
    import fuzzyset
except ImportError:
    fuzzyset = None


class UpdatableCatalog(Catalog):

    @staticmethod
    def _parse_header(header_string):
        if PY2:
            headers = message_from_string(header_string.encode('utf8'))
            decoded_headers = {}
            for name, value in headers.items():
                name = name.decode('utf8')
                value = value.decode('utf8')
                decoded_headers[name] = value
            return decoded_headers
        else:
            return message_from_string(header_string)

    def __setitem__(self, id, message):
        assert isinstance(message, Message), 'expected a Message object'
        key = self._key_for(id, message.context)
        current = self._messages.get(key)
        if current:
            if message.pluralizable and not current.pluralizable:
                # The new message adds pluralization
                current.id = message.id
            if message.string:
                current.string = message.string
            current.locations = list(distinct(current.locations +
                                              message.locations))
            current.auto_comments = list(distinct(current.auto_comments +
                                                  message.auto_comments))
            current.user_comments = list(distinct(current.user_comments +
                                                  message.user_comments))
            current.flags |= message.flags
        elif id == '':
            # special treatment for the header message
            self.mime_headers = self._parse_header(message.string).items()
            self.header_comment = '\n'.join([('# %s' % c).rstrip() for c
                                             in message.user_comments])
            self.fuzzy = message.fuzzy
        else:
            if isinstance(id, (list, tuple)):
                assert isinstance(message.string, (list, tuple)), \
                    'Expected sequence but got %s' % type(message.string)
            self._messages[key] = message


if fuzzyset:
    class FuzzySetEx(fuzzyset.FuzzySet):

        def has_value(self, value, score_threshold):
            try:
                v = self.get(value)
                res = v is not None and v[0][0] > score_threshold
                if res:
                    logger.debug('Value in set > {}, provided value > {}'.format(v, value))
                return res
            except ZeroDivisionError:
                # set is empty
                return False

        def get_text(self, key):
            return self.get(key)[0][-1]

else:
    class FuzzySetEx(object):
        pass


class UniqueMessagesCatalog(Catalog):

    def __init__(self, locale=None, domain=None, header_comment=DEFAULT_HEADER, project=None, version=None,
                 copyright_holder=None, msgid_bugs_address=None, creation_date=None, revision_date=None,
                 last_translator=None, language_team=None, charset=None, fuzzy=True, name=None,
                 clean_msg_funcs=None, fuzzy_score_threshold=0.9):
        if fuzzyset is None:
            raise ImportError('Please install "fuzzyset" to use "UniqueMessagesCatalog" class')

        super(UniqueMessagesCatalog, self).__init__(locale=locale, domain=domain, header_comment=header_comment,
                                                    project=project, version=version, copyright_holder=copyright_holder,
                                                    msgid_bugs_address=msgid_bugs_address, creation_date=creation_date,
                                                    revision_date=revision_date, last_translator=last_translator,
                                                    language_team=language_team, charset=charset, fuzzy=fuzzy)
        self._messages_strings = FuzzySetEx()
        self._repeatable_messages = odict()
        self._clean_msg_funcs = clean_msg_funcs
        self._fuzzy_score_threshold = fuzzy_score_threshold
        self.name = name

    def clean_string(self, msg_string):
        if self._clean_msg_funcs:
            for func in self._clean_msg_funcs:
                try:
                    msg_string = func(msg_string)
                except Exception as e:
                    logger.debug('message string cleaning error > {!r}'.format(e), exc_info=True)
        return msg_string

    def __setitem__(self, id, message):
        message.string = self.clean_string(message.string)
        if not self._messages_strings.has_value(message.string, self._fuzzy_score_threshold):
            self._messages_strings.add(message.string)
            super(UniqueMessagesCatalog, self).__setitem__(id, message)
        else:
            logger.debug('Message is not unique > {}'.format(text_type(message.string)))
            self._repeatable_messages[id] = message.string

    def rollback_obsolete(self):
        self._messages.update(self.obsolete)
        self.obsolete = odict()

    def get_repeatable_messages_catalog(self):
        ctl = Catalog()
        for k, v in self._repeatable_messages.items():
            ctl.add(id=k, string=v)
        return ctl
