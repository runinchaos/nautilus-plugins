#!/usr/bin/env python3
import os
import subprocess

from gi.repository import Nautilus, GObject


class CreateEmptyFileExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def get_background_items(self, *args):
        folder = args[-1]

        item = Nautilus.MenuItem(
            name="CreateEmptyFileExtension::CreateEmptyFile",
            label="新建空白文档",
            tip="在当前目录创建空白文档",
        )
        item.connect("activate", self.create_file, folder)
        return [item]

    def create_file(self, menu, folder):
        path = folder.get_location().get_path()
        new_file = os.path.join(path, "新建文档.txt")

        i = 1
        while os.path.exists(new_file):
            new_file = os.path.join(path, f"新建文档{i}.txt")
            i += 1

        subprocess.run(["touch", new_file])
        subprocess.run(["notify-send", "文档已创建", f"{new_file}"])
