import platform
import socket
import os
import sys
import time
from datetime import datetime

def vm_detection_system_info():
    """Detect virtual machine environment and display system information"""
    print("\n" + "="*70)
    print("VIRTUAL MACHINE DETECTION AND SYSTEM INFORMATION")
    print("="*70)
    
    try:
        # System Information
        print_system_information()
        
        # Virtual Machine Detection
        print_vm_detection()
        
        # Hardware Information
        print_hardware_info()
        
        # Network Information
        print_network_info()
        
        # Process Information (Basic)
        print_process_info_basic()
        
        print("\n" + "="*70)
        print("SYSTEM INFORMATION COLLECTION COMPLETED!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\nERROR: System information collection failed: {str(e)}")
        return False

def print_system_information():
    """Display basic system information"""
    print("\n" + "-"*50)
    print("BASIC SYSTEM INFORMATION")
    print("-"*50)
    
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Processor: {platform.processor()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Platform: {platform.platform()}")

def print_vm_detection():
    """Detect if running in virtual machine"""
    print("\n" + "-"*50)
    print("VIRTUAL MACHINE DETECTION")
    print("-"*50)
    
    vm_indicators = {
        "System Check": check_system_vm(),
        "Process Check": check_processes_basic(),
        "MAC Address Check": check_mac_basic(),
        "Hardware Check": check_hardware_basic(),
        "Platform Check": check_platform_vm()
    }
    
    vm_score = 0
    total_checks = len(vm_indicators)
    
    print("Running VM detection checks...")
    for check_name, result in vm_indicators.items():
        status = "DETECTED" if result else "Not detected"
        symbol = "!" if result else " "
        print(f"  [{symbol}] {check_name}: {status}")
        if result:
            vm_score += 1
    
    # Determine VM likelihood
    likelihood = "UNKNOWN"
    if vm_score == 0:
        likelihood = "LOW - Probably physical machine"
    elif vm_score <= 2:
        likelihood = "MEDIUM - Possible VM"
    else:
        likelihood = "HIGH - Likely virtual machine"
    
    print(f"\nVM Detection Summary:")
    print(f"  Indicators detected: {vm_score}/{total_checks}")
    print(f"  Likelihood: {likelihood}")

def check_system_vm():
    """Check system information for VM indicators"""
    try:
        system_info = platform.system().lower() + " " + platform.version().lower()
        vm_keywords = ['hyperv', 'vmware', 'virtual', 'kvm', 'qemu', 'xen', 'vbox']
        return any(keyword in system_info for keyword in vm_keywords)
    except:
        return False

def check_processes_basic():
    """Basic process check for VM indicators"""
    try:
        # Check for common VM processes in system info
        system_info = str(platform.uname()).lower()
        vm_processes = ['vmware', 'virtual', 'vbox', 'qemu']
        return any(proc in system_info for proc in vm_processes)
    except:
        return False

def check_mac_basic():
    """Basic MAC address check"""
    try:
        # This is a simplified check
        hostname = socket.gethostname()
        # Just check if hostname contains common VM patterns
        vm_patterns = ['vm', 'virtual', 'docker', 'container']
        return any(pattern in hostname.lower() for pattern in vm_patterns)
    except:
        return False

def check_hardware_basic():
    """Basic hardware check for VM indicators"""
    try:
        processor_info = platform.processor().lower()
        vm_hardware = ['hyperv', 'vmware', 'virtual', 'qemu']
        return any(hw in processor_info for hw in vm_hardware)
    except:
        return False

def check_platform_vm():
    """Check platform for VM indicators"""
    try:
        platform_info = platform.platform().lower()
        vm_platforms = ['microsoft', 'cloud', 'aws', 'azure', 'gcp']
        return any(platform in platform_info for platform in vm_platforms)
    except:
        return False

def print_hardware_info():
    """Display hardware information without psutil"""
    print("\n" + "-"*50)
    print("HARDWARE INFORMATION")
    print("-"*50)
    
    print("CPU Information:")
    print(f"  Architecture: {platform.architecture()[0]}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")
    
    print("\nMemory Information:")
    print("  Note: Detailed memory info requires 'psutil' module")
    print("  Install with: pip install psutil")
    
    print("\nDisk Information:")
    print("  Current drive info:")
    try:
        # Simple disk space check that works on both Windows and Linux
        if platform.system() == 'Windows':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p("C:\\"), 
                None, 
                ctypes.byref(total_bytes), 
                ctypes.byref(free_bytes)
            )
            total_gb = total_bytes.value / (1024**3)
            free_gb = free_bytes.value / (1024**3)
            used_gb = total_gb - free_gb
            print(f"  Drive C: Total: {total_gb:.2f} GB, Free: {free_gb:.2f} GB, Used: {used_gb:.2f} GB")
        else:
            # Linux/Mac disk info
            stat = os.statvfs('/')
            total = (stat.f_blocks * stat.f_frsize) / (1024**3)
            free = (stat.f_bfree * stat.f_frsize) / (1024**3)
            used = total - free
            print(f"  Root FS: Total: {total:.2f} GB, Free: {free:.2f} GB, Used: {used:.2f} GB")
    except Exception as e:
        print(f"  Disk information: Basic info available - install psutil for details")

def print_network_info():
    """Display network information"""
    print("\n" + "-"*50)
    print("NETWORK INFORMATION")
    print("-"*50)
    
    # IP Addresses
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Local IP Address: {local_ip}")
        
        # Get external IP (simplified)
        try:
            external_ip = socket.gethostbyname(socket.gethostname())
            print(f"External IP: {external_ip}")
        except:
            print("External IP: Unable to determine")
            
    except:
        print("Local IP Address: Unable to determine")
    
    print("\nNetwork Configuration:")
    print("  Note: Detailed network interface info requires 'psutil' module")

def print_process_info_basic():
    """Display basic process information without psutil"""
    print("\n" + "-"*50)
    print("PROCESS INFORMATION")
    print("-"*50)
    
    print("Current Process Info:")
    print(f"  Process ID: {os.getpid()}")
    print(f"  Parent Process ID: {os.getppid()}")
    
    # Get current user in a cross-platform way
    try:
        current_user = os.getlogin()
    except:
        try:
            current_user = os.environ.get('USER', os.environ.get('USERNAME', 'N/A'))
        except:
            current_user = 'N/A'
    
    print(f"  Current User: {current_user}")
    
    print("\nSystem Processes:")
    print("  Note: Detailed process listing requires 'psutil' module")
    print("  Install with: pip install psutil")
    
    # Basic process count using tasklist (Windows) or ps (Linux)
    try:
        if platform.system() == 'Windows':
            result = os.popen('tasklist').read()
            process_count = len([line for line in result.splitlines() if '.exe' in line])
            print(f"  Approximate running processes: {process_count}")
        else:
            result = os.popen('ps aux').read()
            process_count = len(result.splitlines()) - 1
            print(f"  Approximate running processes: {process_count}")
    except:
        print("  Process count: Unable to determine")

def print_installation_instructions():
    """Print instructions for installing psutil"""
    print("\n" + "="*70)
    print("INSTALLATION INSTRUCTIONS")
    print("="*70)
    print("For full system information capabilities, install psutil:")
    print("\nWindows Command Prompt:")
    print("  pip install psutil")
    print("\nIf you get permission errors, try:")
    print("  pip install --user psutil")
    print("\nOr use:")
    print("  python -m pip install psutil")
    print("\nAfter installation, restart this program.")
    print("="*70)

if __name__ == "__main__":
    success = vm_detection_system_info()
    if success:
        print_installation_instructions()
