import unittest

from json2py.generator import generate_python_classes_from_json


class GeneratorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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
                                }
                            ],
                            'pagination': {
                                'cursor':        '1',
                                'totalElements': 1301
                            },
                            'totalPages': 84
                        }
                    ]
                }
            }
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







if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(MyTestCase('test_something'))