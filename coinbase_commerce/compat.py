import six

if six.PY2:
    from itertools import imap  # noqa
    from urllib import quote  # noqa
    from urlparse import urljoin  # noqa
    from urlparse import urlparse  # noqa
elif six.PY3:
    from urllib.parse import quote  # noqa
    from urllib.parse import urljoin  # noqa
    from urllib.parse import urlparse  # noqa


def py2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.
    """
    if six.PY2:
        if '__str__' not in klass.__dict__:
            raise ValueError("@python_2_unicode_compatible cannot be applied "
                             "to %s because it doesn't define __str__()." %
                             klass.__name__)
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass
