from email import message_from_string

from babel.messages import Catalog, Message
from babel.util import distinct

from pybabel_utils import PY2


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
