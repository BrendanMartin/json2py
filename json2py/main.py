import argparse
import json
import sys

from json2py.generator import generate_python_classes_from_json


def main():
    parser = argparse.ArgumentParser(description='Generate Python classes from JSON.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output Python file')
    parser.add_argument('-r', '--root-class-name', default='Root', help='Root class name')
    parser.add_argument('-ik', '--ignore-keys', help='Ignore creating fields or classes matching a list of comma-separated keys')

    args = parser.parse_args()

    # Process the JSON input file and generate classes
    with open(args.input, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    ignore_keys = ik.split(',') if (ik := args.ignore_keys) else []

    class_definitions = generate_python_classes_from_json(json_data, args.root_class_name, ignore_keys)

    command = f"\"\"\"\nGenerated with:\njson2py {' '.join(sys.argv[1:])}\n\"\"\"\n\n"

    class_definitions = command + class_definitions

    # Write the generated classes to the output file
    with open(args.output, 'w') as output_file:
        output_file.write(class_definitions)

if __name__ == '__main__':
    main()
