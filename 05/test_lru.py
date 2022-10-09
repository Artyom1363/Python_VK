import unittest
from lru_cache import CustomList, LRUCache


class TestLRUCache(unittest.TestCase):
    def test_custom_list(self):
        custom_list = CustomList()
        one = custom_list.push_front(1)
        self.assertEqual(custom_list.list_start, custom_list.list_end)
        self.assertEqual(custom_list.size, 1)
        self.assertIsNone(custom_list.list_start.nref)
        self.assertIsNone(custom_list.list_start.pref)

        custom_list.move_up(one)
        self.assertEqual(custom_list.list_start, custom_list.list_end)
        self.assertEqual(custom_list.size, 1)
        self.assertIsNone(custom_list.list_start.nref)
        self.assertIsNone(custom_list.list_start.pref)

        custom_list.push_front(2)
        custom_list.push_front(3)
        self.assertEqual(custom_list.size, 3)
        self.assertNotEqual(custom_list.list_start, custom_list.list_end)
        self.assertEqual(custom_list.list_start.value, 3)
        self.assertEqual(custom_list.list_start.nref.value, 2)
        self.assertEqual(custom_list.list_end.value, 1)
        self.assertEqual(custom_list.list_start.nref.nref,
                         custom_list.list_end)

        custom_list.move_up(one)
        self.assertEqual(custom_list.list_start.value, 1)
        self.assertEqual(custom_list.list_start.nref.value, 3)
        self.assertEqual(custom_list.list_end.value, 2)
        self.assertEqual(custom_list.list_start.nref.nref,
                         custom_list.list_end)

        deleted = custom_list.pop_back()
        self.assertEqual(deleted.value, 2)
        self.assertEqual(custom_list.list_start.value, 1)
        self.assertEqual(custom_list.list_start.nref.value, 3)
        self.assertEqual(custom_list.list_start.nref, custom_list.list_end)

    def test_lru_cache(self):
        with self.assertRaises(Exception):
            LRUCache(max_size=0)

        lru = LRUCache(max_size=2)
        lru["1"] = 1
        lru["2"] = 2
        lru["3"] = 3
        self.assertEqual(lru.size, 2)
        self.assertEqual(lru.dict_storage["2"].value, ("2", 2))

    def test_from_example(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

    def test_from_example_like_dict(self):
        cache = LRUCache(2)

        cache["k1"] = "val1"
        cache["k2"] = "val2"
        self.assertIsNone(cache["k3"])
        self.assertEqual(cache["k2"], "val2")
        self.assertEqual(cache["k1"], "val1")
        cache["k3"] = "val3"
        self.assertEqual(cache["k3"], "val3")
        self.assertIsNone(cache["k2"])
        self.assertEqual(cache["k1"], "val1")


if __name__ == "__main__":
    unittest.main()
