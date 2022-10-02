import unittest
from meta_classes import CustomMeta


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class TestMetaClass(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_existing_custom_values(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(CustomClass.custom_x, 50)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")

    def test_absence(self):
        inst = CustomClass()
        with self.assertRaises(AttributeError):
            inst.x
        with self.assertRaises(AttributeError):
            inst.val
        with self.assertRaises(AttributeError):
            inst.line()
        with self.assertRaises(AttributeError):
            inst.yyy
        with self.assertRaises(AttributeError):
            CustomClass.x


if __name__ == '__main__':
    unittest.main()
