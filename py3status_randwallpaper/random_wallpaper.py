# -*- coding: utf-8 -*-
"""
Allows you to change your background image (i.e. wallpaper).

This module sets a random wallpaper each time you start py3status.
Additionally, you can request a change by clicking on it.

Configuration parameters:
    button_next: Select the button used to set the wallpaper as the next
        in the list. (default 1)
    button_prev: Select the button used to set the wallpaper as the previous
        in the list. (default 3)
    button_rand: Select the button used to set a random wallpaper in the list.
        (default 2)
    cache_list: Set to True to cache the list of images. This will result
        in a faster and less power-consuming module, but you will need to
        reload the module to update the list of images. (default False)
    command: The command that will be executed to update the wallpaper. You
        must use '{}' as a placeholder for the path.
        (default 'feh --bg-scale {}')
    filter_extensions: The list of extensions that will be allowed for the
        wallpapers. Set to None to authorize all extensions.
        (default ['jpg', 'png'])
    first_image_path: Path to the first image to be loaded. This path should
        be in the list of found wallpapers. If set to None, a random image
        will be used. (default None)
    format_string: content that will be printed on the i3bar.
        (default 'Wallpaper {current_basename}')
    ignored_patterns: List of patterns to ignore when searching for wallpapers.
        (default [])
    recursive_search: Set to True to search for images in subdirectories.
        (default False)
    search_dirs: The list of directories to search for wallpapers.
        (default ['~/Pictures/'])
    screen_count: The number of screens, i.e. the number of wallpapers to set;
        or 'auto' to automatically detect the number of screens.
        (default 'auto')
    same_all_screens: True to set the same wallpaper on all screens, False to
        set different wallpapers for each screen. Has no effect if
        `screen_count` is 1.
        (default True)

Button reference: (see the official py3status reference if unsure, this might
    be outdated)
    1: left click
    2: middle click
    3: right click
    4: scroll up
    5: scroll down

Format placeholders:
    {full_name} Full name (including path) of the current(s) wallpaper(s)
    {basename} Basename (i.e. excluding path) of the current(s) wallpaper(s)

Requires:
    feh Used to set the background image (by default, unless you change the
        command parameter).

Author: rchaput <rchaput.pro@gmail.com>

License: Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0.html>
"""


import os
import subprocess
from fnmatch import fnmatch
from random import randint


def detect_number_of_screens():
    cmd = ['xrandr', '--listmonitors']
    output = subprocess.check_output(cmd).decode('utf-8').splitlines()
    output = [line for line in output if '+' in line]
    return len(output)


class WallpapersFinder:
    """Helper class to find wallpapers."""

    def __init__(self,
                 search_dirs,
                 recursive_search,
                 filter_extensions,
                 ignored_patterns):
        self._search_dirs = search_dirs
        self._recursive_search = recursive_search
        self._filter_extensions = filter_extensions
        self._ignored_patterns = ignored_patterns
        self.wallpapers = []

    def previous(self, index, number=1, same=True):
        if len(self.wallpapers) == 0:
            return None
        if same:
            return [(index - 1) % len(self.wallpapers) for _ in range(number)]
        else:
            return [(index - (i+1)) % len(self.wallpapers) for i in range(number)]

    def next(self, index, number=1, same=True):
        if len(self.wallpapers) == 0:
            return None
        if same:
            return [(index + 1) % len(self.wallpapers) for _ in range(number)]
        else:
            return [(index + i+1) % len(self.wallpapers) for i in range(number)]

    def random(self, index=None, number=1, same=True):
        if len(self.wallpapers) == 0:
            return None
        if same:
            new_index = randint(0, len(self.wallpapers) - 1)
            return [new_index for _ in range(number)]
        else:
            return [randint(0, len(self.wallpapers) - 1) for _ in range(number)]

    def search(self):
        """
        Search in all the configured directories and find the wallpapers.

        :return: The list of paths to all the found wallpapers.
        :rtype: list
        """
        wallpapers = []
        for dir_path in self._search_dirs:
            for wallpaper in self._search_in_dir(dir_path):
                wallpapers.append(wallpaper)
        self.wallpapers = wallpapers
        return wallpapers

    def _search_in_dir(self, dir_path):
        """
        Search only in the specified directory and yield the wallpapers.

        :param dir_path: The path to the requested directory. This path
            will be expanded (so `~` is authorized).
        :type dir_path: str
        """
        dir_path = os.path.expanduser(dir_path)
        for root, dirs, files in os.walk(dir_path, topdown=True):
            if not self._recursive_search:
                # delete the list of dirs, cancelling the recursion
                del dirs[:]
            # For each file, add it to wallpapers if it meets the conditions
            for file in files:
                abs_path = os.path.join(root, file)
                if self._should_add_file(abs_path):
                    yield abs_path

    def _should_add_file(self, filename):
        """
        Determine if the given filename should be added.

        The conditions are:
            - the extension must be correct (according to the configuration)
            - the file does not match an ignore pattern

        :param filename: The name of the file
        :type filename: str

        :return: `True` if the file meets all the conditions.
        """
        return self._is_extension_correct(filename) \
            and not self._is_ignored_file(filename)

    def _is_extension_correct(self, filename):
        """
        Determine if the given filename has a correct extension.

        :param filename: The absolute, relative path or even basename of
            the file (i.e. without the path).
        :type filename: str

        :return: `True` if `self.filter_extensions == None` or if it contains
            the extension of the given filename (e.g. jpg, png, etc.).
        """
        if self._filter_extensions is None:
            return True
        # splitext('/file.2.ext') returns ('/file.2', '.ext')
        # Thus [1] returns the 2nd value (i.e. the extension) '.ext'
        # And [1:] deletes the heading '.' in the extension 'ext'
        extension = os.path.splitext(filename)[1][1:]
        return extension in self._filter_extensions

    def _is_ignored_file(self, filename):
        """
        Determine if the file should be ignored.

        :param filename: The absolute, relative path or even basename of
            the file (i.e. without the path).

        :return: `True` if `self.ignored_patterns` is not None, and one of the
            patterns matches the given filename.
        """
        if self._ignored_patterns is None:
            return False
        for pattern in self._ignored_patterns:
            if fnmatch(filename, pattern):
                return True
        return False


class Py3status:

    # Public attributes (i.e. config parameters)
    button_next = 1
    button_prev = 3
    button_rand = 2
    cache_list = False
    command = 'feh --bg-scale {}'
    filter_extensions = [
        'jpg',
        'png'
    ]
    first_image_path = None
    format_string = 'Wallpaper {basename}'
    ignored_patterns = []
    recursive_search = False
    search_dirs = [
        '~/Pictures/'
    ]
    screen_count = 'auto'
    same_all_screens = True

    def __init__(self):
        self._current_indexes = None
        self._finder = None
        self._wallpapers = None
        self._error = None

    def show(self):
        """
        Main method, returns the module content to py3status.

        This is the method that will be called by py3status to compute the
        output and show it on the i3bar.
        """
        if self._error:
            format_string = 'Error! (code: {error_code})'
            full_text = self.py3.safe_format(format_string, self._error)
        else:
            full_names = [self._wallpapers[i] for i in self._current_indexes]
            basenames = [os.path.basename(p) for p in full_names]
            data = {'full_name': ' '.join(full_names),
                    'basename': ' '.join(basenames)}
            full_text = self.py3.safe_format(self.format_string, data)
        return {
            'full_text': full_text,
            'cached_until': self.py3.CACHE_FOREVER
        }

    def on_click(self, event):
        """
        Callback function, called when a click event is received.
        """
        # {'y': 13,'x': 1737, 'button': 1, 'name':'example','instance':'first'}
        if not self.cache_list:
            self._wallpapers = self._finder.search()
        indexes = self._current_indexes
        index = indexes[0] if indexes is not None else 0
        nb_screens = detect_number_of_screens() if self.screen_count == 'auto' \
            else self.screen_count
        if event['button'] == self.button_next:
            indexes = self._finder.next(index, nb_screens,
                                        self.same_all_screens)
        elif event['button'] == self.button_prev:
            indexes = self._finder.previous(index, nb_screens,
                                            self.same_all_screens)
        elif event['button'] == self.button_rand:
            indexes = self._finder.random(index, nb_screens,
                                          self.same_all_screens)
        if indexes is not None and indexes != self._current_indexes:
            self._current_indexes = indexes
            paths = [self._wallpapers[i] for i in self._current_indexes]
            self._set_wallpaper(paths)

    def post_config_hook(self):
        """
        Initialization method (after config parameters have been set).
        """
        self._finder = WallpapersFinder(self.search_dirs,
                                        self.recursive_search,
                                        self.filter_extensions,
                                        self.ignored_patterns)
        self._wallpapers = self._finder.search()
        nb_screens = detect_number_of_screens() if self.screen_count == 'auto' \
            else self.screen_count
        # get random index
        self._current_indexes = self._finder.random(None, nb_screens,
                                                    self.same_all_screens)
        if self._current_indexes is not None:
            paths = [self._wallpapers[i] for i in self._current_indexes]
            self._set_wallpaper(paths)
        else:
            self.py3.log('Could not find a suitable wallpaper',
                         self.py3.LOG_ERROR)
            self._error = {'error_code': -2}

    # Private Methods

    def _set_wallpaper(self, paths):
        """
        Change the current wallpaper.

        :param paths: List of paths to the desired wallpapers.
        :type paths: list

        :return: The error code from the command that will be executed
            to set the wallpaper. Usually, if this code is `0`, it means
            that the command succeeded. Otherwise it indicates a problem.
        :rtype: int
        """
        if paths is None:
            self.py3.log('Cannot set wallpaper: `paths` is not defined',
                         self.py3.LOG_ERROR)
            self._error = {'error_code': -1}
            return -1
        if len(paths) == 0:
            self.py3.log('Cannot set wallpaper: `paths` is empty',
                         self.py3.LOG_ERROR)
            self.error = {'error_code': -2}

        str_paths = ' '.join(paths)
        self._error = None
        self.py3.log('Trying to set wallpaper(s): %s' % str_paths,
                     self.py3.LOG_INFO)
        cmd = self.command.format(str_paths)
        try:
            code = self.py3.command_run(cmd)
        except self.py3.CommandError as e:
            code = e.error_code
            self._error = {'error_code': code}
            msg = 'Error while setting the wallpaper! Return code: %d ; ' \
                  'stdout: %s ; stderr: %s' % (code, e.output, e.error)
            self.py3.log(msg, self.py3.LOG_ERROR)
        return code


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from os.path import abspath, dirname, join
    from py3status.module_test import module_test
    config = {
        'recursive_search': True,
        'search_dirs': [join(dirname(dirname(abspath(__file__))), 'tests/data')]
    }

    module_test(Py3status, config=config)
