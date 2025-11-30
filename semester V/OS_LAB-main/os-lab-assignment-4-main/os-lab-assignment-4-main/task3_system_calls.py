import os
import time
import threading
import multiprocessing
import queue
import random
from datetime import datetime

def worker_process(process_id, iterations=3):
    """Worker function for multiprocessing demo - defined at module level"""
    for i in range(iterations):
        time.sleep(0.5)  # Simulate work
        print(f"   Process {process_id}: Iteration {i+1}/{iterations} "
              f"(PID: {os.getpid()})")
    return f"Process {process_id} completed"

def system_calls_demo():
    """Demonstrate various system calls and Inter-Process Communication"""
    print("\n" + "="*70)
    print("SYSTEM CALLS AND IPC DEMONSTRATION")
    print("="*70)
    
    print("This task demonstrates:")
    print("1. File System Operations (Create, Read, Write, Delete)")
    print("2. Process Management (Multiprocessing)")
    print("3. Threading and Synchronization")
    print("4. Inter-Process Communication (Pipes, Queues)")
    print("5. Shared Memory and Locks")
    print("="*70)
    
    try:
        # 1. File System Operations
        file_operations_demo()
        
        # 2. Process Management
        process_management_demo()
        
        # 3. Threading and Synchronization
        threading_demo()
        
        # 4. IPC Mechanisms
        ipc_demo()
        
        # 5. Shared Memory with Locks
        shared_memory_demo()
        
        print("\n" + "="*70)
        print("ALL SYSTEM CALLS AND IPC OPERATIONS COMPLETED SUCCESSFULLY!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\nERROR: System calls demonstration failed: {str(e)}")
        return False

