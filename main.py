#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RM-01 Serial Switcher Tool
"""

import os
import sys
import subprocess
import time
import pexpect


def print_logo():
    """Display the application logo"""
    print("\n")
    print("    ██████╗ ███╗   ███╗██╗███╗   ██╗████████╗███████╗")
    print("    ██╔══██╗████╗ ████║██║████╗  ██║╚══██╔══╝██╔════╝")
    print("    ██████╔╝██╔████╔██║██║██╔██╗ ██║   ██║   █████╗  ")
    print("    ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║   ██║   ██╔══╝  ")
    print("    ██║  ██║██║ ╚═╝ ██║██║██║ ╚████║   ██║   ███████╗")
    print("    ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝")
    print("")
    print("\n" + "-"*50)
    print("RM-01 Serial Switcher Tool")
    print("-"*50)


def check_ttyacm0_exists() -> bool:
    """Check if /dev/ttyACM0 exists using tio -l"""
    try:
        result = subprocess.run(['tio', '-l'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return '/dev/ttyACM0' in result.stdout
    except Exception as e:
        print(f"Warning: Failed to check ttyACM0: {e}")
        return False


def wait_for_ttyacm0() -> bool:
    """Wait for /dev/ttyACM0 to be available"""
    print("\nWaiting for connection...")
    time.sleep(5)
    
    print("Checking for /dev/ttyACM0...")
    if check_ttyacm0_exists():
        print("✓ /dev/ttyACM0 detected!")
        return True
    
    print("Device not found, waiting another 5 seconds...")
    time.sleep(5)
    
    print("Checking for /dev/ttyACM0 again...")
    if check_ttyacm0_exists():
        print("✓ /dev/ttyACM0 detected!")
        return True
    
    print("✗ /dev/ttyACM0 not found")
    return False


def switch_to_module(module_type: str) -> bool:
    """
    Switch to specified module type
    
    Args:
        module_type: 'agx' for Inference Module or 'lpmu' for Application Module
    """
    module_name = "Inference Module" if module_type == "agx" else "Application Module"
    print(f"\n{'='*50}")
    print(f"Switching to {module_name}")
    print('='*50)
    
    # Wait for device
    if not wait_for_ttyacm0():
        print(f"\nError: Cannot connect to /dev/ttyACM0")
        return False
    
    print("\nConnecting to serial console...")
    
    try:
        # Start tio session
        child = pexpect.spawn('tio /dev/ttyACM0', encoding='utf-8', timeout=10)
        
        # Wait for connection message
        index = child.expect(['Connected to /dev/ttyACM0', pexpect.TIMEOUT, pexpect.EOF])
        
        if index != 0:
            print("\nError: Failed to connect to serial console")
            child.close()
            return False
        
        print("✓ Connected to /dev/ttyACM0")
        print("\nPress ENTER to start switching...")
        input()
        
        # Send initial enter
        child.sendline('')
        time.sleep(2)
        
        # Send usbmux command
        print(f"Executing: usbmux {module_type}")
        child.sendline(f'usbmux {module_type}')
        time.sleep(2)
        
        # Save configuration
        print("Saving configuration...")
        child.sendline('usbmux save')
        time.sleep(2)
        
        # Close the connection
        child.sendcontrol('t')
        child.send('q')
        child.close()
        
        print("\n" + "="*50)
        print(f"✓ Successfully switched to {module_name}!")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"\nError during switch: {e}")
        return False


def main():
    """Main function"""
    print_logo()
    
    while True:
        print("\nPlease select an option:")
        print("  1. Switch to Inference Module")
        print("  2. Switch to Application Module")
        print("  3. Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            switch_to_module('agx')
        elif choice == '2':
            switch_to_module('lpmu')
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice, please try again.")
        
        print("\nPress ENTER to continue...")
        input()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        print("\nPress ENTER to exit...")
        input()
        sys.exit(1)

