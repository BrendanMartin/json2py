import argparse
import json
import subprocess
import sys
from pathlib import Path

from json2py.generator import generate_python_classes_from_json

def successfully_generated(input_file_name, output_file_name, root_class_name):
    module_name = Path(output_file_name).stem
    command = (
        'python -c '
        '"import json; '
        f'from {module_name} import {root_class_name}; '
        f'f = open(\'{input_file_name}\', \'r\', encoding=\'utf-8\'); '
        f'data = json.load(f); '
        'f.close(); '
        f'instance = {root_class_name}(data); "'
    )
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print('Error when testing generated class:\n', result.stderr)
        return False
    else:
        print('Successfully generated classes.\n', result.stderr)
        return True


def main():
    parser = argparse.ArgumentParser(description='Generate Python classes from JSON.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file')
    parser.add_argument('-o', '--output', help='Output Python file')
    parser.add_argument('-r', '--root-class-name', default='Root', help='Root class name')
    parser.add_argument('-ik', '--ignore-keys', help='Ignore creating fields or classes matching a list of comma-separated keys')

    args = parser.parse_args()

    input_file_name = args.input
    if args.output:
        output_file_name = args.output
    else:
        output_file_name = Path(input_file_name).stem + '.py'
    root_class_name = args.root_class_name

    # Process the JSON input file and generate classes
    with open(input_file_name, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    ignore_keys = ik.split(',') if (ik := args.ignore_keys) else []

    class_definitions = generate_python_classes_from_json(json_data, root_class_name, ignore_keys)

    command = f"\"\"\"\nGenerated with:\njson2py {' '.join(sys.argv[1:])}\n\"\"\"\n\n"

    class_definitions = command + class_definitions

    # Write the generated classes to the output file
    with open(output_file_name, 'w') as output_file:
        output_file.write(class_definitions)

    if not successfully_generated(input_file_name, output_file_name, root_class_name):
        return

if __name__ == '__main__':
    main()
