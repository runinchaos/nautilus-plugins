#!/usr/bin/env python3
import os
import subprocess

from gi.repository import Nautilus, GObject


class CopyPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def get_file_items(self, *args):
        files = args[-1]

        if not files:
            return

        item = Nautilus.MenuItem(
            name="CopyPathExtension::CopyPath",
            label="复制绝对路径",
            tip="Copy full path of selected file",
        )
        item.connect("activate", self.copy_path, files)
        return [item]

    def copy_path(self, menu, files):
        paths = []
        for file in files:
            paths.append(file.get_location().get_path())

        text = "\n".join(paths) if len(paths) > 1 else paths[0]
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())

        subprocess.run(
            ["notify-send", "路径已复制", f"已复制 {len(paths)} 个文件的路径"]
        )

    def get_background_items(self, *args):
        folder = args[-1]
        item = Nautilus.MenuItem(
            name="CopyPathExtension::CopyPathBackground",
            label="复制当前目录路径",
            tip="Copy current folder path",
        )
        item.connect("activate", self.copy_background_path, folder)
        return [item]

    def copy_background_path(self, menu, folder):
        path = folder.get_location().get_path()
        subprocess.run(["xclip", "-selection", "clipboard"], input=path.encode())
        subprocess.run(["notify-send", "路径已复制", f"已复制目录: {path}"])


class CopyParentPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def get_file_items(self, *args):
        files = args[-1]

        if not files:
            return

        item = Nautilus.MenuItem(
            name="CopyParentPathExtension::CopyParentPath",
            label="复制父目录路径",
            tip="Copy parent directory path",
        )
        item.connect("activate", self.copy_parent_path, files)
        return [item]

    def copy_parent_path(self, menu, files):
        paths = []
        for file in files:
            path = file.get_location().get_path()
            parent = os.path.dirname(path)
            if parent not in paths:
                paths.append(parent)

        text = "\n".join(paths) if len(paths) > 1 else paths[0]
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())

        subprocess.run(
            ["notify-send", "路径已复制", f"已复制 {len(paths)} 个父目录路径"]
        )


class OpenOpencodeExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def _open_opencode(self, path):
        # 使用 terminator 启动 opencode，需要加载 nvm 环境
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
