class Elements:
    def __init__(self, data: dict):
        self.typename = data.get('__typename', None)
        self.avg_product_rating = data.get('avgProductRating', None)
        self.cobranding_enabled = data.get('cobrandingEnabled', None)
        self.id = data.get('id', None)

class Pagination:
    def __init__(self, data: dict):
        self.cursor = data.get('cursor', None)
        self.total_elements = data.get('totalElements', None)

class Search:
    def __init__(self, data: dict):
        self.elements = [Elements(item) for item in items] if (items := data.get('elements')) else []
        self.pagination = Pagination(item) if (item := data.get('pagination')) else None
        self.total_pages = data.get('totalPages', None)

class Searchresult:
    def __init__(self, data: dict):
        self.search = [Search(item) for item in items] if (items := data.get('search')) else []

class Data:
    def __init__(self, data: dict):
        self.search_result = Searchresult(item) if (item := data.get('SearchResult')) else None

class Root:
    def __init__(self, data: dict):
        self.data = Data(item) if (item := data.get('data')) else None
