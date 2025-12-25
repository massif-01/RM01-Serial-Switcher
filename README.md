# RM-01 串口切换工具

## 简介

一个用于通过串口控制台在 RM-01 设备的不同模块之间切换的工具。

## 功能特性

**切换到推理模块**
   - 自动检测 `/dev/ttyACM0`
   - 连接到串口控制台
   - 执行 `usbmux agx` 命令
   - 保存配置

**切换到应用模块**
   - 自动检测 `/dev/ttyACM0`
   - 连接到串口控制台
   - 执行 `usbmux lpmu` 命令
   - 保存配置

## 前置要求

- Linux 操作系统
- Python 3.6+
- 已安装 `tio` 串口终端工具
- `pexpect` Python 库

## 安装

1. 安装系统依赖：
```bash
# Ubuntu/Debian
sudo apt install tio

# Arch Linux
sudo pacman -S tio
```

2. 安装 Python 依赖：
```bash
pip3 install -r requirements.txt
```

## 使用方法

```bash
python3 main.py
# 或者
./run.sh
```

## 系统要求

- Linux 操作系统
- Python 3.6+
- tio 串口终端
- 访问 `/dev/ttyACM0` 的权限（可能需要 sudo 或将用户添加到 dialout 组）

## 用户权限设置

要在不使用 sudo 的情况下访问串口，请将您的用户添加到 dialout 组：

```bash
sudo usermod -a -G dialout $USER
```

然后注销并重新登录以使更改生效。

## 注意事项

- 工具会自动等待 `/dev/ttyACM0` 可用
- 如果 10 秒后仍未检测到设备，操作将失败
- 确保 RM-01 设备已通过 USB 正确连接

