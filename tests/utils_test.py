import unittest

from parameterized import param, parameterized

from hyperleda import utils


class DictCleaningTest(unittest.TestCase):
    @parameterized.expand(
        [
            param(
                "no cleaning",
                {"a": 1, "b": 2},
                {"a": 1, "b": 2},
            ),
            param(
                "first level",
                {"a": 1, "b": None},
                {"a": 1},
            ),
            param(
                "third level",
                {"a": 1, "b": {"c": {"d": None}}},
                {"a": 1},
            ),
            param(
                "list",
                [{"a": 1, "b": None}, {"a": 2, "b": 3}],
                [{"a": 1}, {"a": 2, "b": 3}],
            ),
            param(
                "list in dict",
                {"a": 1, "b": {"c": [{"d": None}, {"e": 2}]}},
                {"a": 1, "b": {"c": [{}, {"e": 2}]}},
            ),
            param(
                "list in list",
                [[{"c": 2}], [{"a": 1, "b": None}]],
                [[{"c": 2}], [{"a": 1}]],
            ),
            param(
                "list of primitives",
                [1, None, 3],
                [1, None, 3],
            ),
        ]
    )
    def test_table(self, name, data, expected):
        self.assertEqual(utils.clean_dict(data), expected)
