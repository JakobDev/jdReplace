<h1 align="center">jdReplace</h1>

<h3 align="center">With jdReplace you can replace a text in all files of a directorys</h3>

<p align="center">
    <img alt="jdReplace" src="screenshots/MainWindow_en.png"/>
</p>

jdReplace is a simple mass search and replace tool.
You set a directory, a text to replace, the replacement and click OK.
jdReplace will do the rest.

## Install

### Flatpak
You can get jdReplace from [Flathub](https://flathub.org/apps/page.codeberg.JakobDev.jdReplace)

### AUR
Arch Users can get jdReplace from the [AUR](https://aur.archlinux.org/packages/jdreplace)

### pip
You can install jdReplace from [PyPI](https://pypi.org/project/jdReplace) using `pip`:
```shell
pip install jdReplace
```
Using this Method, it will not include a Desktop Entry or any other Data file, so you need to run jdReplace from the Command Line.
Use this only, when nothing else works.

### From source
This is only for experienced Users and someone, who wants to package jdReplace for a Distro.
jdReplaceshould be installed as a Python package.
You can use `pip` or any other tool that can handle Python packages.
You need to have `lrelease` installed to build the Package.
After that, you should run `install-unix-datafiles.py` which wil install things like the Desktop Entry or the Icon in the correct place.
It defaults to `/usr`, but you can change it with the `--prefix` argument.
It also applies the translation to this files.
You need gettext installed to run `install-unix-datafiles.py`.

Here's a example of installing jdReplace into `/usr/local`:
```shell
sudo pip install --prefix /usr/local .
sudo ./install-unix-datafiles.py --prefix /usr/local
```

## Translate
You can help translating jdReplace on [Codeberg Translate](https://translate.codeberg.org/projects/jdReplace)

## Develop
jdReplaceis written in Python and uses PyQt6 as GUI toolkit. You should have some experience in both.
You can run `jdReplace.py`to start jdReplace from source and test your local changes.
It ships with a few scripts in the tools directory that you need to develop.

#### BuildTranslations.py
This script takes all `.ts` files and compiles it to `.qm` files.
The `.ts` files are containing the translation source and are being used during the translation process.
The `.qm` contains the compiled translation and are being used by the Program.
You need to compile a `.ts` file to a `.qm` file to see the translations in the Program.

#### UpdateTranslations.py
This regenerates the `.ts` files. You need to run it, when you changed something in the source code.
The `.ts` files are contains the line in the source, where the string to translate appears,
so make sure you run it even when you don't changed a translatable string, so the location is correct.

####  UpdateUnixDataTranslations.py
This regenerates the translation files in `deploy/translations`. these files contains the translations for the Desktop Entry and the AppStream File.
It uses gettext, as it is hard to translate this using Qt.
These files just exists to integrate the translation with Weblate, because Weblate can't translate the Desktop Entry and the AppStream file.
Make sure you run this when you edited one of these files.
You need to have gettext installed to use it.
