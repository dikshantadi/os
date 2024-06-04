class MemoryPartition:
    def __init__(self, size):
        self.size = size
        self.is_allocated = False
        self.process_id = None

class MemoryManager:
    def __init__(self, partition_sizes):
        self.partitions = [MemoryPartition(size) for size in partition_sizes]

    def first_fit(self, processes):
        for process_id, process_size in enumerate(processes):
            for partition in self.partitions:
                if not partition.is_allocated and partition.size >= process_size:
                    partition.is_allocated = True
                    partition.process_id = process_id
                    break

    def best_fit(self, processes):
        for process_id, process_size in enumerate(processes):
            best_partition = None
            for partition in self.partitions:
                if not partition.is_allocated and partition.size >= process_size:
                    if best_partition is None or partition.size < best_partition.size:
                        best_partition = partition
            if best_partition:
                best_partition.is_allocated = True
                best_partition.process_id = process_id

    def worst_fit(self, processes):
        for process_id, process_size in enumerate(processes):
            worst_partition = None
            for partition in self.partitions:
                if not partition.is_allocated and partition.size >= process_size:
                    if worst_partition is None or partition.size > worst_partition.size:
                        worst_partition = partition
            if worst_partition:
                worst_partition.is_allocated = True
                worst_partition.process_id = process_id

    def display_memory_allocation(self):
        for i, partition in enumerate(self.partitions):
            if partition.is_allocated:
                print(f"Partition {i+1} (Size: {partition.size} KB) -> Process {partition.process_id} (Allocated)")
            else:
                print(f"Partition {i+1} (Size: {partition.size} KB) -> Free")


# Define the partition sizes (in KB)
partition_sizes = [100, 500, 200, 300, 600]

# Define the process sizes (in KB)
process_sizes = [212, 417, 112, 426]

# Initialize the memory manager
memory_manager = MemoryManager(partition_sizes)

# Allocate processes using First Fit strategy
print("First Fit Allocation:")
memory_manager.first_fit(process_sizes)
memory_manager.display_memory_allocation()

# Reset the partitions for the next strategy
memory_manager = MemoryManager(partition_sizes)

# Allocate processes using Best Fit strategy
print("\nBest Fit Allocation:")
memory_manager.best_fit(process_sizes)
memory_manager.display_memory_allocation()

# Reset the partitions for the next strategy
memory_manager = MemoryManager(partition_sizes)

# Allocate processes using Worst Fit strategy
print("\nWorst Fit Allocation:")
memory_manager.worst_fit(process_sizes)
memory_manager.display_memory_allocation()
