# -*- coding: utf-8 -*-
"""
Allows you to change your background image (i.e. wallpaper).

This module sets a random wallpaper each time you start py3status. Additionally,
you can request a change by clicking on it.

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
    command: The command that will be executed to update the wallpaper. You must
        use '{}' as a placeholder for the path. (default 'feh --bg-scale {}')
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

Button reference: (see the official py3status reference if unsure, this might be
    outdated)
    1: left click
    2: middle click
    3: right click
    4: scroll up
    5: scroll down

Format placeholders:
    {current_name} Full name (including path) of the current wallpaper
    {current_basename} Basename (i.e. excluding path) of the current wallpaper

Requires:
    feh Used to set the background image (by default, unless you change the
        command parameter).

Author: rchaput <rchaput.pro@gmail.com>

License: Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0.html>
"""


import os
from fnmatch import fnmatch
from random import randint


def detect_number_of_screens():
    cmd = ['xrandr', '--query']


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

    def previous(self, index):
        if len(self.wallpapers) == 0:
            return None
        return (index - 1) % len(self.wallpapers)

    def next(self, index):
        if len(self.wallpapers) == 0:
            return None
        return (index + 1) % len(self.wallpapers)

    def random(self, index=None):
        if len(self.wallpapers) == 0:
            return None
        new_index = index
        while new_index == index:
            new_index = randint(0, len(self.wallpapers) - 1)
        return new_index

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

    def __init__(self):
        self._current_index = None
        self._current_name = None
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
            data = {'full_name': self._current_name,
                    'basename': os.path.basename(self._current_name)}
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
        index = self._current_index
        if event['button'] == self.button_next:
            index = self._finder.next(index)
        elif event['button'] == self.button_prev:
            index = self._finder.previous(index)
        elif event['button'] == self.button_rand:
            index = self._finder.random(index)
        if index != self._current_index:
            self._current_index = index
            self._set_wallpaper(self._wallpapers[self._current_index])

    def post_config_hook(self):
        """
        Initialization method (after config parameters have been set).
        """
        self._finder = WallpapersFinder(self.search_dirs,
                                        self.recursive_search,
                                        self.filter_extensions,
                                        self.ignored_patterns)
        self._wallpapers = self._finder.search()
        if self.first_image_path is None:
            # get random index
            self._current_index = self._finder.random()
        else:
            # get index of given path
            try:
                self._current_index = \
                    self._wallpapers.index(self.first_image_path)
            except ValueError:
                msg = 'Tried to force first image but path %s was not found ' \
                      'in the list of wallpapers' % self.first_image_path
                self.py3.log(msg, self.py3.LOG_WARNING)
                self._current_index = 0
        if self._current_index is not None:
            self._set_wallpaper(self._wallpapers[self._current_index])
        else:
            msg = 'Could not find a suitable wallpaper'
            self.py3.log(msg, self.py3.LOG_ERROR)
            self._error = {'error_code': -2}

    # Private Methods

    def _set_wallpaper(self, path):
        """
        Change the current wallpaper.

        :param path: The full path to the desired wallpaper. Must not be None.
        :type path: str

        :return: The error code from the command that will be executed
            to set the wallpaper. Usually, if this code is `0`, it means
            that the command succeeded. Otherwise it indicates a problem.
        :rtype: int
        """
        if path is None:
            msg = 'Cannot set wallpaper: path is not defined'
            self.py3.log(msg, self.py3.LOG_ERROR)
            self._error = {'error_code': -1}
            return -1

        self._error = None
        msg = 'Trying to set wallpaper: %s' % path
        self.py3.log(msg, self.py3.LOG_INFO)
        cmd = self.command.format(path)
        try:
            code = self.py3.command_run(cmd)
            self._current_name = path
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
    config = {
        'recursive_search': True,
    }
    from py3status.module_test import module_test

    module_test(Py3status, config=config)
