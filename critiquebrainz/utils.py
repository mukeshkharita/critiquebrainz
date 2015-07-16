from flask_uuid import UUID_RE
from flask_babel import format_datetime, format_date
import difflib
import urllib
import urlparse
import string
import random

tags = {'+': ('<ins>', '</ins>'), '-': ('<del>', '</del>'), ' ': (' ', '')}


def build_url(base, additional_params=None):
    url = urlparse.urlparse(base)
    query_params = {}
    query_params.update(urlparse.parse_qsl(url.query, True))
    if additional_params is not None:
        query_params.update(additional_params)
        for key, val in additional_params.iteritems():
            if val is None:
                query_params.pop(key)

    return urlparse.urlunparse(
        (url.scheme, url.netloc, url.path, url.params,
         urllib.urlencode(query_params), url.fragment))


def validate_uuid(string):
    """Validates UUID. Returns True if valid, False otherwise."""
    return True if UUID_RE.match(string) else False


def generate_string(length):
    """Generates random string with a specified length."""
    return ''.join([random.choice(string.ascii_letters.decode('ascii')
                                  + string.digits.decode('ascii'))
                    for _ in xrange(length)])


def reformat_date(value, format=None):
    """Converts date into string formatted for current locale."""
    return format_date(value, format)


def reformat_datetime(value, format=None):
    """Converts datetime into string formatted for current locale."""
    return format_datetime(value.replace(tzinfo=None), format)


def track_length(value):
    """Converts track length specified in milliseconds into a pretty string."""
    seconds = int(value) / 1000
    minutes, seconds = divmod(seconds, 60)
    return '%i:%02i' % (minutes, seconds)


def side_by_side_diff(old, new):
    left, right = [], []

    # Deletions on the left, insertions on the right.
    def append(tag, text):
        if tag == '<ins>':
            right.append(text)
        elif tag == '<del>':
            left.append(text)
        else:
            left.append(text)
            right.append(text)

    # Generates a compact word diff
    prev_start, prev_end = None, ''
    prev_item = ''

    for item in difflib.ndiff(old.split(), new.split()):
        tag = tags.get(item[0])

        if not tag:
            continue

        if prev_start == tag[0]:
            prev_item += item[1:]
        else:
            append(prev_start, prev_item + prev_end)
            prev_start, prev_end = tag
            prev_item = prev_start + item[1:]

    append(prev_start, prev_item + prev_end)

    return " ".join(left), " ".join(right)
