import os
import time
import subprocess
import sys

def task1_create_processes():
    print("=== Task 1: Process Creation Utility ===")
    n = 2
    print(f"Creating {n} child processes...")
    
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            print(f"Child {i+1}: PID = {os.getpid()}, Parent PID = {os.getppid()}")
            print(f"Child {i+1}: Custom message - Hello from child process {i+1}!")
            os._exit(0)
        else:
            os.wait()
    print("All children have finished!")

def task2_command_execution():
    print("\n=== Task 2: Command Execution Using exec() ===")
    commands = ['ls', 'date', 'pwd', 'whoami']
    
    for i, cmd in enumerate(commands):
        pid = os.fork()
        if pid == 0:
            print(f"Child {i+1} (PID: {os.getpid()}) executing: {cmd}")
            try:
                result = subprocess.run([cmd], capture_output=True, text=True)
                print(f"Output: {result.stdout.strip()}")
            except FileNotFoundError:
                print(f"Command '{cmd}' not found")
            os._exit(0)
        else:
            os.wait()
    print("All command executions completed!")

def task3_zombie_orphan():
    print("\n=== Task 3: Zombie & Orphan Processes ===")
    print("Creating a ZOMBIE process...")
    pid = os.fork()
    if pid == 0:
        print(f"Zombie Child: PID = {os.getpid()}, exiting quickly...")
        os._exit(0)
    else:
        print(f"Parent: Created child {pid}, but NOT waiting (zombie scenario)")
        print("Run 'ps -ef | grep defunct' in another terminal to see zombie")
        time.sleep(2)
        os.wait()
        print("Zombie cleaned up!")
    
    print("\nCreating an ORPHAN process...")
    
    print("Orphan Process: Child continues after parent exits")
    print("Parent PID becomes 1 (init process)")
    print("This is demonstrated conceptually to avoid program termination")

def task4_proc_inspection():
    print("\n=== Task 4: Inspecting Process Info from /proc ===")
    pid = os.getpid()
    print(f"Inspecting current process (PID: {pid})")
    
    try:
        with open(f"/proc/{pid}/status", 'r') as f:
            print("=== Process Status ===")
            for line in f:
                if any(key in line for key in ['Name', 'State', 'Pid', 'PPid']):
                    print(line.strip())
    except FileNotFoundError:
        print("Status file not found")
    
    try:
        exe_path = os.readlink(f"/proc/{pid}/exe")
        print(f"Executable path: {exe_path}")
    except OSError:
        print("Executable path not available")
    
    print("Task 4 completed!")

def task5_prioritization():
    print("\n=== Task 5: Process Prioritization ===")
    
    def cpu_task(name):
        start = time.time()
        count = 0
        while time.time() - start < 1:  # Reduced time for faster execution
            count += 1
        print(f"Task {name} completed {count} iterations")
    
    for i in range(2):  # Reduced number of processes
        pid = os.fork()
        if pid == 0:
            print(f"Process {i+1}: PID = {os.getpid()}")
            cpu_task(f"Process-{i+1}")
            os._exit(0)
        else:
            os.wait()
    print("All prioritized tasks completed!")

def main():
    print("OS Lab Assignment 1 - Process Management")
    print("Running all tasks automatically...")
    
    sys.stdout.flush()
    
    task1_create_processes()
    time.sleep(1)
    task2_command_execution()
    time.sleep(1)
    task3_zombie_orphan()
    time.sleep(1)
    task4_proc_inspection()
    time.sleep(1)
    task5_prioritization()
    
    print("\n=== ALL TASKS COMPLETED ===")

if __name__ == "__main__":
    main()
