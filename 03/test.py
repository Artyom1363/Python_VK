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

        for arr_elem, custom_elem in zip(self.array, CustomList([1, 2, 3])):
            self.assertEqual(arr_elem, custom_elem)

        self.assertEqual(len(array2), 2)
        for arr_elem, custom_elem in zip(array2, CustomList([1, 2])):
            self.assertEqual(arr_elem, custom_elem)

        self.assertEqual([1, 2] + self.array, CustomList([2, 4, 3]))

        test_list = [1, 2, 3, 4]
        list_addition = self.array + test_list
        self.assertEqual(list_addition, CustomList([16]))
        for list_elem, custom_elem in zip(list_addition,
                                          CustomList([2, 4, 6, 4])):
            self.assertEqual(list_elem, custom_elem)

        list_addition = test_list + self.array
        self.assertEqual(list_addition, CustomList([16]))
        for list_elem, custom_elem in zip(list_addition,
                                          CustomList([2, 4, 6, 4])):
            self.assertEqual(list_elem, custom_elem)

        self.assertEqual(self.array + [], self.array)
        self.assertEqual([] + self.array, self.array)

    def test_subtraction(self):
        array2 = CustomList([1, 2])
        self.assertEqual(self.array - array2, CustomList([0, 0, 3]))
        self.assertEqual(len(self.array), 3)

        for arr_elem, custom_elem in zip(self.array, CustomList([1, 2, 3])):
            self.assertEqual(arr_elem, custom_elem)

        self.assertEqual(len(array2), 2)
        for arr_elem, custom_elem in zip(array2, CustomList([1, 2])):
            self.assertEqual(arr_elem, custom_elem)

        self.assertEqual([1, 2] - self.array, CustomList([0, 0, -3]))

        test_list = [1, 2, 3, 4]
        list_subtraction = self.array - test_list
        self.assertEqual(list_subtraction, CustomList([-4]))
        for list_elem, custom_elem in zip(list_subtraction,
                                          CustomList([0, 0, 0, -4])):
            self.assertEqual(list_elem, custom_elem)

        list_subtraction = test_list - self.array
        self.assertEqual(list_subtraction, CustomList([4]))
        for list_elem, custom_elem in zip(list_subtraction,
                                          CustomList([0, 0, 0, 4])):
            self.assertEqual(list_elem, custom_elem)

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
