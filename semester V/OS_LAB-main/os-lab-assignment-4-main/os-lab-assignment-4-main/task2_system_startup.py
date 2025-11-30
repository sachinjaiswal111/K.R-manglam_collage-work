import time
import logging
import threading
import random
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_startup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SystemStartup')

class SystemProcess:
    def __init__(self, pid, name, priority=1, dependencies=None):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.dependencies = dependencies or []
        self.status = "CREATED"
        self.start_time = None
        self.end_time = None
        
    def execute(self):
        self.status = "RUNNING"
        self.start_time = datetime.now()
        logger.info(f"Process {self.pid}: {self.name} - STARTED")
        
        # Simulate process execution time
        execution_time = random.uniform(0.5, 3.0)
        time.sleep(execution_time)
        
        self.status = "COMPLETED"
        self.end_time = datetime.now()
        logger.info(f"Process {self.pid}: {self.name} - COMPLETED (Duration: {execution_time:.2f}s)")
        
        return execution_time

class ProcessScheduler:
    def __init__(self):
        self.processes = []
        self.completed_processes = []
        self.failed_processes = []
        
    def add_process(self, process):
        self.processes.append(process)
        
    def can_start_process(self, process):
        """Check if all dependencies are satisfied"""
        for dep_pid in process.dependencies:
            dep_process = next((p for p in self.completed_processes if p.pid == dep_pid), None)
            if not dep_process:
                return False
        return True
    
    def schedule_processes(self):
        """Schedule processes based on dependencies and priority"""
        logger.info("Starting process scheduling...")
        
        remaining_processes = self.processes.copy()
        max_attempts = len(self.processes) * 2  # Prevent infinite loops
        attempts = 0
        
        while remaining_processes and attempts < max_attempts:
            attempts += 1
            ready_processes = []
            
            # Find processes that can start (dependencies satisfied)
            for process in remaining_processes:
                if self.can_start_process(process):
                    ready_processes.append(process)
            
            if not ready_processes:
                logger.warning("No processes ready to start - possible dependency deadlock")
                break
            
            # Sort by priority (higher priority first)
            ready_processes.sort(key=lambda x: x.priority, reverse=True)
            
            # Execute ready processes
            for process in ready_processes[:]:  # Use copy for safe removal
                try:
                    # Start process in a separate thread
                    thread = threading.Thread(target=process.execute)
                    thread.start()
                    thread.join()  # Wait for completion (for simulation purposes)
                    
                    self.completed_processes.append(process)
                    remaining_processes.remove(process)
                    
                except Exception as e:
                    logger.error(f"Process {process.pid} failed: {str(e)}")
                    process.status = "FAILED"
                    self.failed_processes.append(process)
                    remaining_processes.remove(process)
        
        # Report any processes that couldn't start
        if remaining_processes:
            logger.error(f"{len(remaining_processes)} processes could not be started:")
            for process in remaining_processes:
                logger.error(f"  - {process.name} (PID: {process.pid})")

def initialize_system_processes():
    """Create and return system processes with dependencies"""
    processes = [
        # Core system processes (no dependencies)
        SystemProcess(1, "Kernel Initialization", priority=10),
        SystemProcess(2, "Memory Management", priority=9),
        SystemProcess(3, "Interrupt Handler Setup", priority=9),
        
        # Hardware detection (depends on kernel)
        SystemProcess(4, "CPU Detection", priority=8, dependencies=[1]),
        SystemProcess(5, "Memory Detection", priority=8, dependencies=[2]),
        SystemProcess(6, "Device Enumeration", priority=7, dependencies=[1]),
        
        # Driver loading (depends on hardware detection)
        SystemProcess(7, "Storage Driver", priority=6, dependencies=[6]),
        SystemProcess(8, "Network Driver", priority=6, dependencies=[6]),
        SystemProcess(9, "Display Driver", priority=6, dependencies=[6]),
        
        # System services (depends on drivers)
        SystemProcess(10, "File System Mount", priority=5, dependencies=[7]),
        SystemProcess(11, "Network Stack", priority=5, dependencies=[8]),
        
        # User space initialization
        SystemProcess(12, "Init Process", priority=4, dependencies=[10]),
        SystemProcess(13, "Service Manager", priority=4, dependencies=[12]),
        SystemProcess(14, "Login Service", priority=3, dependencies=[13, 11]),
        SystemProcess(15, "GUI Interface", priority=2, dependencies=[9, 13]),
    ]
    
    return processes

