# py3status-random-wallpaper
> Author: rchaput <rchaput.pro@gmail.com>

This is a [py3status] module allowing you to set a random wallpaper from
your library.

Each time the module is loaded (for example, when the i3bar is started), it
will pick a new random wallpaper. You can then navigate through the different
wallpapers or ask for another random by clicking on the module.

## Install

By default, this module requires [feh] to set your wallpaper. You must
install [feh], either by downloading the sources or using your
distribution's package manager (for example, `apt install feh`).
You can also set another backend software, please refer to the [configuration]
section to do so.

Download the Wheel (.whl) file in the [releases] section and install it using
`pip install py3status-random-wallpaper-1.0.whl`.

Then, add this module to your py3status configuration file: usually, this
will be located in `~/.config/i3/py3status.conf`. 
Add the following block in order to ask [py3status] to show this module on
your i3bar:
```
order += "random_wallpaper"
random_wallpaper {
    search_dirs = ['~/Pictures/Wallpapers/']
}
```

You can read more about this module's configuration parameters in the 
[dedicated section](#configuration).

Reload your i3 configuration, and admire your new wallpaper!


## Configuration

*py3status-random-wallpaper* was made with high configurability in mind.
The default configuration should be fine for most users, but here is the
complete list should you need to tweak the parameters:

+ **button_next**
  + Select the button used to set the wallpaper as the next
    in the list. See [this page][buttons] for a reference of the allowed
    values. For example, `1` represents the left click.
  + Default: `1`
+ **button_prev**
  + Select the button used to set the wallpaper as the previous
    in the list.  See [this page][buttons] for a reference of the allowed
    values. For example, `3` represents the right click.
  + Default: `3`
+ **button_rand**
  + Select the button used to set a random wallpaper in the list. See
    [this page][buttons] for a reference of the allowed values. For example,
    `2` represents the middle click.
  + Default: `2`
+ **cache_list**
  + Set to True to cache the list of images. This will result
    in a faster and less power-consuming module, but you will need to
    reload the module to update the list of images (by reloading i3 for
    example).
  + Default: `False`
+ **command**
  + The command that will be executed to update the wallpaper. You must
    use `{}` as a placeholder for the path. `feh` has been tested and should
    work, but you can replace it if you prefer another software. You can
    also change the `--bg-scale` parameter, please refer to the 
    [feh man page][feh-man] (*Background Settings*) for more information.
  + Default: `'feh --bg-scale {}'`
+ **filter_extensions**
  + The list of extensions that will be allowed for the
    wallpapers. Set to `None` to authorize all extensions. Please make sure
    that the extensions are supported by your software (usually, `feh`),
    otherwise you might run into errors.
  + Default: `['jpg', 'png']`
+ **first_image_path**
  + Path to the first image to be loaded. This path should
    be in the list of found wallpapers. If set to `None`, a random image
    will be used. 
  + Default: `None`
+ **format_string**
  + Content that will be printed on the i3bar. You can use `{basename}` and
    `{full_name}` as placeholders for the current wallpaper's basename
    (for example *mywallpaper.png*) and full name (for example 
    *~/Pictures/mywallpaper.png*), respectively.
  + Default: `'Wallpaper {basename}'`
+ **ignore_files**
  + List of filename to ignore when searching for wallpapers.
  + Default: `[]`
+ **recursive_search**
  + Set to True to search for images in subdirectories.
  + Default: `False`
+ **search_dirs**
  + The list of directories to search for wallpapers.
  + Default: `['~/Pictures/']`
  
You can override these values in your py3status configuration file,
which is usually `~/.config/i3/py3status.conf`.


## Contributing

Your contributions are welcome: if you want to report a bug, propose an
enhancement, please refer to the [Issues page][issues]. You can also create
a [Pull Request][pr].


## License

This project is licensed under the [Apache License][license].

Basically, this means that you are allowed to modify and distribute this
project, but you must include the [License file][license] and state the
changes you've made (please refer to the [License file][license] or the
https://choosealicense.com/licenses/apache-2.0/ website for the full
list of permissions, conditions and limitations).



[py3status]: https://github.com/ultrabug/py3status/ "py3status on GitHub"
[feh]: https://feh.finalrewind.org/ "feh's project page"
[releases]: https://github.com/rchaput/py3status-random-wallpaper/releases "py3status-random-wallpaper releases page on GitHub"
[issues]: https://github.com/rchaput/py3status-random-wallpaper/issues "py3status-random-wallpaper issues page on GitHub"
[buttons]: https://py3status.readthedocs.io/en/latest/configuration.html#custom-click-events "py3status documentation"
[feh-man]: https://linux.die.net/man/1/feh "feh man page"
[license]: ./LICENSE
