import tkinter as tk
from tkinter import ttk, messagebox


class MemoryBlock:
    def __init__(self, block_id, size, is_allocated=False, process_id=None):
        self.block_id = block_id
        self.size = size
        self.is_allocated = is_allocated
        self.process_id = process_id


class ProcessRequest:
    def __init__(self, process_id, size):
        self.process_id = process_id
        self.size = size
        self.allocated_block = None


class MemoryManagementModule:
    def __init__(self, parent, back_callback):
        self.parent = parent
        self.back_callback = back_callback
        self.memory_blocks = []
        self.process_requests = []
        self.allocation_history = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.parent, bg="#34495e", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(
            header_frame,
            text="← Back to Home",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="white",
            command=self.back_callback,
            cursor="hand2",
            relief=tk.FLAT
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title = tk.Label(
            header_frame,
            text="Memory Management Algorithms",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=20)
        
        # Main content area
        content_frame = tk.Frame(self.parent, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Input and Controls
        left_panel = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        left_panel.config(width=350)
        left_panel.pack_propagate(False)
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(left_panel, text="Select Algorithm",
                                   font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        algo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.algorithm_var = tk.StringVar(value="FirstFit")
        algorithms = [("First Fit", "FirstFit"), ("Best Fit", "BestFit"),
                     ("Worst Fit", "WorstFit")]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var,
                               value=value, bg="white", font=("Arial", 10))
            rb.pack(anchor=tk.W)
        
        # Memory block input
        block_frame = tk.LabelFrame(left_panel, text="Add Memory Block",
                                    font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        block_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Block size
        size_frame = tk.Frame(block_frame, bg="white")
        size_frame.pack(fill=tk.X, pady=2)
        tk.Label(size_frame, text="Block Size (KB):", width=15, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.block_size_var = tk.StringVar(value="100")
        tk.Entry(size_frame, textvariable=self.block_size_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Add block button
        tk.Button(block_frame, text="Add Block", command=self.add_memory_block,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=(10, 0))
        
        # Quick setup button
        tk.Button(block_frame, text="Quick Setup (5 blocks)", command=self.quick_setup,
                 bg="#16a085", fg="white", font=("Arial", 9),
                 cursor="hand2").pack(pady=(5, 0))
        
        # Memory blocks list
        blocks_list_frame = tk.LabelFrame(left_panel, text="Memory Blocks",
                                          font=("Arial", 11, "bold"), bg="white", padx=5, pady=5)
        blocks_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for memory blocks
        columns = ("ID", "Size", "Status", "Process")
        self.blocks_tree = ttk.Treeview(blocks_list_frame, columns=columns,
                                        show="headings", height=5)
        self.blocks_tree.heading("ID", text="Block")
        self.blocks_tree.heading("Size", text="Size (KB)")
        self.blocks_tree.heading("Status", text="Status")
        self.blocks_tree.heading("Process", text="Process")
        
        self.blocks_tree.column("ID", width=50)
        self.blocks_tree.column("Size", width=70)
        self.blocks_tree.column("Status", width=70)
        self.blocks_tree.column("Process", width=70)
        
        self.blocks_tree.pack(fill=tk.BOTH, expand=True)
        
        # Process request input
        process_frame = tk.LabelFrame(left_panel, text="Process Request",
                                      font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        process_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Process ID
        pid_frame = tk.Frame(process_frame, bg="white")
        pid_frame.pack(fill=tk.X, pady=2)
        tk.Label(pid_frame, text="Process ID:", width=15, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.process_id_var = tk.StringVar(value="P1")
        tk.Entry(pid_frame, textvariable=self.process_id_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Request size
        req_size_frame = tk.Frame(process_frame, bg="white")
        req_size_frame.pack(fill=tk.X, pady=2)
        tk.Label(req_size_frame, text="Size Needed (KB):", width=15, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.request_size_var = tk.StringVar(value="50")
        tk.Entry(req_size_frame, textvariable=self.request_size_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Allocate button
        tk.Button(process_frame, text="Allocate Memory", command=self.allocate_memory,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=(10, 5))
        
        # Deallocate button
        tk.Button(process_frame, text="Deallocate Process", command=self.deallocate_memory,
                 bg="#e67e22", fg="white", font=("Arial", 9),
                 cursor="hand2").pack(pady=(0, 0))
        
        # Control buttons
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Clear All", command=self.clear_all,
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Reset Memory", command=self.reset_memory,
                 bg="#95a5a6", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        
        # Right panel - Visualization
        right_panel = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
        
        # Canvas for memory visualization
        canvas_frame = tk.LabelFrame(right_panel, text="Memory Visualization",
                                     font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Results frame
        results_frame = tk.LabelFrame(right_panel, text="Allocation Details & Statistics",
                                      font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        results_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.results_text = tk.Text(results_frame, height=8, font=("Courier", 9),
                                   bg="#f8f9fa", relief=tk.FLAT)
        self.results_text.pack(fill=tk.X, padx=5, pady=5)
    
    def add_memory_block(self):
        try:
            size = int(self.block_size_var.get())
            
            if size <= 0:
                messagebox.showerror("Error", "Block size must be positive")
                return
            
            block_id = f"B{len(self.memory_blocks) + 1}"
            block = MemoryBlock(block_id, size)
            self.memory_blocks.append(block)
            
            self.update_blocks_display()
            self.draw_memory_visualization()
            self.update_statistics()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value")
    
    def quick_setup(self):
        self.clear_all()
        sizes = [100, 200, 300, 150, 250]
        for size in sizes:
            block_id = f"B{len(self.memory_blocks) + 1}"
            block = MemoryBlock(block_id, size)
            self.memory_blocks.append(block)
        
        self.update_blocks_display()
        self.draw_memory_visualization()
        self.update_statistics()
    
    def update_blocks_display(self):
        # Clear existing items
        for item in self.blocks_tree.get_children():
            self.blocks_tree.delete(item)
        
        # Add all blocks
        for block in self.memory_blocks:
            status = "Allocated" if block.is_allocated else "Free"
            process = block.process_id if block.is_allocated else "-"
            self.blocks_tree.insert("", tk.END,
                                   values=(block.block_id, block.size, status, process))
    
    def allocate_memory(self):
        if not self.memory_blocks:
            messagebox.showwarning("Warning", "Please add memory blocks first")
            return
        
        try:
            process_id = self.process_id_var.get().strip()
            size = int(self.request_size_var.get())
            
            if not process_id:
                messagebox.showerror("Error", "Process ID cannot be empty")
                return
            
            if size <= 0:
                messagebox.showerror("Error", "Size must be positive")
                return
            
            # Check if process already allocated
            for block in self.memory_blocks:
                if block.is_allocated and block.process_id == process_id:
                    messagebox.showwarning("Warning",
                                          f"Process {process_id} already has memory allocated")
                    return
            
            # Perform allocation based on selected algorithm
            algorithm = self.algorithm_var.get()
            allocated_block = None
            
            if algorithm == "FirstFit":
                allocated_block = self.first_fit(size)
            elif algorithm == "BestFit":
                allocated_block = self.best_fit(size)
            elif algorithm == "WorstFit":
                allocated_block = self.worst_fit(size)
            
            if allocated_block:
                # Allocate the block
                allocated_block.is_allocated = True
                allocated_block.process_id = process_id
                
                # Record allocation
                self.allocation_history.append({
                    'process_id': process_id,
                    'size': size,
                    'block_id': allocated_block.block_id,
                    'block_size': allocated_block.size,
                    'algorithm': algorithm
                })
                
                # Update displays
                self.update_blocks_display()
                self.draw_memory_visualization()
                self.update_statistics()
                
                # Auto-increment process ID
                if process_id.startswith("P") and process_id[1:].isdigit():
                    next_num = int(process_id[1:]) + 1
                    self.process_id_var.set(f"P{next_num}")
                
                messagebox.showinfo("Success",
                                   f"Process {process_id} allocated to {allocated_block.block_id}\n"
                                   f"Requested: {size} KB, Allocated: {allocated_block.size} KB\n"
                                   f"Internal Fragmentation: {allocated_block.size - size} KB")
            else:
                messagebox.showerror("Allocation Failed",
                                    f"No suitable block found for {size} KB request")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def first_fit(self, size):
        for block in self.memory_blocks:
            if not block.is_allocated and block.size >= size:
                return block
        return None
    
    def best_fit(self, size):
        suitable_blocks = [block for block in self.memory_blocks
                          if not block.is_allocated and block.size >= size]
        
        if not suitable_blocks:
            return None
        
        # Return the block with minimum size that fits
        return min(suitable_blocks, key=lambda b: b.size)
    
    def worst_fit(self, size):
        suitable_blocks = [block for block in self.memory_blocks
                          if not block.is_allocated and block.size >= size]
        
        if not suitable_blocks:
            return None
        
        # Return the block with maximum size
        return max(suitable_blocks, key=lambda b: b.size)
    
    def deallocate_memory(self):
        try:
            process_id = self.process_id_var.get().strip()
            
            if not process_id:
                messagebox.showerror("Error", "Please enter Process ID to deallocate")
                return
            
            # Find and deallocate the block
            found = False
            for block in self.memory_blocks:
                if block.is_allocated and block.process_id == process_id:
                    block.is_allocated = False
                    block.process_id = None
                    found = True
                    break
            
            if found:
                self.update_blocks_display()
                self.draw_memory_visualization()
                self.update_statistics()
                messagebox.showinfo("Success", f"Memory deallocated for process {process_id}")
            else:
                messagebox.showwarning("Not Found",
                                      f"Process {process_id} has no allocated memory")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_all(self):
        self.memory_blocks.clear()
        self.allocation_history.clear()
        self.update_blocks_display()
        self.canvas.delete("all")
        self.results_text.delete(1.0, tk.END)
    
    def reset_memory(self):
        for block in self.memory_blocks:
            block.is_allocated = False
            block.process_id = None
        
        self.allocation_history.clear()
        self.update_blocks_display()
        self.draw_memory_visualization()
        self.update_statistics()
    
    def draw_memory_visualization(self):
        self.canvas.delete("all")
        
        if not self.memory_blocks:
            self.canvas.create_text(400, 200,
                                   text="No memory blocks defined\nAdd blocks to visualize",
                                   font=("Arial", 14),
                                   fill="#95a5a6")
            return
        
        # Calculate dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 400
        
        # Draw title
        self.canvas.create_text(canvas_width // 2, 20,
                               text=f"Memory Layout - {self.algorithm_var.get()} Algorithm",
                               font=("Arial", 14, "bold"))
        
        # Calculate total memory
        total_memory = sum(block.size for block in self.memory_blocks)
        
        # Drawing parameters
        margin = 50
        block_height = 60
        start_y = 60
        available_width = canvas_width - 2 * margin
        
        # Calculate scale
        scale = available_width / total_memory if total_memory > 0 else 1
        
        # Draw memory blocks
        current_x = margin
        
        for i, block in enumerate(self.memory_blocks):
            block_width = block.size * scale
            
            # Choose color based on allocation status
            if block.is_allocated:
                fill_color = "#e74c3c"  # Red for allocated
                text_color = "white"
            else:
                fill_color = "#2ecc71"  # Green for free
                text_color = "white"
            
            # Draw block rectangle
            self.canvas.create_rectangle(current_x, start_y,
                                         current_x + block_width, start_y + block_height,
                                         fill=fill_color,
                                         outline="black",
                                         width=2)
            
            # Draw block info
            center_x = current_x + block_width / 2
            center_y = start_y + block_height / 2
            
            self.canvas.create_text(center_x, center_y - 10,
                                   text=block.block_id,
                                   font=("Arial", 11, "bold"),
                                   fill=text_color)
            
            self.canvas.create_text(center_x, center_y + 10,
                                   text=f"{block.size} KB",
                                   font=("Arial", 9),
                                   fill=text_color)
            
            if block.is_allocated:
                self.canvas.create_text(center_x, center_y + 25,
                                       text=block.process_id,
                                       font=("Arial", 9, "bold"),
                                       fill=text_color)
            
            current_x += block_width
        
        # Draw legend
        legend_y = start_y + block_height + 40
        
        # Free block legend
        self.canvas.create_rectangle(margin, legend_y, margin + 30, legend_y + 20,
                                     fill="#2ecc71", outline="black", width=1)
        self.canvas.create_text(margin + 40, legend_y + 10,
                               text="Free Block",
                               anchor=tk.W,
                               font=("Arial", 10))
        
        # Allocated block legend
        self.canvas.create_rectangle(margin + 150, legend_y, margin + 180, legend_y + 20,
                                     fill="#e74c3c", outline="black", width=1)
        self.canvas.create_text(margin + 190, legend_y + 10,
                               text="Allocated Block",
                               anchor=tk.W,
                               font=("Arial", 10))
        
        # Draw memory addresses (simplified visualization)
        addr_y = start_y + block_height + 10
        self.canvas.create_text(margin, addr_y,
                               text="0",
                               font=("Arial", 9))
        self.canvas.create_text(margin + available_width, addr_y,
                               text=f"{total_memory}",
                               font=("Arial", 9))
    
    def update_statistics(self):
        self.results_text.delete(1.0, tk.END)
        
        if not self.memory_blocks:
            self.results_text.insert(tk.END, "No memory blocks defined.\n")
            return
        
        # Calculate statistics
        total_memory = sum(block.size for block in self.memory_blocks)
        allocated_memory = sum(block.size for block in self.memory_blocks if block.is_allocated)
        free_memory = total_memory - allocated_memory
        
        # Count blocks
        total_blocks = len(self.memory_blocks)
        allocated_blocks = sum(1 for block in self.memory_blocks if block.is_allocated)
        free_blocks = total_blocks - allocated_blocks
        
        # Calculate internal fragmentation
        internal_fragmentation = 0
        for entry in self.allocation_history:
            if any(b.block_id == entry['block_id'] and b.is_allocated 
                  for b in self.memory_blocks):
                internal_fragmentation += entry['block_size'] - entry['size']
        
        # Display statistics
        self.results_text.insert(tk.END, f"{'='*60}\n")
        self.results_text.insert(tk.END, f" Memory Statistics\n")
        self.results_text.insert(tk.END, f"{'='*60}\n\n")
        
        self.results_text.insert(tk.END, f"Total Memory:          {total_memory} KB\n")
        self.results_text.insert(tk.END, f"Allocated Memory:      {allocated_memory} KB\n")
        self.results_text.insert(tk.END, f"Free Memory:           {free_memory} KB\n")
        self.results_text.insert(tk.END, f"Utilization:           {(allocated_memory/total_memory*100):.1f}%\n\n")
        
        self.results_text.insert(tk.END, f"Total Blocks:          {total_blocks}\n")
        self.results_text.insert(tk.END, f"Allocated Blocks:      {allocated_blocks}\n")
        self.results_text.insert(tk.END, f"Free Blocks:           {free_blocks}\n\n")
        
        self.results_text.insert(tk.END, f"Internal Fragmentation: {internal_fragmentation} KB\n")
        self.results_text.insert(tk.END, f"External Fragmentation: {free_blocks} fragments\n")
        self.results_text.insert(tk.END, f"{'='*60}\n")
        
        # Show recent allocations
        if self.allocation_history:
            self.results_text.insert(tk.END, f"\nRecent Allocations:\n")
            for entry in self.allocation_history[-5:]:
                status = "Active"
                for block in self.memory_blocks:
                    if block.block_id == entry['block_id'] and not block.is_allocated:
                        status = "Deallocated"
                        break
                
                self.results_text.insert(tk.END,
                                        f"  {entry['process_id']} → {entry['block_id']} "
                                        f"({entry['size']} KB) [{status}]\n")
