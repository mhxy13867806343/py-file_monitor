#!/bin/bash

# 文件监控运行脚本
# 作者: hooksvue
# 日期: 2025-05-10

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查watchdog库是否安装
if ! python3 -c "import watchdog" &> /dev/null; then
    echo "正在安装必要的依赖库..."
    pip3 install watchdog
fi

# 显示帮助信息
show_help() {
    echo "文件监控程序 - 使用说明"
    echo "用法: ./run_monitor.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --files FILE1,FILE2,...  指定要监控的文件名（逗号分隔）"
    echo "  --dirs DIR1,DIR2,...     指定要监控的目录（逗号分隔）"
    echo "  --interval SECONDS       指定全局扫描间隔（秒）"
    echo "  --menu                   显示交互式菜单"
    echo "  --help                   显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  ./run_monitor.sh --files diff_result.html,temp.log --dirs ~/Desktop,~/Documents"
    echo "  ./run_monitor.sh --menu"
    echo "  ./run_monitor.sh --interval 1800"
}

# 处理--help参数
for arg in "$@"; do
    if [ "$arg" == "--help" ]; then
        show_help
        exit 0
    fi
done

echo "启动文件监控程序..."
echo "按 Ctrl+C 停止运行"
echo ""

# 运行Python脚本，传递所有命令行参数
python3 "$SCRIPT_DIR/file_monitor.py" "$@"
