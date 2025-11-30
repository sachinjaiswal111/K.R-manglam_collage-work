import random
import time
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class ProcessState(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    WAITING = "WAITING"

@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 1
    remaining_time: int = 0
    start_time: int = -1
    completion_time: int = -1
    state: ProcessState = ProcessState.READY
    
    def __post_init__(self):
        self.remaining_time = self.burst_time
    
    @property
    def turnaround_time(self):
        if self.completion_time != -1:
            return self.completion_time - self.arrival_time
        return 0
    
    @property
    def waiting_time(self):
        if self.completion_time != -1:
            return self.turnaround_time - self.burst_time
        return 0

class CPUScheduler:
    def __init__(self):
        self.processes = []
        self.completed_processes = []
        self.current_time = 0
        self.gantt_chart = []
    
    def add_process(self, process: Process):
        self.processes.append(process)
    
    def generate_test_processes(self, num_processes=5):
        """Generate random test processes"""
        self.processes.clear()
        for i in range(num_processes):
            arrival = random.randint(0, 10)
            burst = random.randint(1, 10)
            priority = random.randint(1, 5)
            self.processes.append(Process(i+1, arrival, burst, priority))
    
    def fcfs(self):
        """First Come First Serve Scheduling"""
        print("\nFirst Come First Serve (FCFS) Scheduling:")
        print("-" * 50)
        
        # Sort by arrival time
        ready_queue = sorted([p for p in self.processes], key=lambda x: x.arrival_time)
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        
        for process in ready_queue:
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            
            process.start_time = self.current_time
            process.state = ProcessState.RUNNING
            
            # Execute process
            self.gantt_chart.append((process.pid, self.current_time, self.current_time + process.burst_time))
            self.current_time += process.burst_time
            
            process.completion_time = self.current_time
            process.state = ProcessState.COMPLETED
            self.completed_processes.append(process)
        
        self.print_schedule()
    
    def sjf(self):
        """Shortest Job First Scheduling (Non-preemptive)"""
        print("\nShortest Job First (SJF) Scheduling:")
        print("-" * 50)
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        remaining_processes = self.processes.copy()
        
        while remaining_processes:
            # Get processes that have arrived
            available_processes = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            
            if not available_processes:
                # No processes available, advance time
                self.current_time += 1
                continue
            
            # Select process with shortest burst time
            next_process = min(available_processes, key=lambda x: x.burst_time)
            remaining_processes.remove(next_process)
            
            next_process.start_time = self.current_time
            next_process.state = ProcessState.RUNNING
            
            # Execute process
            self.gantt_chart.append((next_process.pid, self.current_time, self.current_time + next_process.burst_time))
            self.current_time += next_process.burst_time
            
            next_process.completion_time = self.current_time
            next_process.state = ProcessState.COMPLETED
            self.completed_processes.append(next_process)
        
        self.print_schedule()
    
    def priority_scheduling(self):
        """Priority Scheduling (Non-preemptive)"""
        print("\nPriority Scheduling (Non-preemptive):")
        print("-" * 50)
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        remaining_processes = self.processes.copy()
        
        while remaining_processes:
            # Get processes that have arrived
            available_processes = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            
            if not available_processes:
                # No processes available, advance time
                self.current_time += 1
                continue
            
            # Select process with highest priority (lower number = higher priority)
            next_process = min(available_processes, key=lambda x: x.priority)
            remaining_processes.remove(next_process)
            
            next_process.start_time = self.current_time
            next_process.state = ProcessState.RUNNING
            
            # Execute process
            self.gantt_chart.append((next_process.pid, self.current_time, self.current_time + next_process.burst_time))
            self.current_time += next_process.burst_time
            
            next_process.completion_time = self.current_time
            next_process.state = ProcessState.COMPLETED
            self.completed_processes.append(next_process)
        
        self.print_schedule()
    
    def round_robin(self, time_quantum=2):
        """Round Robin Scheduling"""
        print(f"\nRound Robin Scheduling (Time Quantum: {time_quantum}):")
        print("-" * 50)
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        ready_queue = []
        remaining_processes = self.processes.copy()
        
        # Reset remaining times
        for process in remaining_processes:
            process.remaining_time = process.burst_time
        
        while remaining_processes or ready_queue:
            # Add processes that have arrived to ready queue
            new_arrivals = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            for process in new_arrivals:
                ready_queue.append(process)
                remaining_processes.remove(process)
            
            if not ready_queue:
                self.current_time += 1
                continue
            
            # Get next process from ready queue
            current_process = ready_queue.pop(0)
            
            if current_process.start_time == -1:
                current_process.start_time = self.current_time
            
            current_process.state = ProcessState.RUNNING
            
            # Execute for time quantum or remaining time
            execution_time = min(time_quantum, current_process.remaining_time)
            start_time = self.current_time
            self.current_time += execution_time
            current_process.remaining_time -= execution_time
            
            self.gantt_chart.append((current_process.pid, start_time, self.current_time))
            
            # Add new arrivals during execution
            new_arrivals = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            for process in new_arrivals:
                ready_queue.append(process)
                remaining_processes.remove(process)
            
            if current_process.remaining_time > 0:
                # Process not finished, add back to ready queue
                ready_queue.append(current_process)
                current_process.state = ProcessState.READY
            else:
                # Process completed
                current_process.completion_time = self.current_time
                current_process.state = ProcessState.COMPLETED
                self.completed_processes.append(current_process)
        
        self.print_schedule()
    
    def print_schedule(self):
        """Print scheduling results and statistics"""
        # Print Gantt Chart
        print("Gantt Chart:")
        gantt_str = ""
        for pid, start, end in self.gantt_chart:
            gantt_str += f"P{pid}[{start}-{end}] "
        print(gantt_str)
        
        # Print process table
        print("\nProcess Execution Details:")
        print("PID | Arrival | Burst | Priority | Start | Complete | Turnaround | Waiting")
        print("-" * 80)
        
        total_turnaround = 0
        total_waiting = 0
        
        for process in sorted(self.completed_processes, key=lambda x: x.pid):
            print(f"P{process.pid:2d} | {process.arrival_time:7d} | {process.burst_time:5d} | {process.priority:8d} | "
                  f"{process.start_time:5d} | {process.completion_time:8d} | {process.turnaround_time:10d} | {process.waiting_time:7d}")
            
            total_turnaround += process.turnaround_time
            total_waiting += process.waiting_time
        
        # Print averages
        num_processes = len(self.completed_processes)
        if num_processes > 0:
            print("-" * 80)
            print(f"Average Turnaround Time: {total_turnaround/num_processes:.2f}")
            print(f"Average Waiting Time: {total_waiting/num_processes:.2f}")
    
    def compare_algorithms(self):
        """Compare all scheduling algorithms"""
        print("\n" + "="*70)
        print("CPU SCHEDULING ALGORITHMS COMPARISON")
        print("="*70)
        
        # Generate test processes
        self.generate_test_processes(5)
        
        # Display test processes
        print("Test Processes:")
        print("PID | Arrival | Burst | Priority")
        print("-" * 30)
        for process in self.processes:
            print(f"P{process.pid:2d} | {process.arrival_time:7d} | {process.burst_time:5d} | {process.priority:8d}")
        
        # Run all algorithms
        original_processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in self.processes]
        
        # FCFS
        self.processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in original_processes]
        self.fcfs()
        
        # SJF
        self.processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in original_processes]
        self.sjf()
        
        # Priority
        self.processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in original_processes]
        self.priority_scheduling()
        
        # Round Robin
        self.processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in original_processes]
        self.round_robin(time_quantum=2)

def cpu_scheduling_demo():
    """Main function for CPU scheduling demonstration"""
    print("\n" + "="*70)
    print("CPU SCHEDULING ALGORITHMS DEMONSTRATION")
    print("="*70)
    
    try:
        scheduler = CPUScheduler()
        scheduler.compare_algorithms()
        
        print("\n" + "="*70)
        print("CPU SCHEDULING DEMONSTRATION COMPLETED!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\nERROR: CPU scheduling demonstration failed: {str(e)}")
        return False

if __name__ == "__main__":
    cpu_scheduling_demo()
