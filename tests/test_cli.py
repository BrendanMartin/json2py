import os
import subprocess
import unittest
from pathlib import Path


class CLITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        parent = Path(__file__).parent
        cls.input_file = (parent/'test.json').as_posix()
        cls.output_file = (parent/'output.py').as_posix()

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_main(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        result = subprocess.run(['json2py', '--input', self.input_file, '--output', self.output_file], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0, f"CLI tool did not exit successfully. Error: {result.stderr}")

        self.assertTrue(os.path.exists(self.output_file), "Output file was not created.")

        with open(self.output_file, 'r') as file:
            output_contents = file.read()
            self.assertIn("class Root", output_contents)


if __name__ == '__main__':
    unittest.main()
