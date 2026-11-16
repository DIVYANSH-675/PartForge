import json
import tempfile
import unittest
from pathlib import Path
from partforge import inspect_file, inspect_vector


def row(command):
    return [command] + [-1] * 16


class VectorTests(unittest.TestCase):
    def test_normal_export(self):
        result = inspect_vector([row(4), row(0), row(5), row(3), row(3)])
        self.assertTrue(result["valid"])
        self.assertEqual(result["commands"]["Ext"], 1)

    def test_command_after_end(self):
        self.assertFalse(inspect_vector([row(4), row(3), row(5)])["valid"])

    def test_bad_values(self):
        for data in ([], [[0]], [row(float("nan"))], [row(7)], [row(.5)]):
            with self.subTest(data=data):
                self.assertFalse(inspect_vector(data)["valid"])

    def test_missing_or_corrupt_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            self.assertFalse(inspect_file(path)["valid"])
            path.write_text("not json")
            self.assertFalse(inspect_file(path)["valid"])
            path.write_text(json.dumps({"vec": [row(4), row(0), row(5)]}))
            self.assertTrue(inspect_file(path)["valid"])
