import json
import unittest
from pathlib import Path

from json2py.generator import generate_python_classes_from_json, make_class_name, make_field_name


class GeneratorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = Path(__file__).parent / 'fixtures'
        cls.json_data = {
            'data': {
                'SearchResult': {
                    'search': [
                        {
                            'elements':   [
                                {
                                    '__typename':        'Search_ProductHit',
                                    'avgProductRating':  4.844,
                                    'cobrandingEnabled': False,
                                    'id':                'some_id',
                                    'complex-field.1': 0
                                }
                            ],
                            'pagination': {
                                'cursor':        '1',
                                'totalElements': 1301
                            },
                            'totalPages': 84,
                            'empty': {}
                        }
                    ]
                }
            },
            "__N_SSP": True
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generator(self):
        python_code = generate_python_classes_from_json(self.json_data)
        local_env = {}
        exec(python_code, local_env, local_env) # https://stackoverflow.com/a/29979633/3711940

        Root = local_env['Root']
        root = Root(self.json_data)

        self.assertIsNotNone(root.data.search_result)

    def test_generated_classes(self):
        from generated import Root
        root = Root(self.json_data)
        self.assertIsNotNone(root.data)

    def test_ignore_keys(self):
        python_code = generate_python_classes_from_json(self.json_data, ignore_keys=['elements','totalPages'])
        local_env = {}
        exec(python_code, local_env, local_env)

        Root = local_env['Root']
        root = Root(self.json_data)

        search = root.data.search_result.search

        with self.assertRaises(AttributeError):
            elements = search.elements

        with self.assertRaises(AttributeError):
            total_pages = search.total_pages

    def test_empty_skip_empty_object(self):
        python_code = generate_python_classes_from_json(self.json_data)
        local_env = {}
        exec(python_code, local_env, local_env)

        Root = local_env['Root']
        root = Root(self.json_data)

        search = root.data.search_result.search

        with self.assertRaises(AttributeError):
            empty = search.empty

    def test_make_class_name(self):
        tests = [
            ('lowerUpper', 'LowerUpper'),
            ('underscored_name', 'UnderscoredName'),
            ('complex-name_with.punc', 'ComplexNameWithPunc'),
            ('cats', 'Cat'), # test de-pluralization
            ('physics', 'Physics')
        ]

        for t in tests:
            res = make_class_name(t[0])
            self.assertEqual(t[1], res)

    def test_make_field_name(self):
        tests = [
            ('FooBar', 'foo_bar'),
            ('_foo_bar', 'foo_bar'),
            ('foo_bar__', 'foo_bar'),
            ('__N_SSG', 'n_ssg'),
            ('__N_SSP', 'n_ssp')
        ]
        for t in tests:
            res = make_field_name(t[0])
            self.assertEqual(t[1], res)

    def test_root_is_list(self):
        with open(self.fixtures/'list_example.json', 'r') as f:
            j = json.load(f)

        python_code = generate_python_classes_from_json(j)


if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(MyTestCase('test_something'))
