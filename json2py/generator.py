import json

def camel_to_snake(s):
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def generate_python_classes_from_json(json_data, class_name="Root"):
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
                # Handle nested dictionary
                if isinstance(value, dict):
                    nested_class_name = ''.join([x.capitalize() for x in key.split('_')])
                    properties[key] = (nested_class_name, False, False)  # (class name, is list, is simple type)
                    parse_structure(value, nested_class_name, key)
                # Handle list of items
                elif isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        # List of dictionaries
                        nested_class_name = ''.join([x.capitalize() for x in key.split('_')])
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
            snake_prop = camel_to_snake(prop)
            if is_list and not is_simple_type:
                class_code += f"        self.{snake_prop} = [{prop_type}(item) for item in items] if (items := data.get('{prop}')) else []\n"
            elif not is_list and not is_simple_type:
                class_code += f"        self.{snake_prop} = {prop_type}(item) if (item := data.get('{prop}')) else None\n"
            else:
                # Handle simple types (including simple lists) directly without conversion
                default_value = "[]" if is_list else "None"
                class_code += f"        self.{snake_prop} = data.get('{prop}', {default_value})\n"
        class_code += "\n"
        return class_code

    # Generate Python code for all class definitions
    all_classes_code = ""
    for class_name, properties in class_definitions.items():
        all_classes_code += generate_class_code(class_name, properties)

    return imports + all_classes_code

