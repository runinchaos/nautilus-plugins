# Nautilus 扩展插件

一组用于 GNOME Nautilus 文件管理器的 Python 扩展。

## 安装

```bash
# 安装依赖
sudo apt install python3-nautilus python3-yaml xclip

# 克隆仓库
git clone https://github.com/runinchaos/nautilus-plugins.git

# 复制扩展到 Nautilus 扩展目录
cp nautilus-plugins/*.py ~/.local/share/nautilus-python/extensions/

# 重启 Nautilus
nautilus -q
```

## 扩展功能

### open_terminal.py - 在 Terminator 中打开

右键菜单添加"在Terminator中打开"选项，在当前目录打开 Terminator 终端。

### copypath.py - 复制路径

提供两个右键菜单选项：
- **复制绝对路径** - 复制选中文件的完整路径
- **复制父目录路径** - 复制选中文件所在目录的路径
- **复制当前目录路径** - 在空白处右键时复制当前目录路径

### open_opencode.py - 在 opencode 中打开

右键菜单添加"在 opencode 中打开"选项，在 Terminator 终端中启动 opencode 并切换到当前目录。

### create_empty_file.py - 新建空白文档

右键空白处添加"新建空白文档"选项，在当前目录创建空的 txt 文件。
