import json
import string
from collections import OrderedDict
from dataclasses import dataclass
from typing import List, Dict
import typing
from nltk.corpus import wordnet as wn

reserved_words = ['class']


def make_field_name(key: str):
    field_name = ''
    for i, c in enumerate(key):
        if c.isupper():
            # camel to snake case
            field_name += '_'
            field_name += c.lower()
        elif i == 0 and c.isnumeric():
            field_name += f'n{c}'
        elif c in string.punctuation or c.isspace():
            field_name += '_'
        else:
            field_name += c
    field_name = field_name.lstrip('_')
    if field_name in reserved_words:
        field_name = field_name + '_'
    return field_name


def make_class_name(key: str):
    if (k := wn.morphy(key.lower())):
        key = k
    class_name = ''
    cap_next = False
    for i, c in enumerate(key):
        if c in string.punctuation:
            cap_next = True
        elif c.isspace():
            c += '_'
        elif i == 0:
            if c.isnumeric():
                class_name += 'n'
            class_name += c.upper()
        else:
            if cap_next:
                c = c.upper()
                cap_next = False
            class_name += c
    if class_name in reserved_words:
        class_name = class_name + '_'
    return class_name


@dataclass(frozen=True)
class Key:
    name: str
    is_root: bool = False
    data_is_list: bool = False


@dataclass
class Element:
    prop_type: str
    is_list: bool
    is_simple_type: bool


@dataclass
class Property:
    key: str
    element: Element


def generate_python_classes_from_json(json_data, class_name="Root", ignore_keys=List[str]):
    class_definitions: typing.OrderedDict[Key, List[Property]] = OrderedDict()
    imports = ""

    # TODO: check if key in properties or class_definitions already. If so, update name to be <parent><name>
    def parse_structure(structure, class_name, parent_key=None):
        """
        Recursively parse JSON structure to generate class definitions.
        """
        if isinstance(structure, dict):
            # properties = Dict[str, Element]
            properties: List[Property] = []
            for key, value in structure.items():
                if key in ignore_keys:
                    continue
                # Handle nested dictionary
                if isinstance(value, dict) and len(value.keys()) > 0:
                    nested_class_name = make_class_name(key)
                    # properties[key] = Element(nested_class_name, False,
                    #                              False)  # (class name, is list, is simple type)
                    properties.append(Property(
                            key,
                            Element(nested_class_name, False, False)  # (class name, is list, is simple type)
                    ))
                    parse_structure(value, nested_class_name, key)
                # Handle list of items
                elif isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        # List of dictionaries
                        nested_class_name = make_class_name(key)
                        # properties[key] = Element(nested_class_name, True, False)  # Mark as list of nested class
                        properties.append(Property(
                                key,
                                Element(nested_class_name, True, False)  # Mark as list of nested class
                        ))
                        parse_structure(value[0], nested_class_name, key)
                    else:
                        # properties[key] = Element("list", True, True)  # Mark as simple list
                        properties.append(Property(
                                key,
                                Element("list", True, True)  # Mark as simple list
                        ))
                else:
                    # Simple types (int, str, bool, etc.)
                    # properties[key] = Element(type(value).__name__, False, True)  # Mark as simple type
                    properties.append(Property(
                            key,
                            Element(type(value).__name__, False, True)  # Mark as simple type
                    ))
            class_definitions[Key(class_name)] = properties
        elif isinstance(structure, list) and structure and isinstance(structure[0], dict):
            # Handle list of nested objects at root or without a parent key
            if parent_key is None:
                class_definitions[Key(class_name, True, True)] = [Property('elements', Element('Element', True, False))]
                parse_structure(structure[0], 'Element', class_name)
            elif isinstance(structure[0], dict):
                parse_structure(structure[0], class_name)

    # if isinstance(json_data, list):
    #     json_data = {class_name + 'Item': json_data}
    #     parse_structure(json_data, class_name)
    # else:
    parse_structure(json_data, class_name)

    def generate_class_code(key: Key, properties: List[Property]):
        """
        Generate Python class code from properties dictionary, handling simple types, nested objects, and lists appropriately.
        """
        class_code = f"class {key.name}:\n"
        if key.is_root and key.data_is_list:
            class_code += "    def __init__(self, data: list):\n"
        else:
            class_code += "    def __init__(self, data: dict):\n"

        for prop in properties:
            field_name = make_field_name(prop.key)
            if prop.element.is_list and not prop.element.is_simple_type:
                if key.data_is_list:
                    class_code += f"        self.{field_name} = [{prop.element.prop_type}(item) for item in data]\n"
                else:
                    class_code += f"        self.{field_name} = [{prop.element.prop_type}(item) for item in items] if (items := data.get('{prop.key}')) else []\n"
            elif not prop.element.is_list and not prop.element.is_simple_type:
                class_code += f"        self.{field_name} = {prop.element.prop_type}(item) if (item := data.get('{prop.key}')) else None\n"
            else:
                # Handle simple types (including simple lists) directly without conversion
                if prop.element.is_list:
                    class_code += f"        self.{field_name} = data.get('{prop.key}', [])\n"
                else:
                    class_code += f"        self.{field_name} = data.get('{prop.key}')\n"
        class_code += "\n"
        return class_code

    # Generate Python code for all class definitions
    # all_classes_code = ""
    # for class_name, properties in reversed(class_definitions.items()):
    #     all_classes_code += generate_class_code(class_name, properties)

    all_classes_code = ""
    for key, properties in reversed(class_definitions.items()):
        all_classes_code += generate_class_code(key, properties)
    return imports + all_classes_code
