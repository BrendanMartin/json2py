import argparse
import json

from json2py.generator import generate_python_classes_from_json


def main():
    parser = argparse.ArgumentParser(description='Generate Python classes from JSON.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output Python file')
    parser.add_argument('-r', '--root-class-name', default='Root', help='Root class name')

    args = parser.parse_args()

    # Process the JSON input file and generate classes
    with open(args.input, 'r') as json_file:
        json_data = json.load(json_file)

    class_definitions = generate_python_classes_from_json(json_data, args.root_class_name)

    # Write the generated classes to the output file
    with open(args.output, 'w') as output_file:
        output_file.write(class_definitions)

if __name__ == '__main__':
    main()
