import json
import string
from typing import List


def make_field_name(key: str):
    field_name = ''
    for i, c in enumerate(key):
        if c.isupper():
            # camel to snake case
            field_name += '_'
            field_name += c.lower()
        elif i == 0 and c.isnumeric():
            field_name += f'n{c}'
        elif c in string.punctuation:
            field_name += '_'
        else:
            field_name += c
    return field_name.lstrip('_')

def make_class_name(key: str):
    class_name = ''
    cap_next = False
    for i, c in enumerate(key):
        if c in string.punctuation:
            cap_next = True
        elif i == 0:
            if c.isnumeric():
                class_name += 'n'
            class_name += c.upper()
        else:
            if cap_next:
                c = c.upper()
                cap_next = False
            class_name += c
    return class_name

def generate_python_classes_from_json(json_data, class_name="Root", ignore_keys=List[str]):
    class_definitions = {}
    imports = ""
    # imports = "import json\n\n"

    def parse_structure(structure, class_name, parent_key=None):
        """
        Recursively parse JSON structure to generate class definitions.
        """
        if isinstance(structure, dict):
            properties = {}
            for key, value in structure.items():
                if key in ignore_keys:
                    continue
                # Handle nested dictionary
                if isinstance(value, dict) and len(value.keys()) > 0:
                    nested_class_name = make_class_name(key)
                    properties[key] = (nested_class_name, False, False)  # (class name, is list, is simple type)
                    parse_structure(value, nested_class_name, key)
                # Handle list of items
                elif isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        # List of dictionaries
                        nested_class_name = make_class_name(key)
                        properties[key] = (nested_class_name, True, False)  # Mark as list of nested class
                        parse_structure(value[0], nested_class_name, key)
                    else:
                        properties[key] = ("list", True, True)  # Mark as simple list
                else:
                    # Simple types (int, str, bool, etc.)
                    properties[key] = (type(value).__name__, False, True)  # Mark as simple type
            class_definitions[class_name] = properties
        elif isinstance(structure, list) and structure and isinstance(structure[0], dict):
            # Handle list of nested objects at root or without a parent key
            if parent_key is None or isinstance(structure[0], dict):
                parse_structure(structure[0], class_name)

    parse_structure(json_data, class_name)


    def generate_class_code(class_name, properties):
        """
        Generate Python class code from properties dictionary, handling simple types, nested objects, and lists appropriately.
        """
        class_code = f"class {class_name}:\n"
        class_code += "    def __init__(self, data: dict):\n"
        for prop, (prop_type, is_list, is_simple_type) in properties.items():
            field_name = make_field_name(prop)
            if is_list and not is_simple_type:
                class_code += f"        self.{field_name} = [{prop_type}(item) for item in items] if (items := data.get('{prop}')) else []\n"
            elif not is_list and not is_simple_type:
                class_code += f"        self.{field_name} = {prop_type}(item) if (item := data.get('{prop}')) else None\n"
            else:
                # Handle simple types (including simple lists) directly without conversion
                if is_list:
                    class_code += f"        self.{field_name} = data.get('{prop}', [])\n"
                else:
                    class_code += f"        self.{field_name} = data.get('{prop}')\n"
        class_code += "\n"
        return class_code

    # Generate Python code for all class definitions
    all_classes_code = ""
    for class_name, properties in class_definitions.items():
        all_classes_code += generate_class_code(class_name, properties)

    return imports + all_classes_code

