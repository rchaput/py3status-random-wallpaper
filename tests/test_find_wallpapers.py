"""
This module tests the `search` method of `WallpapersFinder`, i.e. the
ability to find wallpapers in specific folders (with recursive search,
ignored patterns, extensions, etc.).
"""


import os
import unittest

from py3status_randwallpaper.random_wallpaper import WallpapersFinder

# The path to this folder (the `tests/` folder in the project).
tests_dir = os.path.dirname(os.path.abspath(__file__))
# The path to the data folder (`tests/data`).
data_dir = os.path.join(tests_dir, 'data')


class TestWallpapers(unittest.TestCase):

    def test_search_simple(self):
        finder = WallpapersFinder(
            search_dirs=[os.path.join(data_dir, 'dir2')],
            recursive_search=False,
            filter_extensions=['jpg', 'png'],
            ignored_patterns=None
        )
        wallpapers = finder.search()
        truth = [os.path.join(data_dir, 'dir2', 'picture4.png')]
        self.assertSetEqual(set(wallpapers), set(truth))

    def test_search_recursive(self):
        finder = WallpapersFinder(
            search_dirs=[os.path.join(data_dir, 'dir1')],
            recursive_search=True,
            filter_extensions=['jpg', 'png'],
            ignored_patterns=None
        )
        wallpapers = finder.search()
        truth = [os.path.join(data_dir, 'dir1', 'subdir1', 'picture3.jpg'),
                 os.path.join(data_dir, 'dir1', 'not_this1.jpg'),
                 os.path.join(data_dir, 'dir1', 'picture1.jpg'),
                 os.path.join(data_dir, 'dir1', 'picture2.png')]
        self.assertSetEqual(set(wallpapers), set(truth))

    def test_search_ignore_patterns(self):
        finder = WallpapersFinder(
            search_dirs=[os.path.join(data_dir, 'dir1')],
            recursive_search=False,
            filter_extensions=['jpg', 'png'],
            ignored_patterns=['**/not*']
        )
        wallpapers = finder.search()
        truth = [os.path.join(data_dir, 'dir1', 'picture1.jpg'),
                 os.path.join(data_dir, 'dir1', 'picture2.png')]
        self.assertSetEqual(set(wallpapers), set(truth))

    def test_search_extensions(self):
        finder = WallpapersFinder(
            search_dirs=[os.path.join(data_dir, 'dir1')],
            recursive_search=False,
            filter_extensions=['png'],
            ignored_patterns=None
        )
        wallpapers = finder.search()
        truth = [os.path.join(data_dir, 'dir1', 'picture2.png')]
        self.assertSetEqual(set(wallpapers), set(truth))


if __name__ == '__main__':
    unittest.main()
