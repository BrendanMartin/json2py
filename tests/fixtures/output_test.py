class NoneField:
    def __getattribute__(self, item):
        return self

    def __getitem__(self, item):
        return self

    def __eq__(self, other):
        if other is None:
            return True
        return False

class SafeAccess:
    def __getattribute__(self, item):
        print('called get attribute in safe access')
        return NoneField()

class SearchResponse(SafeAccess):
    def __init__(self, data: dict):
        self.data = Data(item) if (item := data.get('data')) else None
        self.n_ssp = data.get('__N_SSP')

class Data:
    def __init__(self, data: dict):
        self.search_result = SearchResult(item) if (item := data.get('SearchResult')) else None

class SearchResult:
    def __init__(self, data: dict):
        self.search = [Search(item) for item in items] if (items := data.get('search')) else []

class Search:
    def __init__(self, data: dict):
        self.elements = [Elements(item) for item in items] if (items := data.get('elements')) else []
        self.pagination = Pagination(item) if (item := data.get('pagination')) else None
        self.total_pages = data.get('totalPages')
        self.empty = data.get('empty')

class Pagination:
    def __init__(self, data: dict):
        self.cursor = data.get('cursor')
        self.total_elements = data.get('totalElements')

class Elements:
    def __init__(self, data: dict):
        self.typename = data.get('__typename')
        self.avg_product_rating = data.get('avgProductRating')
        self.id = data.get('id')
        self.complex_field_1 = data.get('complex-field.1')


if __name__ == '__main__':
    json_data = {
        'data': {
            'SearchResult': {
                'search': [
                    # {
                    #     'elements':   [
                    #         {
                    #             '__typename':        'Search_ProductHit',
                    #             'avgProductRating':  4.844,
                    #             'cobrandingEnabled': False,
                    #             'id':                'some_id',
                    #             'complex-field.1': 0
                    #         }
                    #     ],
                    #     'pagination': {
                    #         'cursor':        '1',
                    #         'totalElements': 1301
                    #     },
                    #     'totalPages': 84,
                    #     'empty': {}
                    # }
                ]
            }
        },
        "__N_SSP": True
    }
    resp = SearchResponse(json_data)
    d = resp.data.search_result.search[0].elements
    print(d)
    if isinstance(d, NoneField):
        print(d.missing)