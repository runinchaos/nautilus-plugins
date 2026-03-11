#!/usr/bin/env python3
import os
import subprocess

from gi.repository import Nautilus, GObject


class OpenOpencodeExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def _open_opencode(self, path):
        home = os.path.expanduser("~")
        bash_cmd = f'export NVM_DIR="{home}/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh" && opencode "{path}"; exec bash'
        subprocess.Popen(
            ["terminator", "-e", f"bash -c '{bash_cmd}'"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    def get_file_items(self, *args):
        files = args[-1]

        if not files or len(files) != 1:
            return

        file = files[0]
        if file.get_uri_scheme() != "file":
            return

        item = Nautilus.MenuItem(
            name="OpenOpencodeExtension::OpenOpencode",
            label="在 opencode 中打开",
            tip="在 opencode 中打开此文件或文件夹",
        )
        item.connect("activate", self.menu_activate_cb, file)
        return [item]

    def menu_activate_cb(self, menu, file):
        path = file.get_location().get_path()
        self._open_opencode(path)

    def get_background_items(self, *args):
        folder = args[-1]

        item = Nautilus.MenuItem(
            name="OpenOpencodeExtension::OpenOpencodeBackground",
            label="在 opencode 中打开",
            tip="在 opencode 中打开当前文件夹",
        )
        item.connect("activate", self.menu_background_activate_cb, folder)
        return [item]

    def menu_background_activate_cb(self, menu, folder):
        path = folder.get_location().get_path()
        self._open_opencode(path)
