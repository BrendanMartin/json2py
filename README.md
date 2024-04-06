# JSON2Py Class Generator

`json2py` is a command-line interface (CLI) tool that automatically generates Python class definitions from JSON files. This tool's primary use case is to parse JSON API response bodies into Python classes.

## Features

- Generate Python classes from JSON files with a single command.
- Customize the root class name for the generated Python classes.
- Option to ignore specific keys in the JSON file during class generation.
- Automatically test the generated classes to ensure they can be successfully instantiated with the provided JSON data.

## Installation

You can install the `json2py` tool directly from this GitHub repository:

```bash
git clone https://github.com/yourgithubusername/json2py.git
cd json2py
pip install .
```

## Usage

To use `json2py`, run the following command from the terminal, specifying the input JSON file and optional arguments:

```json2py -i path/to/input.json [-o path/to/output.py] [-r RootClassName] [-ik ignore,keys,list]```

### Arguments

- `-i`, `--input`: (Required) The path to the input JSON file.
- `-o`, `--output`: (Optional) The path to the output Python file. If not specified, the output file name is derived from the input file name.
- `-r`, `--root-class-name`: (Optional) The name of the root class in the generated Python code. Defaults to `Root`.
- `-ik`, `--ignore-keys`: (Optional) A comma-separated list of keys to ignore when generating Python classes.

### Example

Given this JSON response in `example.json`:

```json
{
    "data": {
      "SearchResult": {
        "search": [
          {
            "elements": [
              {
                "__typename": "Search_ProductHit",
                "avgProductRating": 4.844,
                "cobrandingEnabled": false,
                "id": "some_id",
                "complex-field.1": 0
              }
            ],
            "pagination": {
              "cursor": "1",
              "totalElements": 1301
            },
            "totalPages": 84,
            "empty": {}
          }
        ]
      }
    },
    "__N_SSP": false
}
```

Using this command:
```bash
json2py -i example.json -o example.py -r SearchResponse -ik cobrandingEnabled
```

Produces this class structure in `example.py`:

```python
class SearchResponse:
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
```

Now, when you make an API request, you can convert the JSON response body into these classes. For example:
```python
import requests
from example import SearchResponse

r = requests.get('https://example.com/search-endpoint')

search_response = SearchResponse(r.json())

print("First element's rating: ", search_response.data.search_result.search[0].elements[0].avg_product_rating)
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to report bugs or suggest enhancements. 

## License

This project is licensed under [MIT License](LICENSE). See the LICENSE file for more details.
