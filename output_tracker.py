#!/usr/bin/env python3
import os
import subprocess

from gi.repository import Nautilus, GObject

# 打开窗口时先回显的末尾行数，设为 0 则只显示 tail -f 默认的 10 行
TAIL_LINES = 100


class OutputTrackerExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        pass

    def get_file_items(self, *args):
        files = args[-1]

        if not files or len(files) != 1:
            return

        file = files[0]
        if file.is_directory() or file.get_uri_scheme() != "file":
            return

        path = file.get_location().get_path()
        if not path or not os.path.isfile(path):
            return

        item = Nautilus.MenuItem(
            name="OutputTrackerExtension::OutputTracker",
            label="输出跟踪",
            tip="在新 Terminator 窗口中 tail -f %s" % file.get_name(),
        )
        item.connect("activate", self.menu_activate_cb, file)
        return [item]

    def get_background_items(self, *args):
        # 空白处右键不显示任何条目；此方法必须存在，否则 nautilus-python 会报
        # “object ... is not initialized”
        return []

    def menu_activate_cb(self, menu, file):
        path = file.get_location().get_path()
        if not path:
            return

        command = [
            "terminator",
            "-u",  # 强制新进程、不走 DBus，保证每次都是独立的新窗口
            "--working-directory=%s" % os.path.dirname(path),
            "-T",
            "输出跟踪: %s" % os.path.basename(path),
        ]
        # -x 之后的参数由 Terminator 直接 exec，不经过 shell，路径含空格也安全
        if TAIL_LINES > 0:
            command += ["-x", "tail", "-n", str(TAIL_LINES), "-f", path]
        else:
            command += ["-x", "tail", "-f", path]

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
