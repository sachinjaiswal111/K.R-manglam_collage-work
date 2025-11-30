#!/usr/bin/env python3
"""
OS Lab Assignment 3 - Complete Solution
CPU Scheduling, File Allocation, and Memory Management
"""

import os
import sys

def main():
    print("🎓 OS LAB ASSIGNMENT 3 - COMPLETE SOLUTION")
    print("=" * 60)
    print("Course: ENCS351 Operating System")
    print("Student: Muskan Kumari")
    print("=" * 60)
    
    while True:
        print("\n📋 AVAILABLE TASKS:")
        print("1. CPU Scheduling Algorithms")
        print("2. Sequential File Allocation") 
        print("3. Indexed File Allocation")
        print("4. Memory Allocation Strategies")
        print("5. MFT & MVT Memory Management")
        print("6. Run All Tasks")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            os.system('python task1_cpu_scheduling.py')
        elif choice == '2':
            os.system('python task2_sequential_file.py')
        elif choice == '3':
            os.system('python task3_indexed_file.py')
        elif choice == '4':
            os.system('python task4_memory_allocation.py')
        elif choice == '5':
            os.system('python task5_mft_mvt.py')
        elif choice == '6':
            print("\n🚀 RUNNING ALL TASKS...")
            tasks = [
                'task1_cpu_scheduling.py',
                'task2_sequential_file.py', 
                'task3_indexed_file.py',
                'task4_memory_allocation.py',
                'task5_mft_mvt.py'
            ]
            for task in tasks:
                print(f"\n{'='*50}")
                print(f"RUNNING: {task}")
                print(f"{'='*50}")
                os.system(f'python {task}')
        elif choice == '7':
            print("👋 Thank you for using OS Lab Assignment 3!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-7.")

if __name__ == "__main__":
    main()
