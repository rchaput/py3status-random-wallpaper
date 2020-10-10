"""
This module tests the `previous`, `next` and `random` methods of
`WallpapersFinder`, i.e. the ability to compute new indexes for wallpapers,
with number of screens, same or different images.
"""


import unittest
import random

from py3status_randwallpaper.random_wallpaper import WallpapersFinder


class TestWallpapers(unittest.TestCase):

    def test_previous(self):
        finder = WallpapersFinder(None, None, None, None)
        finder.wallpapers = ['picture1', 'picture2', 'picture3']
        # Previous of 1 is 0
        indexes = finder.previous(1, number=1, same=True)
        self.assertListEqual(indexes, [0])
        indexes = finder.previous(1, number=1, same=False)
        self.assertListEqual(indexes, [0])
        # Previous of 0 is 2
        indexes = finder.previous(0, number=1, same=True)
        self.assertListEqual(indexes, [2])
        # Same previous
        indexes = finder.previous(0, number=2, same=True)
        self.assertListEqual(indexes, [2, 2])
        # Different previous
        indexes = finder.previous(0, number=2, same=False)
        self.assertListEqual(indexes, [2, 1])
        # More previous than available length
        indexes = finder.previous(2, number=4, same=True)
        self.assertListEqual(indexes, [1, 1, 1, 1])
        indexes = finder.previous(2, number=4, same=False)
        self.assertListEqual(indexes, [1, 0, 2, 1])

    def test_next(self):
        finder = WallpapersFinder(None, None, None, None)
        finder.wallpapers = ['picture1', 'picture2', 'picture3']
        # Next of 1 is 2
        indexes = finder.next(1, number=1, same=True)
        self.assertListEqual(indexes, [2])
        indexes = finder.next(1, number=1, same=False)
        self.assertListEqual(indexes, [2])
        # Next of 2 is 0
        indexes = finder.next(2, number=1, same=True)
        self.assertListEqual(indexes, [0])
        # Same next
        indexes = finder.next(2, number=2, same=True)
        self.assertListEqual(indexes, [0, 0])
        # Different next
        indexes = finder.next(2, number=2, same=False)
        self.assertListEqual(indexes, [0, 1])
        # More next than available length
        indexes = finder.next(0, number=4, same=True)
        self.assertListEqual(indexes, [1, 1, 1, 1])
        indexes = finder.next(2, number=4, same=False)
        self.assertListEqual(indexes, [0, 1, 2, 0])

    def test_random(self):
        finder = WallpapersFinder(None, None, None, None)
        finder.wallpapers = ['picture1', 'picture2', 'picture3']
        # Set the seed for reproducibility
        random.seed(42)
        # One random
        indexes = finder.random(None, number=1, same=True)
        self.assertListEqual(indexes, [2])
        # Same random
        indexes = finder.random(None, number=2, same=True)
        self.assertListEqual(indexes, [0, 0])
        # Different random
        indexes = finder.random(None, number=2, same=False)
        self.assertListEqual(indexes, [0, 2])
        # More random than available length
        indexes = finder.random(None, number=4, same=True)
        self.assertListEqual(indexes, [1, 1, 1, 1])
        indexes = finder.random(None, number=4, same=False)
        self.assertListEqual(indexes, [0, 0, 0, 2])


if __name__ == '__main__':
    unittest.main()
