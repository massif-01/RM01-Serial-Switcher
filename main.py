#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RM-01 串口切换工具
"""

import os
import sys
import subprocess
import time
import pexpect


def print_logo():
    """显示应用程序标志"""
    print("\n")
    print("    ██████╗ ███╗   ███╗██╗███╗   ██╗████████╗███████╗")
    print("    ██╔══██╗████╗ ████║██║████╗  ██║╚══██╔══╝██╔════╝")
    print("    ██████╔╝██╔████╔██║██║██╔██╗ ██║   ██║   █████╗  ")
    print("    ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║   ██║   ██╔══╝  ")
    print("    ██║  ██║██║ ╚═╝ ██║██║██║ ╚████║   ██║   ███████╗")
    print("    ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝")
    print("")
    print("\n" + "-"*50)
    print("RM-01 串口切换工具")
    print("-"*50)


def check_ttyacm0_exists() -> bool:
    """使用 tio -l 检查 /dev/ttyACM0 是否存在"""
    try:
        result = subprocess.run(['tio', '-l'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return '/dev/ttyACM0' in result.stdout
    except Exception as e:
        print(f"警告：检查 ttyACM0 失败：{e}")
        return False


def wait_for_ttyacm0() -> bool:
    """等待 /dev/ttyACM0 设备可用"""
    print("\n等待连接...")
    time.sleep(5)
    
    print("正在检查 /dev/ttyACM0...")
    if check_ttyacm0_exists():
        print("✓ 检测到 /dev/ttyACM0！")
        return True
    
    print("未找到设备，再等待 5 秒...")
    time.sleep(5)
    
    print("再次检查 /dev/ttyACM0...")
    if check_ttyacm0_exists():
        print("✓ 检测到 /dev/ttyACM0！")
        return True
    
    print("✗ 未找到 /dev/ttyACM0")
    return False


def switch_to_module(module_type: str) -> bool:
    """
    切换到指定的模块类型
    
    Args:
        module_type: 'agx' 表示推理模块，'lpmu' 表示应用模块
    """
    module_name = "推理模块" if module_type == "agx" else "应用模块"
    print(f"\n{'='*50}")
    print(f"正在切换到{module_name}")
    print('='*50)
    
    # 等待设备
    if not wait_for_ttyacm0():
        print(f"\n错误：无法连接到 /dev/ttyACM0")
        return False
    
    print("\n正在连接串口控制台...")
    
    try:
        # 启动 tio 会话
        child = pexpect.spawn('tio /dev/ttyACM0', encoding='utf-8', timeout=10)
        
        # 等待连接消息
        index = child.expect(['Connected to /dev/ttyACM0', pexpect.TIMEOUT, pexpect.EOF])
        
        if index != 0:
            print("\n错误：连接串口控制台失败")
            child.close()
            return False
        
        print("✓ 已连接到 /dev/ttyACM0")
        print("\n按回车键开始切换...")
        input()
        
        # 发送初始回车
        child.sendline('')
        time.sleep(2)
        
        # 发送 usbmux 命令
        print(f"正在执行：usbmux {module_type}")
        child.sendline(f'usbmux {module_type}')
        time.sleep(2)
        
        # 如果是推理模块，执行 agx recovery
        if module_type == 'agx':
            print("等待 3 秒...")
            time.sleep(3)
            print("正在执行：agx recovery")
            child.sendline('agx recovery')
            
            # 等待设备恢复完成的日志
            print("等待设备恢复完成...")
            child.timeout = 60  # 设置超时时间为60秒
            index = child.expect(['.*设备强制恢复模式完成.*', pexpect.TIMEOUT, pexpect.EOF])
            
            if index == 0:
                print("✓ 检测到恢复完成日志")
                time.sleep(1)
            elif index == 1:
                print("\n警告：等待恢复完成超时，继续保存配置")
            else:
                print("\n警告：连接意外断开")
                child.close()
                return False
        
        # 保存配置
        print("正在保存配置...")
        child.sendline('usbmux save')
        time.sleep(2)
        
        # 关闭连接
        child.sendcontrol('t')
        child.send('q')
        child.close()
        
        print("\n" + "="*50)
        print(f"✓ 成功切换到{module_name}！")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"\n切换过程中发生错误：{e}")
        return False


def agx_recovery() -> bool:
    """
    推理模组重置功能
    """
    print(f"\n{'='*50}")
    print("推理模组重置")
    print('='*50)
    
    # 等待设备
    if not wait_for_ttyacm0():
        print(f"\n错误：无法连接到 /dev/ttyACM0")
        return False
    
    print("\n正在连接串口控制台...")
    
    try:
        # 启动 tio 会话
        child = pexpect.spawn('tio /dev/ttyACM0', encoding='utf-8', timeout=10)
        
        # 等待连接消息
        index = child.expect(['Connected to /dev/ttyACM0', pexpect.TIMEOUT, pexpect.EOF])
        
        if index != 0:
            print("\n错误：连接串口控制台失败")
            child.close()
            return False
        
        print("✓ 已连接到 /dev/ttyACM0")
        print("\n按回车键开始重置...")
        input()
        
        # 发送初始回车
        child.sendline('')
        time.sleep(2)
        
        # 执行 agx recovery
        print("正在执行：agx recovery")
        child.sendline('agx recovery')
        
        # 等待设备恢复完成的日志
        print("等待设备恢复完成...")
        child.timeout = 60  # 设置超时时间为60秒
        index = child.expect(['.*设备强制恢复模式完成.*', pexpect.TIMEOUT, pexpect.EOF])
        
        if index == 0:
            print("✓ 检测到恢复完成日志")
            time.sleep(1)
            
            # 关闭连接
            child.sendcontrol('t')
            child.send('q')
            child.close()
            
            print("\n" + "="*50)
            print("✓ 推理模组重置完成！")
            print("="*50)
            return True
        elif index == 1:
            print("\n错误：等待恢复完成超时")
            child.sendcontrol('t')
            child.send('q')
            child.close()
            return False
        else:
            print("\n错误：连接意外断开")
            child.close()
            return False
        
    except Exception as e:
        print(f"\n重置过程中发生错误：{e}")
        return False


def main():
    """主函数"""
    print_logo()
    
    while True:
        print("\n请选择操作：")
        print("  1. 切换到推理模块")
        print("  2. 切换到应用模块")
        print("  3. 推理模组重置")
        print("  4. 退出")
        print()
        
        choice = input("请输入您的选择（1-4）：").strip()
        
        if choice == '1':
            switch_to_module('agx')
        elif choice == '2':
            switch_to_module('lpmu')
        elif choice == '3':
            agx_recovery()
        elif choice == '4':
            print("\n正在退出...")
            break
        else:
            print("\n无效的选择，请重试。")
        
        print("\n按回车键继续...")
        input()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()
        print("\n按回车键退出...")
        input()
        sys.exit(1)

