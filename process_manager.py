import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import random


class Process:
    
    def __init__(self, pid, name, memory_size, process_type="User"):
        self.pid = pid
        self.name = name
        self.memory_size = memory_size
        self.process_type = process_type
        self.state = "Ready"  # Ready, Running, Waiting, Terminated
        self.allocated_memory = None
        self.creation_time = time.strftime("%H:%M:%S")
        self.cpu_time = 0
        self.priority = random.randint(1, 5)


class MemorySegment:
    
    def __init__(self, start_address, size):
        self.start_address = start_address
        self.size = size
        self.is_allocated = False
        self.process_pid = None
        self.process_name = None


class ProcessManagerModule:
    
    def __init__(self, parent, back_callback):
        self.parent = parent
        self.back_callback = back_callback
        self.processes = []
        self.memory_segments = []
        self.total_memory = 512  # 512 KB total RAM
        self.next_pid = 1
        
        # Initialize memory
        self.initialize_memory()
        self.setup_ui()
        
        # Add some system processes
        self.create_system_process("kernel", 64)
        self.create_system_process("init", 16)
    
    def initialize_memory(self):
        # Start with one large free block
        self.memory_segments.append(MemorySegment(0, self.total_memory))
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.parent, bg="#16a085", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(
            header_frame,
            text="← Back to Home",
            font=("Arial", 11),
            bg="#138871",
            fg="white",
            command=self.back_callback,
            cursor="hand2",
            relief=tk.FLAT
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title = tk.Label(
            header_frame,
            text="Process Manager - Live Memory Allocation",
            font=("Arial", 18, "bold"),
            bg="#16a085",
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=20)
        
        # Main content
        content_frame = tk.Frame(self.parent, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - System overview
        top_section = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        top_section.pack(fill=tk.X, padx=0, pady=(0, 5))
        
        # System stats
        stats_frame = tk.Frame(top_section, bg="white", padx=10, pady=10)
        stats_frame.pack(fill=tk.X)
        
        # Memory usage bar
        tk.Label(stats_frame, text="Memory Usage:", font=("Arial", 11, "bold"),
                bg="white").pack(anchor=tk.W)
        
        self.memory_bar_frame = tk.Frame(stats_frame, bg="#ecf0f1", height=30)
        self.memory_bar_frame.pack(fill=tk.X, pady=5)
        
        self.memory_bar_canvas = tk.Canvas(self.memory_bar_frame, height=30,
                                           bg="#ecf0f1", highlightthickness=0)
        self.memory_bar_canvas.pack(fill=tk.X)
        
        # Stats labels
        stats_info = tk.Frame(stats_frame, bg="white")
        stats_info.pack(fill=tk.X, pady=5)
        
        self.stats_label = tk.Label(stats_info, text="", font=("Arial", 10),
                                    bg="white", fg="#2c3e50", justify=tk.LEFT)
        self.stats_label.pack(side=tk.LEFT)
        
        # Bottom section - Split view
        bottom_frame = tk.Frame(content_frame, bg="#ecf0f1")
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Process control
        left_panel = tk.Frame(bottom_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        left_panel.config(width=350)
        left_panel.pack_propagate(False)
        
        # Create process section
        create_frame = tk.LabelFrame(left_panel, text="Create New Process",
                                     font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Process name
        name_frame = tk.Frame(create_frame, bg="white")
        name_frame.pack(fill=tk.X, pady=2)
        tk.Label(name_frame, text="Process Name:", width=13, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.proc_name_var = tk.StringVar(value="myapp")
        tk.Entry(name_frame, textvariable=self.proc_name_var, width=12,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Memory required
        mem_frame = tk.Frame(create_frame, bg="white")
        mem_frame.pack(fill=tk.X, pady=2)
        tk.Label(mem_frame, text="Memory (KB):", width=13, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.proc_mem_var = tk.StringVar(value="32")
        tk.Entry(mem_frame, textvariable=self.proc_mem_var, width=12,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Quick create buttons
        quick_frame = tk.Frame(create_frame, bg="white")
        quick_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(quick_frame, text="Small (16KB)", 
                 command=lambda: self.quick_create(16),
                 bg="#3498db", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="Medium (32KB)", 
                 command=lambda: self.quick_create(32),
                 bg="#3498db", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="Large (64KB)", 
                 command=lambda: self.quick_create(64),
                 bg="#3498db", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        
        # Create button
        tk.Button(create_frame, text="Create Process", command=self.create_process,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=(5, 0))
        
        # Process list
        list_frame = tk.LabelFrame(left_panel, text="Running Processes",
                                   font=("Arial", 11, "bold"), bg="white", padx=5, pady=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for processes
        columns = ("PID", "Name", "Memory", "State")
        self.process_tree = ttk.Treeview(list_frame, columns=columns, 
                                        show="headings", height=10)
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("Name", text="Name")
        self.process_tree.heading("Memory", text="Memory")
        self.process_tree.heading("State", text="State")
        
        self.process_tree.column("PID", width=50, anchor=tk.CENTER)
        self.process_tree.column("Name", width=100)
        self.process_tree.column("Memory", width=80, anchor=tk.CENTER)
        self.process_tree.column("State", width=70, anchor=tk.CENTER)
        
        self.process_tree.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="View Details", command=self.view_process_details,
                 bg="#3498db", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Terminate Process", command=self.terminate_process,
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Kill All User Processes", command=self.kill_all_user,
                 bg="#c0392b", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        
        # Right panel - Memory visualization
        right_panel = tk.Frame(bottom_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
        
        # Memory map
        mem_frame = tk.LabelFrame(right_panel, text="Physical Memory Map",
                                  font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        mem_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas with scrollbar
        canvas_container = tk.Frame(mem_frame, bg="white")
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.memory_scrollbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        self.memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.memory_canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0,
                                       yscrollcommand=self.memory_scrollbar.set)
        self.memory_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.memory_scrollbar.config(command=self.memory_canvas.yview)
        
        # Enable mouse wheel scrolling
        self.memory_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.memory_canvas.bind("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.memory_canvas.bind("<Button-5>", self._on_mousewheel)  # Linux scroll down
        
        # Activity log
        log_frame = tk.LabelFrame(right_panel, text="System Log",
                                  font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        log_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, font=("Courier", 8),
                                                  bg="#2c3e50", fg="#2ecc71", relief=tk.FLAT)
        self.log_text.pack(fill=tk.X, padx=5, pady=5)
        self.log("System initialized. Total RAM: {} KB".format(self.total_memory))
        self.log("System processes started.")
        
        # Initial updates
        self.update_displays()
    
    def create_system_process(self, name, memory):
        self.allocate_memory_to_process(name, memory, "System")
    
    def quick_create(self, size):
        self.proc_mem_var.set(str(size))
        self.create_process()
    
    def create_process(self):
        try:
            name = self.proc_name_var.get().strip()
            memory = int(self.proc_mem_var.get())
            
            if not name:
                messagebox.showerror("Error", "Process name cannot be empty")
                return
            
            if memory <= 0:
                messagebox.showerror("Error", "Memory must be positive")
                return
            
            self.allocate_memory_to_process(name, memory, "User")
            
            # Auto-increment name
            if name[-1].isdigit():
                base = ''.join(filter(str.isalpha, name))
                num = int(''.join(filter(str.isdigit, name)))
                self.proc_name_var.set(f"{base}{num+1}")
            else:
                self.proc_name_var.set(f"{name}2")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def allocate_memory_to_process(self, name, memory_size, proc_type):
        # Find suitable memory segment
        for i, segment in enumerate(self.memory_segments):
            if not segment.is_allocated and segment.size >= memory_size:
                # Create process
                pid = self.next_pid
                self.next_pid += 1
                
                process = Process(pid, name, memory_size, proc_type)
                process.state = "Running" if proc_type == "System" else "Ready"
                process.allocated_memory = segment.start_address
                
                self.log(f"Creating process PID={pid} '{name}' ({memory_size} KB)")
                
                # Allocate memory
                if segment.size == memory_size:
                    # Exact fit
                    segment.is_allocated = True
                    segment.process_pid = pid
                    segment.process_name = name
                    self.log(f"  Allocated memory at 0x{segment.start_address:04X} (exact fit)")
                else:
                    # Split segment
                    # Create allocated segment
                    allocated_seg = MemorySegment(segment.start_address, memory_size)
                    allocated_seg.is_allocated = True
                    allocated_seg.process_pid = pid
                    allocated_seg.process_name = name
                    
                    # Create free segment
                    free_seg = MemorySegment(
                        segment.start_address + memory_size,
                        segment.size - memory_size
                    )
                    
                    # Replace original segment with split segments
                    self.memory_segments[i] = allocated_seg
                    self.memory_segments.insert(i + 1, free_seg)
                    
                    self.log(f"  Allocated memory at 0x{segment.start_address:04X}")
                    self.log(f"  Internal fragmentation: {0} KB (perfect fit)")
                
                self.processes.append(process)
                self.log(f"SUCCESS: Process '{name}' created with PID={pid}")
                
                self.update_displays()
                return True
        
        # No suitable memory found
        messagebox.showerror("Memory Full", 
                            f"Cannot allocate {memory_size} KB!\nInsufficient contiguous memory.")
        self.log(f"ERROR: Failed to create '{name}' - out of memory")
        return False
    
    def terminate_process(self):
        selection = self.process_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to terminate")
            return
        
        item = self.process_tree.item(selection[0])
        pid = int(item['values'][0])
        
        # Find process
        process = next((p for p in self.processes if p.pid == pid), None)
        if not process:
            return
        
        # Prevent terminating system processes
        if process.process_type == "System":
            messagebox.showerror("Error", "Cannot terminate system processes!")
            return
        
        if not messagebox.askyesno("Confirm Terminate",
                                   f"Terminate process PID={pid} '{process.name}'?"):
            return
        
        self.log(f"Terminating process PID={pid} '{process.name}'...")
        
        # Free memory
        for segment in self.memory_segments:
            if segment.process_pid == pid:
                segment.is_allocated = False
                segment.process_pid = None
                segment.process_name = None
                self.log(f"  Freed memory at 0x{segment.start_address:04X} ({segment.size} KB)")
                break
        
        # Merge adjacent free segments
        self.merge_free_segments()
        
        # Remove process
        self.processes.remove(process)
        self.log(f"SUCCESS: Process PID={pid} terminated")
        
        self.update_displays()
    
    def kill_all_user(self):
        user_processes = [p for p in self.processes if p.process_type == "User"]
        
        if not user_processes:
            messagebox.showinfo("Info", "No user processes running")
            return
        
        if not messagebox.askyesno("Confirm", 
                                   f"Kill all {len(user_processes)} user processes?"):
            return
        
        self.log("Killing all user processes...")
        
        for process in user_processes[:]:  # Copy list to avoid modification during iteration
            # Code to reallocate memory for each process
            for segment in self.memory_segments:
                if segment.process_pid == process.pid:
                    segment.is_allocated = False
                    segment.process_pid = None
                    segment.process_name = None
                    break
            
            self.processes.remove(process)
            self.log(f"  Killed PID={process.pid} '{process.name}'")
        
        self.merge_free_segments()
        self.log("All user processes terminated")
        
        self.update_displays()
    
    def merge_free_segments(self):
        merged = True
        while merged:
            merged = False
            for i in range(len(self.memory_segments) - 1):
                curr = self.memory_segments[i]
                next_seg = self.memory_segments[i + 1]
                
                if not curr.is_allocated and not next_seg.is_allocated:
                    # Merge
                    curr.size += next_seg.size
                    self.memory_segments.pop(i + 1)
                    merged = True
                    break
    
    def view_process_details(self):
        selection = self.process_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process")
            return
        
        item = self.process_tree.item(selection[0])
        pid = int(item['values'][0])
        
        process = next((p for p in self.processes if p.pid == pid), None)
        if not process:
            return
        
        # Create details window
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Process Details - PID {pid}")
        details_window.geometry("400x350")
        details_window.configure(bg="white")
        
        # Header
        header = tk.Frame(details_window, bg="#3498db", padx=10, pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"Process: {process.name}",
                font=("Arial", 14, "bold"), bg="#3498db", fg="white").pack()
        tk.Label(header, text=f"PID: {pid}",
                font=("Arial", 11), bg="#3498db", fg="white").pack()
        
        # Details
        details_frame = tk.Frame(details_window, bg="white", padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details = [
            ("Process Name:", process.name),
            ("Process ID:", str(pid)),
            ("Type:", process.process_type),
            ("State:", process.state),
            ("Memory Size:", f"{process.memory_size} KB"),
            ("Memory Address:", f"0x{process.allocated_memory:04X}" if process.allocated_memory else "0x0000"),
            ("Priority:", str(process.priority)),
            ("Created:", process.creation_time),
            ("CPU Time:", f"{process.cpu_time} ms")
        ]
        
        for i, (label, value) in enumerate(details):
            tk.Label(details_frame, text=label, font=("Arial", 10, "bold"),
                    bg="white", anchor='w', width=15).grid(row=i, column=0, sticky='w', pady=5)
            tk.Label(details_frame, text=value, font=("Arial", 10),
                    bg="white", anchor='w').grid(row=i, column=1, sticky='w', pady=5)
        
        # Close button
        tk.Button(details_window, text="Close", command=details_window.destroy,
                 bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
    
    def update_displays(self):
        self.update_process_list()
        self.update_memory_bar()
        self.draw_memory_map()
        self.update_stats()
    
    def update_process_list(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        for process in self.processes:
            self.process_tree.insert("", tk.END,
                                    values=(process.pid, process.name,
                                           f"{process.memory_size} KB", process.state))
    
    def update_memory_bar(self):
        self.memory_bar_canvas.delete("all")
        
        width = self.memory_bar_canvas.winfo_width()
        if width <= 1:
            width = 700
        
        used_memory = sum(s.size for s in self.memory_segments if s.is_allocated)
        free_memory = self.total_memory - used_memory
        
        used_width = (used_memory / self.total_memory) * width
        
        # Used memory (red)
        if used_width > 0:
            self.memory_bar_canvas.create_rectangle(0, 0, used_width, 30,
                                                    fill="#e74c3c", outline="")
        
        # Free memory (green)
        if used_width < width:
            self.memory_bar_canvas.create_rectangle(used_width, 0, width, 30,
                                                    fill="#2ecc71", outline="")
        
        # Text
        self.memory_bar_canvas.create_text(width // 2, 15,
                                           text=f"Used: {used_memory} KB | Free: {free_memory} KB",
                                           font=("Arial", 10, "bold"), fill="white")
    
    def draw_memory_map(self):
        self.memory_canvas.delete("all")
        
        canvas_width = self.memory_canvas.winfo_width()
        canvas_height = self.memory_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 500
        
        # Calculate required height based on minimum segment heights
        min_segment_height = 45  # Minimum height for readability
        num_segments = len(self.memory_segments)
        min_required_height = num_segments * min_segment_height + 150  # Extra for title and legend
        
        # Use the larger of canvas height or calculated minimum
        draw_height = max(canvas_height, min_required_height)
        available_height = draw_height - 150  # Space for title and legend
        
        # Title
        self.memory_canvas.create_text(canvas_width // 2, 20,
                                       text="RAM Layout (Linear Address Space)",
                                       font=("Arial", 12, "bold"))
        
        # Draw memory segments
        margin = 40
        mem_width = 200
        start_x = (canvas_width - mem_width) // 2
        start_y = 50
        
        # Scale with minimum height for each segment
        scale = available_height / self.total_memory
        
        current_y = start_y
        
        for segment in self.memory_segments:
            seg_height = max(segment.size * scale, min_segment_height)
            
            # Color
            if segment.is_allocated:
                if segment.process_name in ["kernel", "init"]:
                    color = "#34495e"  # System processes
                else:
                    color = "#3498db"  # User processes
            else:
                color = "#ecf0f1"  # Free
            
            # Draw segment
            self.memory_canvas.create_rectangle(start_x, current_y,
                                               start_x + mem_width, current_y + seg_height,
                                               fill=color, outline="black", width=2)
            
            # Label
            label_y = current_y + seg_height / 2
            
            if segment.is_allocated:
                # Display process info with better visibility
                font_size = 11
                text = f"{segment.process_name}\nPID={segment.process_pid}\n{segment.size}KB"
                text_color = "white"
                
                self.memory_canvas.create_text(start_x + mem_width // 2, label_y,
                                              text=text, font=("Arial", font_size, "bold"),
                                              fill=text_color)
            else:
                # Free memory display
                font_size = 11
                text = f"FREE\n{segment.size} KB"
                text_color = "#7f8c8d"
                
                self.memory_canvas.create_text(start_x + mem_width // 2, label_y,
                                              text=text, font=("Arial", font_size, "bold"),
                                              fill=text_color)
            
            # Address labels
            self.memory_canvas.create_text(start_x - 15, current_y,
                                          text=f"0x{segment.start_address:04X}",
                                          anchor=tk.E, font=("Courier", 9))
            
            current_y += seg_height
        
        # End address
        self.memory_canvas.create_text(start_x - 15, current_y,
                                       text=f"0x{self.total_memory:04X}",
                                       anchor=tk.E, font=("Courier", 9))
        
        # Legend - place after all segments
        legend_y = current_y + 30
        x = start_x
        
        self.memory_canvas.create_rectangle(x, legend_y, x + 20, legend_y + 20,
                                           fill="#34495e", outline="black")
        self.memory_canvas.create_text(x + 30, legend_y + 10, text="System Process",
                                       anchor=tk.W, font=("Arial", 9))
        
        x += 150
        self.memory_canvas.create_rectangle(x, legend_y, x + 20, legend_y + 20,
                                           fill="#3498db", outline="black")
        self.memory_canvas.create_text(x + 30, legend_y + 10, text="User Process",
                                       anchor=tk.W, font=("Arial", 9))
        
        x += 150
        self.memory_canvas.create_rectangle(x, legend_y, x + 20, legend_y + 20,
                                           fill="#ecf0f1", outline="black")
        self.memory_canvas.create_text(x + 30, legend_y + 10, text="Free Memory",
                                       anchor=tk.W, font=("Arial", 9))
        
        # Set scroll region to include all content
        total_height = legend_y + 50
        self.memory_canvas.configure(scrollregion=(0, 0, canvas_width, total_height))
    
    def update_stats(self):
        used_memory = sum(s.size for s in self.memory_segments if s.is_allocated)
        free_memory = self.total_memory - used_memory
        utilization = (used_memory / self.total_memory) * 100
        
        num_processes = len(self.processes)
        num_user = sum(1 for p in self.processes if p.process_type == "User")
        num_system = num_processes - num_user
        
        num_segments = len(self.memory_segments)
        num_free_segments = sum(1 for s in self.memory_segments if not s.is_allocated)
        
        stats = f"Processes: {num_processes} ({num_system} system, {num_user} user) | "
        stats += f"Memory: {used_memory}/{self.total_memory} KB ({utilization:.1f}%) | "
        stats += f"Segments: {num_segments} ({num_free_segments} free)"
        
        self.stats_label.config(text=stats)
    
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            # Scroll down
            self.memory_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            # Scroll up
            self.memory_canvas.yview_scroll(-1, "units")
