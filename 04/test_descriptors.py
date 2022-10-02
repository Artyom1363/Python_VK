import unittest
from descriptors import Integer, String, PositiveInteger


# Commands to run test coverage
# coverage run test_descriptors.py
# coverage report -m
# coverage html

class Data:
    num = Integer('num_')
    name = String('name_')
    price = PositiveInteger("price_")

    def __init__(self, num_, name_, price_):
        self.num = num_
        self.name = name_
        self.price = price_


class TestDescriptors(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_validate_input(self):
        with self.assertRaises(ValueError):
            Data("1", "1", 1)

        with self.assertRaises(ValueError):
            Data(-1, 1, 1)

        with self.assertRaises(ValueError):
            Data(-1, "1", -1)

        data = Data(-1, "1", 1)
        self.assertEqual(data.num, -1)
        self.assertEqual(data.name, "1")
        self.assertEqual(data.price, 1)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
