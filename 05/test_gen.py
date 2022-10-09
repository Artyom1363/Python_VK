import unittest
from generator import gen_from_file


class TestGenFromFile(unittest.TestCase):
    def test_gen_from_file(self):

        lines = list(gen_from_file("test_data/file.txt", ["боже", "И"]))
        self.assertEqual(lines, ["И лучше выдумать не мог.\n",
                                 "Но, боже мой, какая скука\n",
                                 "С больным сидеть и день и ночь,\n",
                                 "Вздыхать и думать про себя:\n"])
        lines = list(gen_from_file("test_data/file.txt"))
        self.assertEqual(lines, [])


if __name__ == "__main__":
    unittest.main()
