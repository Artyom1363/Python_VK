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

    def __init__(self, num_=-1, name_="name", price_=1):
        self.num = num_
        self.name = name_
        self.price = price_


class TestDescriptors(unittest.TestCase):

    def test_validate_input(self):
        Data()
        with self.assertRaises(ValueError, ):
            Data(num_="1")

        with self.assertRaises(ValueError):
            Data(name_=1)

        with self.assertRaises(ValueError):
            Data(price_=-1)

        data = Data(-1, "1", 1)
        self.assertEqual(data.num, -1)
        self.assertEqual(data.name, "1")
        self.assertEqual(data.price, 1)

    def test_change_values(self):
        data = Data()
        with self.assertRaises(ValueError):
            data.num = "1"

        with self.assertRaises(ValueError):
            data.name = 1

        with self.assertRaises(ValueError):
            data.name = -1


if __name__ == '__main__':
    unittest.main()
