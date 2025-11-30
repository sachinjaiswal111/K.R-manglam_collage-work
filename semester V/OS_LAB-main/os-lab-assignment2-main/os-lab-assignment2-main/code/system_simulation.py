"""
OS Lab Assignment 2 - System Startup, Process Creation, and Termination Simulation
Student: Bhumitanwar
"""

import multiprocessing
import time
import logging
import os

def system_process(task_name):
    """
    Simulates a system process task
    """
    logging.info(f"{task_name} started - PID: {os.getpid()}")
    print(f"[SYSTEM] {task_name} started (PID: {os.getpid()})")
    
    if task_name == "Process-1":
       
        logging.info(f"{task_name} performing CPU calculations")
        result = 0
        for i in range(1000000):
            result += i * 0.1
        time.sleep(1)
        
    elif task_name == "Process-2":
       
        logging.info(f"{task_name} performing I/O operations")
        time.sleep(2)
        
    elif task_name == "Process-3":
       
        logging.info(f"{task_name} running system service")
        time.sleep(1.5)
    
    logging.info(f"{task_name} ended successfully")
    print(f"[SYSTEM] {task_name} completed")

def system_startup():
    """
    Simulates system startup sequence
    """
    print("=" * 50)
    print("SYSTEM STARTUP INITIATED")
    print("=" * 50)
    
    
    logging.info("SYSTEM: Initializing kernel components")
    print("[BOOT] Loading kernel modules...")
    time.sleep(0.5)
    
    logging.info("SYSTEM: Mounting filesystems")
    print("[BOOT] Mounting filesystems...")
    time.sleep(0.5)
    
    logging.info("SYSTEM: Starting system services")
    print("[BOOT] Starting system services...")
    time.sleep(0.5)

def system_shutdown():
    """
    Simulates system shutdown sequence
    """
    print("=" * 50)
    print("SYSTEM SHUTDOWN INITIATED")
    print("=" * 50)
    
    logging.info("SYSTEM: Stopping system services")
    print("[SHUTDOWN] Stopping system services...")
    time.sleep(0.5)
    
    logging.info("SYSTEM: Unmounting filesystems")
    print("[SHUTDOWN] Unmounting filesystems...")
    time.sleep(0.5)
    
    logging.info("SYSTEM: Shutdown complete")
    print("[SHUTDOWN] System halted")

def main():
    """
    Main function to simulate system startup, process execution, and shutdown
    """
   
    logging.basicConfig(
        filename='../outputs/process_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
   
    logging.info("=== SYSTEM BOOT SEQUENCE STARTED ===")
    
    
    system_startup()
    
    processes = []
    process_names = ['Process-1', 'Process-2', 'Process-3']
    
    print("\n[SYSTEM] Creating and starting processes...")
    logging.info("SYSTEM: Creating child processes")
    
    for name in process_names:
        process = multiprocessing.Process(
            target=system_process,
            args=(name,),
            name=name
        )
        processes.append(process)
        process.start()
        print(f"[SYSTEM] Started {name}")
        time.sleep(0.2)  
    
    print(f"\n[SYSTEM] {len(processes)} processes running concurrently")
    logging.info(f"SYSTEM: {len(processes)} processes active")
    
    print("\n[SYSTEM] Waiting for processes to complete...")
    for process in processes:
        process.join()
        print(f"[SYSTEM] {process.name} joined successfully")
    
    system_shutdown()
    logging.info("=== SYSTEM SHUTDOWN COMPLETE ===")
    
    print("\n" + "=" * 50)
    print("SIMULATION COMPLETED SUCCESSFULLY")
    print("Check '../outputs/process_log.txt' for detailed logs")
    print("=" * 50)

if __name__ == '__main__':
    main()
