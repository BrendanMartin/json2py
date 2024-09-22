import json
from pathlib import Path

import pytest

from json2py.generator import generate_python_classes_from_json, make_class_name, make_field_name

fixtures = Path(__file__).parent / 'fixtures'
json_data = {
    'data':    {
        'SearchResult': {
            'search': [
                {
                    'elements':   [
                        {
                            '__typename':        'Search_ProductHit',
                            'avgProductRating':  4.844,
                            'cobrandingEnabled': False,
                            'id':                'some_id',
                            'complex-field.1':   0
                        }
                    ],
                    'pagination': {
                        'cursor':        '1',
                        'totalElements': 1301
                    },
                    'totalPages': 84,
                    'empty':      {}
                },
            ],
            "shared/quotes": {
                "damianOFarrill": {
                    "position": "Director of Data Science and Revenue"
                }
            }
        }
    },
    "__N_SSP": True
}


def test_generator():
    python_code = generate_python_classes_from_json(json_data, class_name='SearchResponse',
                                                    ignore_keys=['cobrandingEnabled'])
    local_env = {}
    exec(python_code, local_env, local_env)  # https://stackoverflow.com/a/29979633/3711940

    Root = local_env['SearchResponse']
    root = Root(json_data)

    print(python_code)

    assert root.data.search_result is not None


def test_generated_classes():
    from generated import Root
    root = Root(json_data)
    assert root.data is not None


def test_ignore_keys():
    python_code = generate_python_classes_from_json(json_data, ignore_keys=['elements', 'totalPages', 'shared/quotes'])
    local_env = {}
    exec(python_code, local_env, local_env)

    Root = local_env['Root']
    root = Root(json_data)

    search = root.data.search_result.search

    with pytest.raises(AttributeError):
        _ = search.elements

    with pytest.raises(AttributeError):
        _ = search.total_pages

    with pytest.raises(AttributeError):
        _ = search.shared_quotes


def test_empty_skip_empty_object():
    python_code = generate_python_classes_from_json(json_data)
    local_env = {}
    exec(python_code, local_env, local_env)

    Root = local_env['Root']
    root = Root(json_data)

    search = root.data.search_result.search

    with pytest.raises(AttributeError):
        empty = search.empty


def test_make_class_name():
    tests = [
        ('lowerUpper', 'LowerUpper'),
        ('underscored_name', 'UnderscoredName'),
        ('complex-name_with.punc', 'ComplexNameWithPunc'),
        ('cats', 'Cat'),  # test de-pluralization
        ('physics', 'Physics'),
        ('4728347', 'N4728347')
    ]

    for t in tests:
        res = make_class_name(t[0])
        assert t[1] == res


def test_make_field_name():
    tests = [
        ('FooBar', 'foo_bar'),
        ('_foo_bar', 'foo_bar'),
        ('foo_bar__', 'foo_bar'),
        ('__N_SSG', 'n_ssg'),
        ('__N_SSP', 'n_ssp'),
        ('--82661', 'n82661'),
        ('someID', 'some_id')
    ]
    for t in tests:
        res = make_field_name(t[0])
        assert t[1] == res


def test_root_is_list():
    with open(fixtures / 'list_example.json', 'r') as f:
        j = json.load(f)
    python_code = generate_python_classes_from_json(j)


def test_array_handled():
    with open(fixtures / 'array_example.json', 'r') as f:
        j = json.load(f)
    python_code = generate_python_classes_from_json(j)


def test_nested_same_name():
    with open(fixtures / 'nested_same_name.json') as f:
        j = json.load(f)
    python_code = generate_python_classes_from_json(j)
    print(python_code)
