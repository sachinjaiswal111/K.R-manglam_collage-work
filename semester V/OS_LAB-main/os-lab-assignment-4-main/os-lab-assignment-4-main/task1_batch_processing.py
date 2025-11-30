import time
import random
import threading
from datetime import datetime
from enum import Enum

class JobState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class BatchJob:
    def __init__(self, job_id, name, processing_time, memory_required, priority=1):
        self.job_id = job_id
        self.name = name
        self.processing_time = processing_time
        self.memory_required = memory_required
        self.priority = priority
        self.state = JobState.PENDING
        self.start_time = None
        self.end_time = None
        self.result = ""
    
    @property
    def duration(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

class BatchProcessor:
    def __init__(self, max_concurrent_jobs=2, max_memory=4096):
        self.job_queue = []
        self.completed_jobs = []
        self.failed_jobs = []
        self.max_concurrent_jobs = max_concurrent_jobs
        self.max_memory = max_memory
        self.available_memory = max_memory
        self.current_jobs = []
        self.processing = False
        self.total_jobs_processed = 0
        self.active_threads = []
        
    def add_job(self, job):
        self.job_queue.append(job)
        print(f"Added job: {job.name} (ID: {job.job_id}) to queue")
        
    def generate_sample_jobs(self, num_jobs=6):
        job_types = [
            ("Data Analysis", 1, 512),
            ("Report Generation", 1, 256),
            ("Backup Process", 2, 1024),
            ("Image Processing", 1, 768),
            ("Database Cleanup", 1, 512),
            ("File Compression", 1, 384),
            ("Network Sync", 2, 896)
        ]
        
        for i in range(num_jobs):
            name, base_time, base_memory = random.choice(job_types)
            processing_time = random.uniform(base_time * 0.5, base_time * 1.0)  # Shorter times for demo
            memory_required = random.randint(base_memory - 100, base_memory + 100)
            priority = random.randint(1, 5)
            
            job = BatchJob(
                job_id=i + 1,
                name=name,
                processing_time=processing_time,
                memory_required=memory_required,
                priority=priority
            )
            self.add_job(job)
    
    def can_start_job(self, job):
        return (len(self.current_jobs) < self.max_concurrent_jobs and 
                self.available_memory >= job.memory_required)
    
    def execute_job(self, job):
        try:
            job.state = JobState.RUNNING
            job.start_time = datetime.now()
            
            print(f"Started job: {job.name} (ID: {job.job_id}) - "
                  f"Time: {job.processing_time:.1f}s, Memory: {job.memory_required}MB")
            
            # Simulate processing time
            time.sleep(job.processing_time)
            
            # Simulate random failures (5% chance)
            if random.random() < 0.05:
                raise Exception("Simulated processing error")
            
            job.state = JobState.COMPLETED
            job.end_time = datetime.now()
            job.result = f"Successfully completed in {job.duration:.2f} seconds"
            
            self.completed_jobs.append(job)
            print(f"Completed job: {job.name} (ID: {job.job_id}) - {job.result}")
            
        except Exception as e:
            job.state = JobState.FAILED
            job.end_time = datetime.now()
            job.result = f"Failed: {str(e)}"
            self.failed_jobs.append(job)
            print(f"Failed job: {job.name} (ID: {job.job_id}) - {job.result}")
        
        finally:
            # Release resources
            if job in self.current_jobs:
                self.current_jobs.remove(job)
            self.available_memory += job.memory_required
            self.total_jobs_processed += 1
    
    def process_batch_fcfs(self):
        """Process batch using First-Come-First-Serve scheduling"""
        print("\nProcessing batch using FCFS (First-Come-First-Serve)...")
        self.processing = True
        self.active_threads = []
        
        queue_copy = self.job_queue.copy()
        
        for job in queue_copy:
            # Wait if resources not available
            while not self.can_start_job(job) and self.processing:
                time.sleep(0.1)
                # Check if any threads finished
                self.active_threads = [t for t in self.active_threads if t.is_alive()]
            
            if not self.processing:
                break
                
            # Start the job
            if job in self.job_queue:
                self.job_queue.remove(job)
            self.current_jobs.append(job)
            self.available_memory -= job.memory_required
            
            # Start job in separate thread
            thread = threading.Thread(target=self.execute_job, args=(job,))
            thread.start()
            self.active_threads.append(thread)
        
        # Wait for all threads to complete
        for thread in self.active_threads:
            thread.join()
        
        self.processing = False
    
    def process_batch_priority(self):
        """Process batch using Priority scheduling"""
        print("\nProcessing batch using Priority Scheduling...")
        self.processing = True
        self.active_threads = []
        
        # Sort jobs by priority (higher priority first)
        priority_queue = sorted(self.job_queue, key=lambda x: x.priority, reverse=True)
        
        while priority_queue and self.processing:
            # Find highest priority job that can start
            next_job = None
            for job in priority_queue:
                if self.can_start_job(job):
                    next_job = job
                    break
            
            if not next_job:
                # Check if any threads finished
                self.active_threads = [t for t in self.active_threads if t.is_alive()]
                time.sleep(0.1)
                continue
            
            # Start the job
            priority_queue.remove(next_job)
            self.job_queue.remove(next_job)
            self.current_jobs.append(next_job)
            self.available_memory -= next_job.memory_required
            
            # Start job in separate thread
            thread = threading.Thread(target=self.execute_job, args=(next_job,))
            thread.start()
            self.active_threads.append(thread)
        
        # Wait for all threads to complete
        for thread in self.active_threads:
            thread.join()
        
        self.processing = False
    
    def process_batch_shortest_first(self):
        """Process batch using Shortest Job First"""
        print("\nProcessing batch using Shortest Job First...")
        self.processing = True
        self.active_threads = []
        
        # Sort jobs by processing time
        time_queue = sorted(self.job_queue, key=lambda x: x.processing_time)
        
        while time_queue and self.processing:
            # Find shortest job that can start
            next_job = None
            for job in time_queue:
                if self.can_start_job(job):
                    next_job = job
                    break
            
            if not next_job:
                # Check if any threads finished
                self.active_threads = [t for t in self.active_threads if t.is_alive()]
                time.sleep(0.1)
                continue
            
            # Start the job
            time_queue.remove(next_job)
            self.job_queue.remove(next_job)
            self.current_jobs.append(next_job)
            self.available_memory -= next_job.memory_required
            
            # Start job in separate thread
            thread = threading.Thread(target=self.execute_job, args=(next_job,))
            thread.start()
            self.active_threads.append(thread)
        
        # Wait for all threads to complete
        for thread in self.active_threads:
            thread.join()
        
        self.processing = False
    
    def stop_processing(self):
        """Stop batch processing"""
        self.processing = False
    
    def get_statistics(self):
        """Get batch processing statistics"""
        total_jobs = len(self.completed_jobs) + len(self.failed_jobs)
        success_rate = (len(self.completed_jobs) / total_jobs * 100) if total_jobs > 0 else 0
        
        total_processing_time = sum(job.duration for job in self.completed_jobs)
        avg_processing_time = total_processing_time / len(self.completed_jobs) if self.completed_jobs else 0
        
        return {
            "total_jobs": total_jobs,
            "completed": len(self.completed_jobs),
            "failed": len(self.failed_jobs),
            "success_rate": success_rate,
            "avg_processing_time": avg_processing_time,
            "total_processing_time": total_processing_time
        }
    
    def print_statistics(self):
        """Print batch processing statistics"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("BATCH PROCESSING STATISTICS")
        print("="*60)
        print(f"Total Jobs Processed: {stats['total_jobs']}")
        print(f"Completed Successfully: {stats['completed']}")
        print(f"Failed: {stats['failed']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Average Processing Time: {stats['avg_processing_time']:.2f}s")
        print(f"Total Processing Time: {stats['total_processing_time']:.2f}s")
        
        if self.completed_jobs:
            print(f"\nCompleted Jobs:")
            for job in sorted(self.completed_jobs, key=lambda x: x.job_id):
                print(f"  {job.name} (ID: {job.job_id}) - {job.duration:.2f}s")
        
        if self.failed_jobs:
            print(f"\nFailed Jobs:")
            for job in self.failed_jobs:
                print(f"  {job.name} (ID: {job.job_id}) - {job.result}")

def batch_processing_demo():
    """Main function for batch processing demonstration"""
    print("\n" + "="*70)
    print("BATCH PROCESSING SIMULATION")
    print("="*70)
    
    try:
        # Test FCFS
        print("\n" + "="*60)
        print("TESTING: First-Come-First-Serve")
        print("="*60)
        processor1 = BatchProcessor(max_concurrent_jobs=2, max_memory=4096)
        processor1.generate_sample_jobs(4)
        
        start_time = time.time()
        processor1.process_batch_fcfs()
        end_time = time.time()
        
        processor1.print_statistics()
        print(f"Total execution time: {end_time - start_time:.2f}s")
        
        # Test Priority
        print("\n" + "="*60)
        print("TESTING: Priority Scheduling")
        print("="*60)
        processor2 = BatchProcessor(max_concurrent_jobs=2, max_memory=4096)
        processor2.generate_sample_jobs(4)
        
        start_time = time.time()
        processor2.process_batch_priority()
        end_time = time.time()
        
        processor2.print_statistics()
        print(f"Total execution time: {end_time - start_time:.2f}s")
        
        # Test Shortest Job First
        print("\n" + "="*60)
        print("TESTING: Shortest Job First")
        print("="*60)
        processor3 = BatchProcessor(max_concurrent_jobs=2, max_memory=4096)
        processor3.generate_sample_jobs(4)
        
        start_time = time.time()
        processor3.process_batch_shortest_first()
        end_time = time.time()
        
        processor3.print_statistics()
        print(f"Total execution time: {end_time - start_time:.2f}s")
        
        print("\n" + "="*70)
        print("BATCH PROCESSING DEMONSTRATION COMPLETED!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\nERROR: Batch processing demonstration failed: {str(e)}")
        return False

if __name__ == "__main__":
    batch_processing_demo()
