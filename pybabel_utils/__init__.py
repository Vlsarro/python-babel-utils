import sys
import logging


__all__ = ('PY2', 'text_type', 'logger')


PY2 = sys.version_info[0] == 2

if not PY2:
    text_type = str
else:
    text_type = unicode

logger = logging.getLogger('pybabel_utils')
