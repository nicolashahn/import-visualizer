import unittest

import vis


class TestVis(unittest.TestCase):
    def test_project_dir(self):
        expected_mod_names = set(
            [
                "main",
                "module_a",
                "module_b",
                "path",
                "path.to",
                "path.to.module_c",
                "module_d",
                "hello",
            ]
        )
        modules = vis.get_modules_in_dir("project")
        self.assertEqual(set(modules.keys()), expected_mod_names)


if __name__ == "__main__":
    unittest.main()
