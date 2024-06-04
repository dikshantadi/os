import tkinter as tk
from tkinter import messagebox
class MemoryManagement:
    def __init__(self, total_size):
        self.total_size = total_size
        self.memory = [None] * total_size

    def display_memory(self):
        print("Memory Allocation:")
        for i in range(self.total_size):
            if self.memory[i] is None:
                print(f"[{i}]: Free")
            else:
                print(f"[{i}]: Process {self.memory[i]}")

class FixedSizePartitioning(MemoryManagement):
    def __init__(self, total_size, partition_size):
        super().__init__(total_size)
        self.partition_size = partition_size
        self.partitions = [None] * (total_size // partition_size)

    def allocate(self, process_id, size, strategy='first_fit'):
        # Implement first fit, best fit, or worst fit allocation strategy
        pass

class UnequalSizePartitioning(MemoryManagement):
    def __init__(self, total_size, partition_sizes):
        super().__init__(total_size)
        self.partitions = partition_sizes

    def allocate(self, process_id, size, strategy='first_fit'):
        # Implement allocation strategy based on partition sizes
        pass

class DynamicMemoryAllocation(MemoryManagement):
    def allocate(self, process_id, size, strategy='first_fit'):
        # Implement first fit, best fit, or worst fit allocation strategy
        pass

class BuddySystem(MemoryManagement):
    def allocate(self, process_id, size):
        # Implement buddy system allocation
        pass

class Paging(MemoryManagement):
    def __init__(self, total_size, page_size):
        super().__init__(total_size)
        self.page_size = page_size
        self.page_table = {}

    def allocate(self, process_id, size):
        # Implement paging allocation
        pass


class MemoryManagementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")

        self.create_widgets()

    def create_widgets(self):
        self.total_memory_label = tk.Label(self.root, text="Total Memory Size:")
        self.total_memory_label.grid(row=0, column=0)
        self.total_memory_entry = tk.Entry(self.root)
        self.total_memory_entry.grid(row=0, column=1)

        self.technique_label = tk.Label(self.root, text="Memory Management Technique:")
        self.technique_label.grid(row=1, column=0)
        self.technique_var = tk.StringVar(value="fixed")
        self.technique_menu = tk.OptionMenu(self.root, self.technique_var, "fixed", "unequal", "dynamic", "buddy", "paging")
        self.technique_menu.grid(row=1, column=1)

        self.partition_label = tk.Label(self.root, text="Partition Size (fixed/unequal):")
        self.partition_label.grid(row=2, column=0)
        self.partition_entry = tk.Entry(self.root)
        self.partition_entry.grid(row=2, column=1)

        self.page_size_label = tk.Label(self.root, text="Page Size (paging):")
        self.page_size_label.grid(row=3, column=0)
        self.page_size_entry = tk.Entry(self.root)
        self.page_size_entry.grid(row=3, column=1)

        self.process_id_label = tk.Label(self.root, text="Process ID:")
        self.process_id_label.grid(row=4, column=0)
        self.process_id_entry = tk.Entry(self.root)
        self.process_id_entry.grid(row=4, column=1)

        self.process_size_label = tk.Label(self.root, text="Process Size:")
        self.process_size_label.grid(row=5, column=0)
        self.process_size_entry = tk.Entry(self.root)
        self.process_size_entry.grid(row=5, column=1)

        self.allocate_button = tk.Button(self.root, text="Allocate", command=self.allocate_memory)
        self.allocate_button.grid(row=6, column=0)

        self.deallocate_button = tk.Button(self.root, text="Deallocate", command=self.deallocate_memory)
        self.deallocate_button.grid(row=6, column=1)

        self.display_button = tk.Button(self.root, text="Display Memory", command=self.display_memory)
        self.display_button.grid(row=7, column=0, columnspan=2)

        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.grid(row=8, column=0, columnspan=2)

    def initialize_memory_management(self):
        total_size = int(self.total_memory_entry.get())
        technique = self.technique_var.get()

        if technique == 'fixed':
            partition_size = int(self.partition_entry.get())
            self.mm = FixedSizePartitioning(total_size, partition_size)
        elif technique == 'unequal':
            partition_sizes = list(map(int, self.partition_entry.get().split()))
            self.mm = UnequalSizePartitioning(total_size, partition_sizes)
        elif technique == 'dynamic':
            self.mm = DynamicMemoryAllocation(total_size)
        elif technique == 'buddy':
            self.mm = BuddySystem(total_size)
        elif technique == 'paging':
            page_size = int(self.page_size_entry.get())
            self.mm = Paging(total_size, page_size)

    def allocate_memory(self):
        process_id = int(self.process_id_entry.get())
        size = int(self.process_size_entry.get())
        strategy = "first_fit"  # For simplicity, using first_fit strategy

        if not hasattr(self, 'mm'):
            self.initialize_memory_management()

        if isinstance(self.mm, Paging):
            self.mm.allocate(process_id, size)
        else:
            self.mm.allocate(process_id, size, strategy)

    def deallocate_memory(self):
        process_id = int(self.process_id_entry.get())
        if hasattr(self, 'mm'):
            self.mm.deallocate(process_id)

    def display_memory(self):
        if hasattr(self, 'mm'):
            self.output_text.delete('1.0', tk.END)
            memory_status = self.mm.display_memory()
            self.output_text.insert(tk.END, memory_status)

class FixedSizePartitioning(MemoryManagement):
    def __init__(self, total_size, partition_size):
        super().__init__(total_size)
        self.partition_size = partition_size
        self.partitions = [None] * (total_size // partition_size)

    def allocate(self, process_id, size, strategy='first_fit'):
        if size > self.partition_size:
            messagebox.showerror("Error", f"Process {process_id} requires more memory than partition size.")
            return False

        if strategy == 'first_fit':
            for i in range(len(self.partitions)):
                if self.partitions[i] is None:
                    self.partitions[i] = process_id
                    for j in range(i * self.partition_size, (i + 1) * self.partition_size):
                        self.memory[j] = process_id
                    return True
        messagebox.showerror("Error", f"Failed to allocate memory for Process {process_id}")
        return False

    def deallocate(self, process_id):
        for i in range(len(self.partitions)):
            if self.partitions[i] == process_id:
                self.partitions[i] = None
                for j in range(i * self.partition_size, (i + 1) * self.partition_size):
                    self.memory[j] = None

    def display_memory(self):
        memory_status = "Memory Allocation:\n"
        for i in range(len(self.memory)):
            if self.memory[i] is None:
                memory_status += f"[{i}]: Free\n"
            else:
                memory_status += f"[{i}]: Process {self.memory[i]}\n"
        return memory_status

# Similarly implement other classes...

if __name__ == "_main_":
    root = tk.Tk()
    app = MemoryManagementSimulator(root)
    root.mainloop()
