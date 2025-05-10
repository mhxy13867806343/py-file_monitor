#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件监控程序 - 自动删除指定文件

这个程序会监控指定的多个目录，当发现指定的文件时自动删除。
同时，它会定期扫描整个系统中的特定目录，查找并删除这些文件。

使用方法：
    python file_monitor.py [选项]

选项：
    --files FILE1,FILE2,...    指定要监控的文件名（逗号分隔，默认为diff_result.html）
    --dirs DIR1,DIR2,...       指定要监控的目录（逗号分隔）
    --interval SECONDS         指定全局扫描间隔（秒，默认为3600秒）
    --menu                     显示交互式菜单

默认会监控当前目录、用户主目录和VSCode扩展目录。
"""

import os
import sys
import time
import logging
import glob
import subprocess
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diff_monitor.log'))
    ]
)

# 默认配置
DEFAULT_CONFIG = {
    'target_files': ["diff_result.html"],  # 默认要删除的文件名列表
    'scan_interval': 3600,              # 默认扫描间隔（秒）
    'dirs': [
        os.getcwd(),                     # 当前工作目录
        str(Path.home()),                # 用户主目录
        '/Users/hooksvue/.windsurf/extensions'  # VSCode扩展目录
    ]
}

# 全局配置变量
CONFIG = DEFAULT_CONFIG.copy()

class FileMonitorHandler(FileSystemEventHandler):
    """处理文件系统事件的处理器"""
    
    def on_created(self, event):
        """当文件或目录被创建时调用"""
        if not event.is_directory and os.path.basename(event.src_path) in CONFIG['target_files']:
            try:
                os.remove(event.src_path)
                logging.info(f"已删除文件: {event.src_path}")
            except Exception as e:
                logging.error(f"删除文件失败: {event.src_path}, 错误: {e}")
    
    def on_modified(self, event):
        """当文件或目录被修改时调用"""
        if not event.is_directory and os.path.basename(event.src_path) in CONFIG['target_files']:
            try:
                os.remove(event.src_path)
                logging.info(f"已删除修改的文件: {event.src_path}")
            except Exception as e:
                logging.error(f"删除文件失败: {event.src_path}, 错误: {e}")

def scan_and_delete_existing():
    """扫描并删除已存在的目标文件"""
    count = 0
    for monitor_dir in CONFIG['dirs']:
        logging.info(f"扫描目录: {monitor_dir}")
        for root, _, files in os.walk(monitor_dir):
            for file in files:
                if file in CONFIG['target_files']:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        logging.info(f"已删除现有文件: {file_path}")
                        count += 1
                    except Exception as e:
                        logging.error(f"删除文件失败: {file_path}, 错误: {e}")
    
    if count > 0:
        logging.info(f"初始扫描已删除 {count} 个文件")
    else:
        logging.info(f"初始扫描未发现目标文件")


def global_scan_and_delete():
    """全局扫描并删除目标文件（使用find命令）"""
    try:
        total_count = 0
        for target_file in CONFIG['target_files']:
            # 使用find命令在整个系统中查找目标文件
            # 注意：这可能需要管理员权限才能扫描某些目录
            cmd = f"find ~ -name {target_file} -type f 2>/dev/null"
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            
            if result.stdout:
                files = result.stdout.strip().split('\n')
                count = 0
                for file_path in files:
                    if file_path and os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            logging.info(f"全局扫描删除文件: {file_path}")
                            count += 1
                        except Exception as e:
                            logging.error(f"全局扫描删除失败: {file_path}, 错误: {e}")
                
                if count > 0:
                    logging.info(f"全局扫描已删除 {count} 个 {target_file} 文件")
                    total_count += count
            else:
                logging.info(f"全局扫描未发现 {target_file} 文件")
        
        if total_count > 0:
            logging.info(f"全局扫描总共删除了 {total_count} 个文件")
    except Exception as e:
        logging.error(f"全局扫描出错: {e}")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='文件监控程序 - 自动删除指定文件')
    parser.add_argument('--files', type=str, help='要监控的文件名（逗号分隔）')
    parser.add_argument('--dirs', type=str, help='要监控的目录（逗号分隔）')
    parser.add_argument('--interval', type=int, help='全局扫描间隔（秒）')
    parser.add_argument('--menu', action='store_true', help='显示交互式菜单')
    
    args = parser.parse_args()
    
    # 更新配置
    if args.files:
        CONFIG['target_files'] = [f.strip() for f in args.files.split(',')]
    if args.dirs:
        dirs = [d.strip() for d in args.dirs.split(',')]
        CONFIG['dirs'] = [d for d in dirs if os.path.isdir(d)]
    if args.interval:
        CONFIG['scan_interval'] = args.interval
    
    return args.menu

def show_menu():
    """显示交互式菜单"""
    while True:
        print("\n文件监控程序 - 菜单")
        print("1. 查看当前配置")
        print("2. 设置监控文件")
        print("3. 设置监控目录")
        print("4. 设置扫描间隔")
        print("5. 开始监控")
        print("0. 退出程序")
        
        choice = input("请选择操作 [0-5]: ")
        
        if choice == '0':
            print("退出程序...")
            sys.exit(0)
        elif choice == '1':
            print("\n当前配置:")
            print(f"监控文件: {', '.join(CONFIG['target_files'])}")
            print(f"监控目录: {', '.join(CONFIG['dirs'])}")
            print(f"扫描间隔: {CONFIG['scan_interval']} 秒")
        elif choice == '2':
            files = input("请输入要监控的文件名（多个文件用逗号分隔）: ")
            if files.strip():
                CONFIG['target_files'] = [f.strip() for f in files.split(',')]
                print(f"已设置监控文件: {', '.join(CONFIG['target_files'])}")
        elif choice == '3':
            dirs = input("请输入要监控的目录（多个目录用逗号分隔）: ")
            if dirs.strip():
                input_dirs = [d.strip() for d in dirs.split(',')]
                valid_dirs = [d for d in input_dirs if os.path.isdir(d)]
                if valid_dirs:
                    CONFIG['dirs'] = valid_dirs
                    print(f"已设置监控目录: {', '.join(CONFIG['dirs'])}")
                else:
                    print("错误: 没有有效的目录")
        elif choice == '4':
            try:
                interval = int(input("请输入扫描间隔（秒）: "))
                if interval > 0:
                    CONFIG['scan_interval'] = interval
                    print(f"已设置扫描间隔: {interval} 秒")
                else:
                    print("错误: 间隔必须大于0")
            except ValueError:
                print("错误: 请输入有效的数字")
        elif choice == '5':
            print("开始监控...")
            break
        else:
            print("无效的选择，请重试")

def start_monitoring():
    """开始监控程序"""
    logging.info(f"开始监控以下目录:")
    for dir_path in CONFIG['dirs']:
        logging.info(f"  - {dir_path}")
    logging.info(f"目标文件: {', '.join(CONFIG['target_files'])}")
    logging.info(f"扫描间隔: {CONFIG['scan_interval']} 秒")
    
    # 先扫描并删除已存在的文件
    scan_and_delete_existing()
    
    # 执行一次全局扫描
    global_scan_and_delete()
    
    # 创建事件处理器
    event_handler = FileMonitorHandler()
    
    # 创建观察者
    observer = Observer()
    
    # 为每个监控目录设置观察者
    for dir_path in CONFIG['dirs']:
        observer.schedule(event_handler, dir_path, recursive=True)
        logging.info(f"已设置监控: {dir_path}")
    
    # 启动观察者
    observer.start()
    
    # 记录上次全局扫描时间
    last_global_scan = time.time()
    
    try:
        logging.info("监控程序已启动，按 Ctrl+C 停止...")
        while True:
            # 定期执行全局扫描
            current_time = time.time()
            if current_time - last_global_scan > CONFIG['scan_interval']:
                logging.info("执行定期全局扫描...")
                global_scan_and_delete()
                last_global_scan = current_time
            
            # 保持程序运行
            time.sleep(1)
    except KeyboardInterrupt:
        # 当用户按下 Ctrl+C 时
        logging.info("监控程序停止...")
        observer.stop()
    
    # 等待观察者完成
    observer.join()

def main():
    """主函数"""
    # 解析命令行参数
    show_menu_flag = parse_arguments()
    
    # 如果指定了--menu参数，显示交互式菜单
    if show_menu_flag:
        show_menu()
    
    # 开始监控
    start_monitoring()

if __name__ == "__main__":
    main()
