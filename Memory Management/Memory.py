import tkinter as tk
from tkinter import messagebox

class MemoryPartition:
    def __init__(self, start, size, is_free=True, process_id=None):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process_id = process_id

class MemoryManager:
    def __init__(self, partition_sizes):
        self.partitions = []
        start_address = 0
        for size in partition_sizes:
            self.partitions.append(MemoryPartition(start_address, size))
            start_address += size

    def allocate_first_fit(self, process_id, process_size):
        for partition in self.partitions:
            if partition.is_free and partition.size >= process_size:
                partition.is_free = False
                partition.process_id = process_id
                return True
        return False

    def allocate_best_fit(self, process_id, process_size):
        best_fit_partition = None
        best_fit_size = float('inf')

        for partition in self.partitions:
            if partition.is_free and partition.size >= process_size and partition.size < best_fit_size:
                best_fit_partition = partition
                best_fit_size = partition.size

        if best_fit_partition:
            best_fit_partition.is_free = False
            best_fit_partition.process_id = process_id
            return True
        return False

    def allocate_worst_fit(self, process_id, process_size):
        worst_fit_partition = None
        worst_fit_size = -1

        for partition in self.partitions:
            if partition.is_free and partition.size >= process_size and partition.size > worst_fit_size:
                worst_fit_partition = partition
                worst_fit_size = partition.size

        if worst_fit_partition:
            worst_fit_partition.is_free = False
            worst_fit_partition.process_id = process_id
            return True
        return False

    def deallocate(self, process_id):
        for partition in self.partitions:
            if partition.process_id == process_id:
                partition.is_free = True
                partition.process_id = None

    def get_memory_status(self):
        status = []
        for i, partition in enumerate(self.partitions):
            status.append(f"Partition {i} ({partition.start}-{partition.start + partition.size} KB): {'Free' if partition.is_free else f'Occupied by Process {partition.process_id}'}")
        return status

class DynamicMemoryManager:
    def __init__(self, total_memory_size):
        self.total_memory_size = total_memory_size
        self.blocks = [MemoryPartition(0, total_memory_size)]

    def allocate_first_fit(self, process_id, process_size):
        for block in self.blocks:
            if block.is_free and block.size >= process_size:
                self._split_block(block, process_id, process_size)
                return True
        return False

    def allocate_best_fit(self, process_id, process_size):
        best_fit_block = None
        best_fit_size = float('inf')

        for block in self.blocks:
            if block.is_free and block.size >= process_size and block.size < best_fit_size:
                best_fit_block = block
                best_fit_size = block.size

        if best_fit_block:
            self._split_block(best_fit_block, process_id, process_size)
            return True
        return False

    def allocate_worst_fit(self, process_id, process_size):
        worst_fit_block = None
        worst_fit_size = -1

        for block in self.blocks:
            if block.is_free and block.size >= process_size and block.size > worst_fit_size:
                worst_fit_block = block
                worst_fit_size = block.size

        if worst_fit_block:
            self._split_block(worst_fit_block, process_id, process_size)
            return True
        return False

    def _split_block(self, block, process_id, process_size):
        if block.size > process_size:
            new_block = MemoryPartition(block.start + process_size, block.size - process_size)
            self.blocks.insert(self.blocks.index(block) + 1, new_block)
        block.size = process_size
        block.is_free = False
        block.process_id = process_id

    def deallocate(self, process_id):
        for block in self.blocks:
            if block.process_id == process_id:
                block.is_free = True
                block.process_id = None
        self._merge_free_blocks()

    def _merge_free_blocks(self):
        merged_blocks = []
        previous_block = None

        for block in self.blocks:
            if previous_block and previous_block.is_free and block.is_free:
                previous_block.size += block.size
            else:
                merged_blocks.append(block)
                previous_block = block

        self.blocks = merged_blocks

    def get_memory_status(self):
        status = []
        for i, block in enumerate(self.blocks):
            status.append(f"Block {i} ({block.start}-{block.start + block.size} KB): {'Free' if block.is_free else f'Occupied by Process {block.process_id}'}")
        return status

