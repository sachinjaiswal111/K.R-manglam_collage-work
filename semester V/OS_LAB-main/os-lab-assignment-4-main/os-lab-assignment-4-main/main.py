#!/usr/bin/env python3
"""
OS Lab Assignment 4: System Calls, VM Detection, and File System Operations
Course: ENCS351 Operating System Lab
Student: Bhumi Tanwar
"""

import os
import sys
import subprocess

def run_task(task_name, task_file):
    """Run a specific task with better error handling"""
    print(f"\n🚀 STARTING: {task_name}")
    print("=" * 50)
    
    if not os.path.exists(task_file):
        print(f"❌ ERROR: File '{task_file}' not found!")
        return False
    
    try:
        # Use subprocess for better control
        result = subprocess.run([sys.executable, task_file], 
                              capture_output=True, 
                              text=True,
                              timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {task_name} completed successfully!")
            if result.stdout.strip():
                print(f"Output:\n{result.stdout}")
        else:
            print(f"❌ {task_name} failed with error:")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {task_name} timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"💥 Error running {task_name}: {e}")
        return False
    
    print("=" * 50)
    return True

def main():
    print("🎓 OS LAB ASSIGNMENT 4 - COMPLETE SOLUTION")
    print("=" * 60)
    print("Course: ENCS351 Operating System Lab")
    print("Student: Bhumi Tanwar")
    print("=" * 60)
    
    tasks = {
        '1': ('Batch Processing Simulation', 'task1_batch_processing.py'),
        '2': ('System Startup and Logging', 'task2_system_startup.py'),
        '3': ('System Calls and IPC', 'task3_system_calls.py'),
        '4': ('VM Detection and System Info', 'task4_vm_detection.py'),
        '5': ('CPU Scheduling Algorithms', 'task5_cpu_scheduling.py')
    }
    
    while True:
        print("\n📋 AVAILABLE TASKS:")
        for key, (name, _) in tasks.items():
            print(f"{key}. {name}")
        print("6. Run All Tasks")
        print("7. Exit")
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice in tasks:
                task_name, task_file = tasks[choice]
                run_task(task_name, task_file)
            elif choice == '6':
                print("\n🚀 RUNNING ALL TASKS...")
                success_count = 0
                for key, (task_name, task_file) in tasks.items():
                    if run_task(task_name, task_file):
                        success_count += 1
                print(f"\n📊 SUMMARY: {success_count}/{len(tasks)} tasks completed successfully!")
            elif choice == '7':
                print("👋 Thank you for using OS Lab Assignment 4!")
                break
            else:
                print("❌ Invalid choice! Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Program interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"💥 An error occurred: {e}")

if __name__ == "__main__":
    main()