def display_process_tree(processes):
    """Display processes in a tree-like structure showing dependencies"""
    print("\n" + "="*60)
    print("SYSTEM PROCESS DEPENDENCY TREE")
    print("="*60)
    
    for process in processes:
        status_symbol = {
            "CREATED": "⏳",
            "RUNNING": "🔄", 
            "COMPLETED": "✅",
            "FAILED": "❌"
        }.get(process.status, "❓")
        
        deps_str = f" [Deps: {process.dependencies}]" if process.dependencies else ""
        print(f"{status_symbol} PID {process.pid:2d}: {process.name:<25} "
              f"[Priority: {process.priority}] {deps_str}")

def system_startup_simulation():
    """Main system startup simulation function"""
    print("\n" + "="*70)
    print("SYSTEM STARTUP AND LOGGING SIMULATION")
    print("="*70)
    
    try:
        # Initialize logging
        logger.info("SYSTEM STARTUP SEQUENCE INITIATED")
        
        # Create process scheduler
        scheduler = ProcessScheduler()
        
        # Initialize system processes
        processes = initialize_system_processes()
        
        # Add processes to scheduler
        for process in processes:
            scheduler.add_process(process)
        
        # Display process tree before execution
        print("\nCreating and starting system processes...")
        display_process_tree(processes)
        
        # Start process scheduling
        print(f"\nStarting execution of {len(processes)} system processes...")
        start_time = time.time()
        
        scheduler.schedule_processes()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Display results
        print("\n" + "="*70)
        print("SYSTEM STARTUP COMPLETED")
        print("="*70)
        
        print(f"\nStartup Summary:")
        print(f"✅ Completed: {len(scheduler.completed_processes)} processes")
        print(f"❌ Failed: {len(scheduler.failed_processes)} processes")
        print(f"⏱️  Total startup time: {total_time:.2f} seconds")
        
        # Display final status
        print(f"\nFinal Process Status:")
        display_process_tree(processes)
        
        # Generate startup report
        generate_startup_report(scheduler, total_time)
        
        logger.info(f"System startup completed in {total_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        logger.error(f"System startup failed: {str(e)}")
        print(f"\n❌ System startup failed with error: {str(e)}")
        return False

def generate_startup_report(scheduler, total_time):
    """Generate a detailed startup report"""
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n" + "="*70)
    print("DETAILED STARTUP REPORT")
    print("="*70)
    print(f"Report Generated: {report_time}")
    print(f"Total Startup Time: {total_time:.2f} seconds")
    print(f"Success Rate: {(len(scheduler.completed_processes)/len(scheduler.processes))*100:.1f}%")
    
    print(f"\nProcess Execution Timeline:")
    completed_sorted = sorted(scheduler.completed_processes, 
                            key=lambda x: x.start_time if x.start_time else datetime.now())
    
    for process in completed_sorted:
        if process.start_time and process.end_time:
            duration = (process.end_time - process.start_time).total_seconds()
            start_str = process.start_time.strftime("%H:%M:%S")
            print(f"  {process.pid:2d}. {process.name:<25} | {start_str} | {duration:5.2f}s")
    
    if scheduler.failed_processes:
        print(f"\nFailed Processes:")
        for process in scheduler.failed_processes:
            print(f"  ❌ {process.name} (PID: {process.pid})")

if __name__ == "__main__":
    system_startup_simulation()
