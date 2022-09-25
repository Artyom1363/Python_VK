import unittest
from custom_list import CustomList

class TestCustomList(unittest.TestCase):
    """

    """
    def setUp(self):
        self.array = CustomList([1, 2, 3])

    def test_adding_list(self):
        self.assertEqual(self.array + [1, 2], CustomList([2, 4, 3]))
        self.assertEqual([1, 2] + self.array, CustomList([2, 4, 3]))
        self.assertEqual(self.array + [1, 2, 3, 4], CustomList([2, 4, 6, 4]))
        self.assertEqual([1, 2, 3, 4] + self.array, CustomList([2, 4, 6, 4]))
        self.assertEqual(self.array + [], self.array)
        self.assertEqual([] + self.array, self.array)
    
    def test_subtraction(self):
        self.assertEqual(self.array - [1, 2], CustomList([0, 0, 3]))
        self.assertEqual([1, 2] - self.array, CustomList([0, 0, 3]))
        self.assertEqual(self.array - [1, 2, 3, 4], CustomList([0, 0, 0, -4]))
        self.assertEqual([1, 2, 3, 4] - self.array, CustomList([0, 0, 0, 4]))
        self.assertEqual(self.array - [], self.array)
        self.assertEqual([] - self.array, CustomList([1, 2, 3]))
    
    def test_equal(self):
        self.assertTrue(self.array == [3, 2, 1])
        self.assertTrue(self.array == [6])
        self.assertEqual(self.array, [3, 2, 1])
    
    def test_to_str(self):
        self.assertEqual(str(self.array), "[1, 2, 3] sum: 6")


if __name__ == "__main__":
    unittest.main()