class BuddyMemoryManager:
    def __init__(self, total_memory_size):
        self.total_memory_size = total_memory_size
        self.blocks = [MemoryPartition(0, total_memory_size)]
        self.min_block_size = 1  # Define the minimum block size for the buddy system

    def allocate_memory(self, process_id, process_size):
        block = self._find_suitable_block(process_size)
        if not block:
            return False
        self._split_block(block, process_id, process_size)
        return True

    def _find_suitable_block(self, process_size):
        for block in self.blocks:
            if block.is_free and block.size >= process_size:
                return block
        return None

    def _split_block(self, block, process_id, process_size):
        while block.size // 2 >= process_size and block.size // 2 >= self.min_block_size:
            new_block = MemoryPartition(block.start + block.size // 2, block.size // 2)
            block.size //= 2
            self.blocks.insert(self.blocks.index(block) + 1, new_block)
        block.is_free = False
        block.process_id = process_id

    def deallocate_memory(self, process_id):
        for block in self.blocks:
            if block.process_id == process_id:
                block.is_free = True
                block.process_id = None
        self._merge_free_blocks()

    def _merge_free_blocks(self):
        merged_blocks = []
        previous_block = None

        for block in self.blocks:
            if previous_block and previous_block.is_free and block.is_free and previous_block.size == block.size:
                previous_block.size *= 2
            else:
                merged_blocks.append(block)
                previous_block = block

        self.blocks = merged_blocks

    def get_memory_status(self):
        status = []
        for i, block in enumerate(self.blocks):
            status.append(f"Block {i} ({block.start}-{block.start + block.size} KB): {'Free' if block.is_free else f'Occupied by Process {block.process_id}'}")
        return status

class PagingMemoryManager:
    def __init__(self, total_memory_size, page_size):
        self.total_memory_size = total_memory_size
        self.page_size = page_size
        self.num_pages = total_memory_size // page_size
        self.frames = [None] * self.num_pages
        self.page_table = {}

    def allocate_memory(self, process_id, process_size):
        num_pages_needed = (process_size + self.page_size - 1) // self.page_size
        allocated_frames = []
        for i in range(self.num_pages):
            if self.frames[i] is None:
                allocated_frames.append(i)
                if len(allocated_frames) == num_pages_needed:
                    break
        if len(allocated_frames) < num_pages_needed:
            messagebox.showwarning("Error", "Not enough memory to allocate the process!")
            return False

        for frame in allocated_frames:
            self.frames[frame] = process_id

        self.page_table[process_id] = allocated_frames

        return True

    def deallocate_memory(self, process_id):
        if process_id not in self.page_table:
            return False

        for frame in self.page_table[process_id]:
            self.frames[frame] = None

        del self.page_table[process_id]

        return True

    def get_memory_status(self):
        status = []
        for i, frame in enumerate(self.frames):
            if frame is None:
                status.append(f"Frame {i}: Free")
            else:
                status.append(f"Frame {i}: Occupied by Process {frame}")
        return status

class MemoryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")

        self.memory_manager = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Allocation Strategy:").grid(row=0, column=0)
        self.strategy = tk.StringVar(value="First Fit")
        tk.Radiobutton(self.root, text="First Fit", variable=self.strategy, value="First Fit").grid(row=0, column=1)
        tk.Radiobutton(self.root, text="Best Fit", variable=self.strategy, value="Best Fit").grid(row=0, column=2)
        tk.Radiobutton(self.root, text="Worst Fit", variable=self.strategy, value="Worst Fit").grid(row=0, column=3)

        tk.Label(self.root, text="Memory Partitioning Type:").grid(row=1, column=0)
        self.partitioning_type = tk.StringVar(value="Equal")
        tk.Radiobutton(self.root, text="Equal-sized Partitions", variable=self.partitioning_type, value="Equal").grid(row=1, column=1)
        tk.Radiobutton(self.root, text="Unequal-sized Partitions", variable=self.partitioning_type, value="Unequal").grid(row=1, column=2)
        tk.Radiobutton(self.root, text="Dynamic Allocation", variable=self.partitioning_type, value="Dynamic").grid(row=1, column=3)
        tk.Radiobutton(self.root, text="Buddy System", variable=self.partitioning_type, value="Buddy System").grid(row=1, column=4)
        tk.Radiobutton(self.root, text="Paging", variable=self.partitioning_type, value="Paging").grid(row=1, column=5)

        tk.Label(self.root, text="Total Memory Size:").grid(row=2, column=0)
        self.total_memory_entry = tk.Entry(self.root)
        self.total_memory_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Partition Sizes (comma separated):").grid(row=3, column=0)
        self.partition_sizes_entry = tk.Entry(self.root)
        self.partition_sizes_entry.grid(row=3, column=1, columnspan=2)

        tk.Label(self.root, text="Page Size:").grid(row=4, column=0)
        self.page_size_entry = tk.Entry(self.root)
        self.page_size_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Initialize Memory", command=self.initialize_memory).grid(row=5, column=0, columnspan=3)

        tk.Label(self.root, text="Process ID:").grid(row=6, column=0)
        self.process_id_entry = tk.Entry(self.root)
        self.process_id_entry.grid(row=6, column=1)

        tk.Label(self.root, text="Process Size:").grid(row=7, column=0)
        self.process_size_entry = tk.Entry(self.root)
        self.process_size_entry.grid(row=7, column=1)

        tk.Button(self.root, text="Allocate Process", command=self.allocate_process).grid(row=8, column=0, columnspan=2)
        tk.Button(self.root, text="Deallocate Process", command=self.deallocate_process).grid(row=8, column=2)

        tk.Button(self.root, text="View Memory Status", command=self.view_memory_status).grid(row=9, column=0, columnspan=3)

        self.status_text = tk.Text(self.root, height=10, width=50)
        self.status_text.grid(row=10, column=0, columnspan=3)

    def initialize_memory(self):
        partitioning_type = self.partitioning_type.get()
        total_memory = int(self.total_memory_entry.get())

        if partitioning_type == "Equal":
            partition_size = int(self.partition_sizes_entry.get())
            partition_sizes = [partition_size] * (total_memory // partition_size)
            self.memory_manager = MemoryManager(partition_sizes)
        elif partitioning_type == "Unequal":
            partition_sizes = list(map(int, self.partition_sizes_entry.get().split(',')))
            self.memory_manager = MemoryManager(partition_sizes)
        elif partitioning_type == "Dynamic":
            self.memory_manager = DynamicMemoryManager(total_memory)
        elif partitioning_type == "Buddy System":
            self.memory_manager = BuddyMemoryManager(total_memory)
        elif partitioning_type == "Paging":
            page_size = int(self.page_size_entry.get())
            self.memory_manager = PagingMemoryManager(total_memory, page_size)

        messagebox.showinfo("Memory Initialized", "Memory has been initialized successfully!")

    def allocate_process(self):
        if not self.memory_manager:
            messagebox.showwarning("Error", "Initialize the memory first!")
            return

        process_id = self.process_id_entry.get()
        process_size = int(self.process_size_entry.get())
        strategy = self.strategy.get()
        partitioning_type = self.partitioning_type.get()

        if partitioning_type == "Equal" or partitioning_type == "Unequal" or partitioning_type == "Dynamic":
            if strategy == "First Fit":
                success = self.memory_manager.allocate_first_fit(process_id, process_size)
            elif strategy == "Best Fit":
                success = self.memory_manager.allocate_best_fit(process_id, process_size)
            elif strategy == "Worst Fit":
                success = self.memory_manager.allocate_worst_fit(process_id, process_size)
        elif partitioning_type == "Buddy System":
            success = self.memory_manager.allocate_memory(process_id, process_size)
        elif partitioning_type == "Paging":
            success = self.memory_manager.allocate_memory(process_id, process_size)

        if success:
            messagebox.showinfo("Success", f"Process {process_id} allocated successfully!")
        else:
            messagebox.showwarning("Error", "Not enough memory to allocate the process!")

    def deallocate_process(self):
        if not self.memory_manager:
            messagebox.showwarning("Error", "Initialize the memory first!")
            return

        process_id = self.process_id_entry.get()
        partitioning_type = self.partitioning_type.get()

        if partitioning_type == "Buddy System" or partitioning_type == "Paging":
            self.memory_manager.deallocate_memory(process_id)
        else:
            self.memory_manager.deallocate(process_id)

        messagebox.showinfo("Success", f"Process {process_id} deallocated successfully!")

    def view_memory_status(self):
        if not self.memory_manager:
            messagebox.showwarning("Error", "Initialize the memory first!")
            return

        status = self.memory_manager.get_memory_status()
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "\n".join(status))

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerApp(root)
    root.mainloop()