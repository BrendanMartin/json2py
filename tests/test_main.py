from pprint import pprint

import pytest

from json2py.main import object_hash
from tests import get_fixture


def test_hash_object():
    d = get_fixture('next_data_old.json')
    h = object_hash(d)
    pprint(h)