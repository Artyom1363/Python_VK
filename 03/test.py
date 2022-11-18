import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    """

    """
    def setUp(self):
        self.array = CustomList([1, 2, 3])

    def test_adding_list(self):
        array2 = CustomList([1, 2])
        self.assertEqual(self.array + array2, CustomList([2, 4, 3]))
        self.assertEqual(len(self.array), 3)

        for a, b in zip(self.array, CustomList([1, 2, 3])):
            self.assertEqual(a, b)

        self.assertEqual(len(array2), 2)
        for a, b in zip(array2, CustomList([1, 2])):
            self.assertEqual(a, b)

        self.assertEqual([1, 2] + self.array, CustomList([2, 4, 3]))
        self.assertEqual(self.array + [1, 2, 3, 4], CustomList([2, 4, 6, 4]))
        self.assertEqual([1, 2, 3, 4] + self.array, CustomList([2, 4, 6, 4]))
        self.assertEqual(self.array + [], self.array)
        self.assertEqual([] + self.array, self.array)

    def test_subtraction(self):
        array2 = CustomList([1, 2])
        self.assertEqual(self.array - array2, CustomList([0, 0, 3]))
        self.assertEqual(len(self.array), 3)

        for a, b in zip(self.array, CustomList([1, 2, 3])):
            self.assertEqual(a, b)

        self.assertEqual(len(array2), 2)
        for a, b in zip(array2, CustomList([1, 2])):
            self.assertEqual(a, b)

        self.assertEqual([1, 2] - self.array, CustomList([0, 0, -3]))
        self.assertEqual(self.array - [1, 2, 3, 4], CustomList([0, 0, 0, -4]))
        self.assertEqual([1, 2, 3, 4] - self.array, CustomList([0, 0, 0, 4]))
        self.assertEqual(self.array - [], self.array)
        self.assertEqual([] - self.array, CustomList([-1, -2, -3]))

    def test_comparison_operators(self):
        self.assertGreater(self.array, [1, 1, 1])
        self.assertGreaterEqual(self.array, [3, 2, 1])
        self.assertGreaterEqual(self.array, [2, 2, 1])
        self.assertEqual(self.array, [3, 2, 1])
        self.assertEqual(self.array, [6])
        self.assertEqual([3, 2, 1], self.array)
        self.assertLessEqual(self.array, [1, 2, 3])
        self.assertLessEqual(self.array, [1, 2, 4])
        self.assertLess(self.array, [1, 2, 4])
        self.assertLess([1, 2, 2], self.array)

    def test_to_str(self):
        self.assertEqual(str(self.array), "[1, 2, 3] sum: 6")


if __name__ == "__main__":
    unittest.main()
