#!/bin/bash

# 文件监控安装脚本
# 作者: hooksvue
# 日期: 2025-05-10

echo "部署文件监控程序 - 安装与使用说明:"
echo ""

# 检查是否安装了Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否安装了watchdog库
if ! python3 -c "import watchdog" &> /dev/null; then
    echo "正在安装必要的依赖库..."
    pip3 install watchdog
fi

# 创建安装目录
INSTALL_DIR="/usr/local/bin"
sudo mkdir -p $INSTALL_DIR

# 下载文件监控程序
echo "正在下载文件监控程序..."
sudo curl -fsSL \
    https://raw.githubusercontent.com/mhxy13867806343/py-file_monitor/main/file_monitor.py \
    -o $INSTALL_DIR/filemonitor

# 添加执行权限
sudo chmod +x $INSTALL_DIR/filemonitor

# 创建数据目录
DATA_DIR="$HOME/.filemonitor"
mkdir -p "$DATA_DIR"

# 创建启动脚本
cat > /tmp/filemonitor_launcher << 'EOF'
#!/bin/bash

# 创建数据目录
DATA_DIR="$HOME/.filemonitor"
mkdir -p "$DATA_DIR"

# 运行Python脚本
python3 /usr/local/bin/filemonitor "$@"
EOF

sudo mv /tmp/filemonitor_launcher $INSTALL_DIR/filemonitor_launcher
sudo chmod +x $INSTALL_DIR/filemonitor_launcher

# 创建软链接
sudo ln -sf $INSTALL_DIR/filemonitor_launcher $INSTALL_DIR/filemonitor_run

# 检查是否安装成功
echo "检查是否安装成功:"
ls -l $INSTALL_DIR | grep filemonitor

echo "确保 $INSTALL_DIR 在 PATH 中"
echo $PATH

echo ""
echo "安装完成! 您可以使用以下命令运行文件监控程序:"
echo "filemonitor_run          # 使用默认设置运行"
echo "filemonitor_run --menu   # 显示交互式菜单"
echo "filemonitor_run --files file1.html,file2.log --dirs /path1,/path2  # 指定监控文件和目录"
echo ""
echo "在后台运行:"
echo "nohup filemonitor_run > /dev/null 2>&1 &"
echo ""
echo "查看帮助:"
echo "filemonitor_run --help"