def file_operations_demo():
    """Demonstrate file system operations"""
    print("\n" + "-"*50)
    print("FILE SYSTEM OPERATIONS")
    print("-"*50)
    
    filename = "demo_file.txt"
    
    try:
        # Create and write to file
        print("1. Creating and writing to file...")
        with open(filename, 'w') as f:
            f.write("Hello, this is a demo file!\n")
            f.write("Created at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("Line 3: File operations demonstration\n")
            f.write("Line 4: System calls in action\n")
            f.write("Line 5: End of demo content\n")
        print(f"   File '{filename}' created successfully")
        
        # Read from file
        print("2. Reading from file...")
        with open(filename, 'r') as f:
            content = f.read()
            print("   File content:")
            for i, line in enumerate(content.splitlines(), 1):
                print(f"   Line {i}: {line}")
        
        # File information
        print("3. Getting file information...")
        stat_info = os.stat(filename)
        print(f"   File size: {stat_info.st_size} bytes")
        print(f"   Created: {datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Modified: {datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Append to file
        print("4. Appending to file...")
        with open(filename, 'a') as f:
            f.write("Appended line: System calls demo completed!\n")
        print("   Content appended successfully")
        
        # Read updated content
        print("5. Reading updated content...")
        with open(filename, 'r') as f:
            lines = f.readlines()
            print(f"   Total lines: {len(lines)}")
        
        # Delete file
        print("6. Cleaning up - deleting file...")
        os.remove(filename)
        print(f"   File '{filename}' deleted successfully")
        
    except Exception as e:
        print(f"   File operation error: {str(e)}")
        # Clean up if file exists
        if os.path.exists(filename):
            os.remove(filename)

def process_management_demo():
    """Demonstrate process creation and management"""
    print("\n" + "-"*50)
    print("PROCESS MANAGEMENT")
    print("-"*50)
    
    print("1. Creating multiple processes...")
    
    # Using multiprocessing
    processes = []
    
    # Create and start processes - using the module-level function
    for i in range(3):
        p = multiprocessing.Process(
            target=worker_process,  # Use module-level function instead of lambda
            args=(i + 1,)  # Pass process ID as argument
        )
        processes.append(p)
        p.start()
        print(f"   Started process {i+1} with PID: {p.pid}")
    
    # Wait for all processes to complete
    print("2. Waiting for processes to complete...")
    for i, p in enumerate(processes):
        p.join()
        print(f"   Process {i+1} finished")
    
    print("3. All processes completed successfully!")
    print(f"   Total processes created: {len(processes)}")

def threading_demo():
    """Demonstrate threading and synchronization"""
    print("\n" + "-"*50)
    print("THREADING AND SYNCHRONIZATION")
    print("-"*50)
    
    shared_counter = 0
    lock = threading.Lock()
    
    def counter_worker(thread_id, increments=5):
        """Worker function that increments shared counter"""
        nonlocal shared_counter
        for i in range(increments):
            time.sleep(0.2)  # Simulate work
            
            # Use lock to synchronize access to shared resource
            with lock:
                current_value = shared_counter
                time.sleep(0.1)  # Simulate processing time
                shared_counter = current_value + 1
                print(f"   Thread {thread_id}: Incremented counter to {shared_counter}")
    
    print("1. Creating multiple threads with shared resource...")
    print(f"   Initial counter value: {shared_counter}")
    
    threads = []
    for i in range(3):
        thread = threading.Thread(target=counter_worker, args=(i+1, 4))
        threads.append(thread)
        thread.start()
        print(f"   Started thread {i+1}")
    
    # Wait for all threads to complete
    print("2. Waiting for threads to complete...")
    for thread in threads:
        thread.join()
    
    print(f"3. All threads completed! Final counter value: {shared_counter}")
    print("   Note: Without proper synchronization, this value might be inconsistent")

def ipc_demo():
    """Demonstrate Inter-Process Communication"""
    print("\n" + "-"*50)
    print("INTER-PROCESS COMMUNICATION (IPC)")
    print("-"*50)
    
    # Message Queue demonstration
    print("1. Message Queue Demonstration")
    
    def producer(queue, producer_id, num_messages=3):
        """Producer function that sends messages"""
        for i in range(num_messages):
            message = f"Message {i+1} from Producer {producer_id}"
            queue.put(message)
            print(f"   Producer {producer_id}: Sent '{message}'")
            time.sleep(0.3)
        queue.put("END")  # Sentinel value
    
    def consumer(queue, consumer_id):
        """Consumer function that receives messages"""
        messages_received = 0
        while True:
            try:
                message = queue.get(timeout=5)
                if message == "END":
                    queue.put("END")  # Put back for other consumers
                    break
                print(f"   Consumer {consumer_id}: Received '{message}'")
                messages_received += 1
                time.sleep(0.2)
            except queue.Empty:
                break
        print(f"   Consumer {consumer_id}: Received {messages_received} messages")
    
    # Create queue and start producer/consumer
    message_queue = queue.Queue()
    
    # Start producers
    producer_threads = []
    for i in range(2):
        thread = threading.Thread(target=producer, args=(message_queue, i+1))
        producer_threads.append(thread)
        thread.start()
    
    # Start consumers
    consumer_threads = []
    for i in range(2):
        thread = threading.Thread(target=consumer, args=(message_queue, i+1))
        consumer_threads.append(thread)
        thread.start()
    
    # Wait for producers to finish
    for thread in producer_threads:
        thread.join()
    
    # Wait for consumers to finish
    for thread in consumer_threads:
        thread.join()
    
    print("2. Message queue demonstration completed!")

def shared_memory_demo():
    """Demonstrate shared memory with proper synchronization"""
    print("\n" + "-"*50)
    print("SHARED MEMORY WITH SYNCHRONIZATION")
    print("-"*50)
    
    shared_data = {"counter": 0, "log": []}
    data_lock = threading.Lock()
    barrier = threading.Barrier(3)  # Synchronize 3 threads
    
    def synchronized_worker(worker_id, operations=4):
        """Worker that uses locks and barriers for synchronization"""
        nonlocal shared_data
        
        # Phase 1: Increment operations
        for i in range(operations):
            time.sleep(0.2)
            
            with data_lock:
                shared_data["counter"] += 1
                current_value = shared_data["counter"]
                log_entry = f"Worker {worker_id} incremented to {current_value}"
                shared_data["log"].append(log_entry)
                print(f"   {log_entry}")
        
        # Wait at barrier for all threads
        print(f"   Worker {worker_id} waiting at barrier...")
        barrier.wait()
        
        # Phase 2: Read operations after synchronization
        print(f"   Worker {worker_id} passed barrier, final counter: {shared_data['counter']}")
    
    print("1. Starting synchronized workers with barrier...")
    print(f"   Initial counter: {shared_data['counter']}")
    
    workers = []
    for i in range(3):
        worker = threading.Thread(target=synchronized_worker, args=(i+1, 3))
        workers.append(worker)
        worker.start()
    
    for worker in workers:
        worker.join()
    
    print(f"2. Synchronization demo completed!")
    print(f"   Final counter value: {shared_data['counter']}")
    print(f"   Total log entries: {len(shared_data['log'])}")
    print("   All workers synchronized correctly using barrier!")

if __name__ == "__main__":
    system_calls_demo()
