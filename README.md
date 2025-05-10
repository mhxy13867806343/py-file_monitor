# 文件监控程序

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![Last Updated](https://img.shields.io/badge/last%20updated-2025--05--10-brightgreen)](https://github.com/mhxy13867806343/py-file_monitor)

这个程序会监控指定的多个目录，当发现指定文件（默认为 `diff_result.html`）时自动删除。同时，它会定期扫描整个系统中的特定目录，查找并删除这些文件。

## 功能特点

- 实时监控多个指定目录
- 可配置监控多种不同的文件
- 自动删除新创建或修改的目标文件
- 定期执行全局扫描，清理系统中的目标文件
- 交互式菜单界面，方便配置
- 详细的日志记录
- 支持命令行参数自定义配置

## 快速安装

### 方法1：使用安装脚本（推荐）

```bash
# 下载安装脚本
curl -fsSL https://raw.githubusercontent.com/mhxy13867806343/py-file_monitor/main/install_monitor.sh -o install_monitor.sh

# 添加执行权限
chmod +x install_monitor.sh

# 运行安装脚本
sudo ./install_monitor.sh
```

安装完成后，可以通过以下命令运行：

```bash
filemonitor_run          # 使用默认设置运行
filemonitor_run --menu   # 显示交互式菜单
```

### 方法2：直接运行

```bash
# 下载运行脚本
curl -fsSL https://raw.githubusercontent.com/mhxy13867806343/py-file_monitor/main/run_monitor.sh -o run_monitor.sh

# 添加执行权限
chmod +x run_monitor.sh

# 运行程序
./run_monitor.sh
```

## 使用方法

### 命令行参数

```bash
# Python脚本方式
python file_monitor.py [选项]

# 安装后使用
filemonitor_run [选项]

# 或使用运行脚本
./run_monitor.sh [选项]
```

### 可用选项

- `--files FILE1,FILE2,...` - 指定要监控的文件名（逗号分隔，默认为diff_result.html）
- `--dirs DIR1,DIR2,...` - 指定要监控的目录（逗号分隔）
- `--interval SECONDS` - 指定全局扫描间隔（秒，默认为3600秒）
- `--menu` - 显示交互式菜单

### 默认监控目录

- 当前工作目录
- 用户主目录
- VSCode扩展目录 (`~/.windsurf/extensions`)

## 在后台运行

要在后台运行此程序，可以使用以下命令：

```bash
# 直接运行Python脚本
nohup python file_monitor.py > /dev/null 2>&1 &

# 或使用安装后的命令
nohup filemonitor_run > /dev/null 2>&1 &

# 或使用运行脚本
nohup ./run_monitor.sh > /dev/null 2>&1 &
```

## 系统要求

- Python 3.6+
- watchdog 库 (`pip install watchdog`)
- 支持的操作系统：macOS, Linux, Windows

## 脚本说明

- `file_monitor.py` - 主程序文件
- `install_monitor.sh` - 系统安装脚本，将程序安装到系统中
- `run_monitor.sh` - 本地运行脚本，无需安装即可运行

## 日志

程序会生成日志文件 `diff_monitor.log`，记录所有操作和错误信息。日志文件存储在程序所在目录或用户主目录中。

## 开源许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT) 开源。

```
MIT License

Copyright (c) 2025 hooksvue

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 版本历史

- **v1.0.0** (2025-05-10)
  - 初始版本发布
  - 支持监控多个文件和目录
  - 添加交互式菜单
  - 提供安装脚本和运行脚本

## 作者

- **hooksvue** - [GitHub](https://github.com/mhxy13867806343)

## 贡献

欢迎提交问题和功能请求！如果您想贡献代码，请提交Pull Request。
