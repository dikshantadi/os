from os import name


class Process:
    def __init__(self, pid, memory_required):
        self.pid = pid
        self.memory_required = memory_required
        self.status = 'waiting'

class Memory:
    def __init__(self, total_size):
        self.total_size = total_size
        self.free_size = total_size
        self.partitions = []

    def display_status(self):
        print(f"Total Memory: {self.total_size}")
        print(f"Free Memory: {self.free_size}")
        print("Partitions:")
        for i, partition in enumerate(self.partitions):
            if partition is None:
                print(f"Partition {i}: Free")
            else:
                print(f"Partition {i}: Process {partition['process'].pid}, Memory Required: {partition['memory_required']}")

class FixedSizePartitioning(Memory):
    def __init__(self, total_size, partition_size):
        super().__init__(total_size)
        self.partition_size = partition_size
        self.partitions = [None] * (total_size // partition_size)

    def allocate(self, process, strategy='first_fit'):
        remaining_memory = process.memory_required
        allocated_partitions = []

        while remaining_memory > 0:
            partition_found = False
            if strategy == 'first_fit':
                for i in range(len(self.partitions)):
                    if self.partitions[i] is None:
                        allocation_size = min(remaining_memory, self.partition_size)
                        self.partitions[i] = {'process': process, 'memory_required': allocation_size}
                        remaining_memory -= allocation_size
                        self.free_size -= allocation_size
                        allocated_partitions.append(i)
                        partition_found = True
                        if remaining_memory <= 0:
                            break
            # Add best_fit and worst_fit handling as needed
            
            if not partition_found:
                # Rollback allocation if we can't fully allocate the process
                for index in allocated_partitions:
                    self.free_size += self.partitions[index]['memory_required']
                    self.partitions[index] = None
                return False

        process.status = 'allocated'
        return True

    def deallocate(self, pid):
        for i in range(len(self.partitions)):
            if self.partitions[i] is not None and self.partitions[i]['process'].pid == pid:
                self.free_size += self.partitions[i]['memory_required']
                self.partitions[i] = None
        return True

class UnequalSizePartitioning(Memory):
    def __init__(self, total_size, partition_sizes):
        super().__init__(total_size)
        self.partition_sizes = partition_sizes
        self.partitions = [None] * len(partition_sizes)

    def allocate(self, process, strategy='best_fit'):
        remaining_memory = process.memory_required
        allocated_partitions = []

        while remaining_memory > 0:
            best_fit_index = -1
            min_diff = float('inf')
            for i in range(len(self.partitions)):
                if self.partitions[i] is None and self.partition_sizes[i] >= remaining_memory:
                    diff = self.partition_sizes[i] - remaining_memory
                    if diff < min_diff:
                        best_fit_index = i
                        min_diff = diff

            if best_fit_index == -1:
                # Cannot find a suitable partition for the remaining memory
                for index in allocated_partitions:
                    self.free_size += self.partitions[index]['memory_required']
                    self.partitions[index] = None
                return False

            allocation_size = min(remaining_memory, self.partition_sizes[best_fit_index])
            self.partitions[best_fit_index] = {'process': process, 'memory_required': allocation_size}
            remaining_memory -= allocation_size
            self.free_size -= allocation_size
            allocated_partitions.append(best_fit_index)

        process.status = 'allocated'
        return True

    def deallocate(self, pid):
        for i in range(len(self.partitions)):
            if self.partitions[i] is not None and self.partitions[i]['process'].pid == pid:
                self.free_size += self.partitions[i]['memory_required']
                self.partitions[i] = None
        return True

class DynamicMemoryAllocation(Memory):
    def __init__(self, total_size):
        super().__init__(total_size)
        self.free_blocks = [(0, total_size)]

    def allocate(self, process, strategy='first_fit'):
        remaining_memory = process.memory_required
        allocated_blocks = []

        while remaining_memory > 0:
            if strategy == 'first_fit':
                for i, (start, size) in enumerate(self.free_blocks):
                    if size >= remaining_memory:
                        allocation_size = min(remaining_memory, size)
                        self.free_blocks[i] = (start + allocation_size, size - allocation_size)
                        if self.free_blocks[i][1] == 0:
                            del self.free_blocks[i]
                        allocated_blocks.append((start, allocation_size))
                        remaining_memory -= allocation_size
                        break
            # Add best_fit and worst_fit handling as needed

            if remaining_memory > 0:
                # Rollback allocation if we can't fully allocate the process
                for (start, size) in allocated_blocks:
                    self.free_blocks.append((start, size))
                self.merge_free_blocks()
                return False

        self.partitions.append({'process': process, 'blocks': allocated_blocks})
        self.free_size -= process.memory_required
        process.status = 'allocated'
        return True

    def deallocate(self, pid):
        for i, partition in enumerate(self.partitions):
            if partition['process'].pid == pid:
                for (start, size) in partition['blocks']:
                    self.free_blocks.append((start, size))
                self.partitions.pop(i)
                self.free_size += partition['process'].memory_required
                self.merge_free_blocks()
                return True
        return False

    def merge_free_blocks(self):
        self.free_blocks.sort()
        merged_blocks = []
        for block in self.free_blocks:
            if not merged_blocks or merged_blocks[-1][0] + merged_blocks[-1][1] != block[0]:
                merged_blocks.append(block)
            else:
                merged_blocks[-1] = (merged_blocks[-1][0], merged_blocks[-1][1] + block[1])
        self.free_blocks = merged_blocks

class BuddySystem(Memory):
    def __init__(self, total_size):
        super().__init__(total_size)
        self.buddy_tree = {}  # Placeholder for buddy system structure

    def allocate(self, process):
        # Placeholder for buddy system allocation logic
        pass

    def deallocate(self, pid):
        # Placeholder for buddy system deallocation logic
        pass

class Paging(Memory):
    def __init__(self, total_size, page_size):
        super().__init__(total_size)
        self.page_size = page_size
        self.frames = [None] * (total_size // page_size)
        self.page_table = {}

    def allocate(self, process):
        num_pages = -(-process.memory_required // self.page_size)  # Ceil division
        allocated_frames = []
        for i in range(len(self.frames)):
            if self.frames[i] is None:
                allocated_frames.append(i)
                if len(allocated_frames) == num_pages:
                    break
        if len(allocated_frames) == num_pages:
            for frame in allocated_frames:
                self.frames[frame] = process
            self.page_table[process.pid] = allocated_frames
            process.status = 'allocated'
            self.free_size -= num_pages * self.page_size
            return True
        return False

    def deallocate(self, pid):
        if pid in self.page_table:
            frames = self.page_table.pop(pid)
            for frame in frames:
                self.frames[frame] = None
            self.free_size += len(frames) * self.page_size
            return True
        return False

def main():
    memory = None

    while True:
        print("\nSelect memory management technique:")
        print("1. Fixed-sized Memory Partitioning")
        print("2. Unequal-sized Fixed Partitioning")
        print("3. Dynamic Memory Allocation")
        print("4. Buddy System")
        print("5. Paging")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            total_size = int(input("Enter total memory size: "))
            partition_size = int(input("Enter partition size: "))
            memory = FixedSizePartitioning(total_size, partition_size)
        elif choice == 2:
            total_size = int(input("Enter total memory size: "))
            partition_sizes = list(map(int, input("Enter partition sizes (comma-separated): ").split(',')))
            memory = UnequalSizePartitioning(total_size, partition_sizes)
        elif choice == 3:
            total_size = int(input("Enter total memory size: "))
            memory = DynamicMemoryAllocation(total_size)
        elif choice == 4:
            total_size = int(input("Enter total memory size: "))
            memory = BuddySystem(total_size)
        elif choice == 5:
            total_size = int(input("Enter total memory size: "))
            page_size = int(input("Enter page size: "))
            memory = Paging(total_size, page_size)
        else:
            print("Invalid choice!")
            continue

        while True:
            print("\nMemory Management Menu:")
            print("1. Add Process")
            print("2. Remove Process")
            print("3. Display Memory Status")
            print("4. Change Memory Management Technique")
            print("5. Exit")
            action = int(input("Enter your choice: "))

            if action == 1:
                pid = input("Enter process ID: ")
                memory_required = int(input("Enter memory required: "))
                process = Process(pid, memory_required)
                strategy = input("Enter allocation strategy (first_fit, best_fit, worst_fit): ")
                if not memory.allocate(process, strategy):
                    print("Allocation failed!")
                else:
                    print("Process allocated successfully.")
            elif action == 2:
                pid = input("Enter process ID to remove: ")
                if not memory.deallocate(pid):
                    print("Deallocation failed!")
                else:
                    print("Process deallocated successfully.")
            elif action == 3:
                memory.display_status()
            elif action == 4:
                break
            elif action == 5:
                return
            else:
                print("Invalid choice!")

if name == "main":
    main()