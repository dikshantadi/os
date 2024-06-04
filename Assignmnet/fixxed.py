def first_fit(partitions, processes):
    allocation = [-1] * len(processes)  # Initialize allocation list
    for i in range(len(processes)):
        for j in range(len(partitions)):
            if partitions[j] >= processes[i]:
                allocation[i] = j
                partitions[j] -= processes[i]
                break
    return allocation

def best_fit(partitions, processes):
    allocation = [-1] * len(processes)  # Initialize allocation list
    for i in range(len(processes)):
        best_idx = -1
        for j in range(len(partitions)):
            if partitions[j] >= processes[i]:
                if best_idx == -1 or partitions[j] < partitions[best_idx]:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            partitions[best_idx] -= processes[i]
    return allocation

def worst_fit(partitions, processes):
    allocation = [-1] * len(processes)  # Initialize allocation list
    for i in range(len(processes)):
        worst_idx = -1
        for j in range(len(partitions)):
            if partitions[j] >= processes[i]:
                if worst_idx == -1 or partitions[j] > partitions[worst_idx]:
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            partitions[worst_idx] -= processes[i]
    return allocation

def display_memory_allocation(partitions, allocation, processes):
    for i in range(len(partitions)):
        partition_info = f"Partition {i+1} (Remaining Size: {partitions[i]} KB) -> "
        if i in allocation:
            process_index = allocation.index(i)
            partition_info += f"Process {process_index} (Size: {processes[process_index]} KB)"
        else:
            partition_info += "Free"
        print(partition_info)

# Define the partition sizes (in KB)
partition_sizes = [100, 500, 200, 300, 600]

# Define the process sizes (in KB)
process_sizes = [212, 417, 112, 426]

# Allocate processes using First Fit strategy
print("First Fit Allocation:")
partitions_copy = partition_sizes[:]
first_fit_allocation = first_fit(partitions_copy, process_sizes)
display_memory_allocation(partitions_copy, first_fit_allocation, process_sizes)

# Allocate processes using Best Fit strategy
print("\n Best Fit Allocation:")
partitions_copy = partition_sizes[:]
best_fit_allocation = best_fit(partitions_copy, process_sizes)
display_memory_allocation(partitions_copy, best_fit_allocation, process_sizes)

# Allocate processes using Worst Fit strategy
print("\nWorst Fit Allocation:")
partitions_copy = partition_sizes[:]
worst_fit_allocation = worst_fit(partitions_copy, process_sizes)
display_memory_allocation(partitions_copy, worst_fit_allocation, process_sizes)

