import json
from pathlib import Path

def get_fixture(name):
    parent = Path(__file__).parent
    with open(parent / 'fixtures' / name, 'r', encoding='utf8') as f:
        return json.load(f)
