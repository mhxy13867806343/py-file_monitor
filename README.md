# 文件监控程序

这个Python程序会监控指定的多个目录，当发现 `diff_result.html` 文件时自动删除。同时，它会定期扫描整个系统中的特定目录，查找并删除 `diff_result.html` 文件。

## 功能特点

- 实时监控多个指定目录
- 自动删除新创建或修改的目标文件
- 定期执行全局扫描，清理系统中的目标文件
- 详细的日志记录
- 支持通过命令行参数添加额外的监控目录

## 使用方法

```bash
python file_monitor.py [额外监控目录1] [额外监控目录2] ...
```

### 默认监控目录

- 当前工作目录
- 用户主目录
- VSCode扩展目录 (`~/.windsurf/extensions`)

## 在后台运行

要在后台运行此程序，可以使用以下命令：

```bash
nohup python file_monitor.py > /dev/null 2>&1 &
```

## 系统要求

- Python 3.6+
- watchdog 库 (`pip install watchdog`)

## 日志

程序会生成日志文件 `diff_monitor.log`，记录所有操作和错误信息。
