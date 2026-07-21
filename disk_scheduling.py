# Disk Scheduling Module for Operating System Algorithm Simulator
import tkinter as tk
from tkinter import ttk, messagebox


class DiskSchedulingModule:
    def __init__(self, parent, back_callback):
        self.parent = parent
        self.back_callback = back_callback
        self.requests = []
        self.seek_sequence = []
        self.total_seek_time = 0
        
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
            text="Disk Scheduling Algorithms",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=20)
        
        # Main content area
        content_frame = tk.Frame(self.parent, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel with scrollbar - Input and Controls
        left_container = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        left_container.config(width=350)
        left_container.pack_propagate(False)
        
        # Canvas for scrolling
        left_canvas = tk.Canvas(left_container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(left_container, orient=tk.VERTICAL, command=left_canvas.yview)
        left_panel = tk.Frame(left_canvas, bg="white")
        
        left_panel.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=left_panel, anchor="nw")
        left_canvas.configure(yscrollcommand=scrollbar.set)
        
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(left_panel, text="Select Algorithm",
                                   font=("Arial", 10, "bold"), bg="white", padx=8, pady=5)
        algo_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = [("FCFS", "FCFS"), ("SSTF", "SSTF"),
                     ("SCAN", "SCAN"), ("C-SCAN", "CSCAN"),
                     ("LOOK", "LOOK"), ("C-LOOK", "CLOOK")]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var,
                               value=value, bg="white", font=("Arial", 10))
            rb.pack(anchor=tk.W)
        
        # Disk parameters
        params_frame = tk.LabelFrame(left_panel, text="Disk Parameters",
                                     font=("Arial", 10, "bold"), bg="white", padx=8, pady=5)
        params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Initial head position
        head_frame = tk.Frame(params_frame, bg="white")
        head_frame.pack(fill=tk.X, pady=2)
        tk.Label(head_frame, text="Initial Head Pos:", width=15, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.initial_head_var = tk.StringVar(value="50")
        tk.Entry(head_frame, textvariable=self.initial_head_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Disk size
        size_frame = tk.Frame(params_frame, bg="white")
        size_frame.pack(fill=tk.X, pady=2)
        tk.Label(size_frame, text="Disk Size:", width=15, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.disk_size_var = tk.StringVar(value="200")
        tk.Entry(size_frame, textvariable=self.disk_size_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Direction (for SCAN/LOOK)
        dir_frame = tk.Frame(params_frame, bg="white")
        dir_frame.pack(fill=tk.X, pady=5)
        tk.Label(dir_frame, text="Direction (SCAN/LOOK):", bg="white",
                font=("Arial", 9)).pack(anchor=tk.W)
        
        self.direction_var = tk.StringVar(value="right")
        dir_buttons = tk.Frame(params_frame, bg="white")
        dir_buttons.pack(fill=tk.X)
        tk.Radiobutton(dir_buttons, text="Left", variable=self.direction_var,
                      value="left", bg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(dir_buttons, text="Right", variable=self.direction_var,
                      value="right", bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Request input
        request_frame = tk.LabelFrame(left_panel, text="Add Disk Request",
                                      font=("Arial", 10, "bold"), bg="white", padx=8, pady=5)
        request_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Request position
        req_frame = tk.Frame(request_frame, bg="white")
        req_frame.pack(fill=tk.X, pady=2)
        tk.Label(req_frame, text="Track Number:", width=15, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.request_var = tk.StringVar(value="82")
        tk.Entry(req_frame, textvariable=self.request_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Add request button
        tk.Button(request_frame, text="Add Request", command=self.add_request,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=(10, 5))
        
        # Quick setup
        tk.Button(request_frame, text="Quick Setup (Example)", command=self.quick_setup,
                 bg="#16a085", fg="white", font=("Arial", 9),
                 cursor="hand2").pack(pady=(0, 0))
        
        # Requests list
        list_frame = tk.LabelFrame(left_panel, text="Request Queue",
                                   font=("Arial", 10, "bold"), bg="white", padx=5, pady=3)
        list_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Listbox for requests
        self.request_listbox = tk.Listbox(list_frame, font=("Arial", 9), height=5)
        self.request_listbox.pack(fill=tk.X, padx=3, pady=3)
        
        # Control buttons
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Prominent Simulate button
        tk.Button(btn_frame, text="▶ RUN SIMULATION", command=self.simulate,
                 bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=6).pack(fill=tk.X, pady=(2, 5))
        
        tk.Button(btn_frame, text="Clear All", command=self.clear_requests,
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold"),
                 cursor="hand2").pack(fill=tk.X, pady=1)
        tk.Button(btn_frame, text="Reset", command=self.reset_simulation,
                 bg="#95a5a6", fg="white", font=("Arial", 9, "bold"),
                 cursor="hand2").pack(fill=tk.X, pady=1)
        
        # Right panel - Visualization
        right_panel = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
        
        # Canvas for disk head movement
        canvas_frame = tk.LabelFrame(right_panel, text="Disk Head Movement",
                                     font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0, height=400, width=700)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Results frame
        results_frame = tk.LabelFrame(right_panel, text="Results & Statistics",
                                      font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        results_frame.pack(fill=tk.X, padx=10, pady=(0, 10), side=tk.BOTTOM)
        
        self.results_text = tk.Text(results_frame, height=8, font=("Courier", 9),
                                   bg="#f8f9fa", relief=tk.FLAT)
        self.results_text.pack(fill=tk.X, padx=5, pady=5)
    
    
    
    def add_request(self):
        try:
            track = int(self.request_var.get())
            disk_size = int(self.disk_size_var.get())
            
            if track < 0 or track >= disk_size:
                messagebox.showerror("Error",
                                    f"Track number must be between 0 and {disk_size-1}")
                return
            
            self.requests.append(track)
            self.request_listbox.insert(tk.END, f"Track {track}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def quick_setup(self):
        self.clear_requests()
        # Classic example: requests at tracks 98, 183, 37, 122, 14, 124, 65, 67
        example_requests = [98, 183, 37, 122, 14, 124, 65, 67]
        
        for track in example_requests:
            self.requests.append(track)
            self.request_listbox.insert(tk.END, f"Track {track}")
    
    def clear_requests(self):
        self.requests.clear()
        self.request_listbox.delete(0, tk.END)
        self.reset_simulation()
    
    def reset_simulation(self):
        self.seek_sequence.clear()
        self.total_seek_time = 0
        self.canvas.delete("all")
        self.results_text.delete(1.0, tk.END)
    
    def simulate(self):
        if not self.requests:
            messagebox.showwarning("Warning", "Please add at least one disk request")
            return
        
        try:
            initial_head = int(self.initial_head_var.get())
            disk_size = int(self.disk_size_var.get())
            
            if initial_head < 0 or initial_head >= disk_size:
                messagebox.showerror("Error",
                                    f"Initial head position must be between 0 and {disk_size-1}")
                return
            
            self.reset_simulation()
            algorithm = self.algorithm_var.get()
            
            if algorithm == "FCFS":
                self.simulate_fcfs(initial_head)
            elif algorithm == "SSTF":
                self.simulate_sstf(initial_head)
            elif algorithm == "SCAN":
                self.simulate_scan(initial_head, disk_size)
            elif algorithm == "CSCAN":
                self.simulate_cscan(initial_head, disk_size)
            elif algorithm == "LOOK":
                self.simulate_look(initial_head)
            elif algorithm == "CLOOK":
                self.simulate_clook(initial_head)
            
            self.draw_visualization()
            self.display_results()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def simulate_fcfs(self, initial_head):
        self.seek_sequence = [initial_head]
        current_position = initial_head
        
        for request in self.requests:
            # Move to requested track
            seek_distance = abs(request - current_position)
            self.total_seek_time += seek_distance
            current_position = request
            self.seek_sequence.append(current_position)
    
    def simulate_sstf(self, initial_head):
        self.seek_sequence = [initial_head]
        current_position = initial_head
        remaining_requests = self.requests.copy()
        
        while remaining_requests:
            # Find closest request
            closest = min(remaining_requests, key=lambda x: abs(x - current_position))
            
            # Move to closest request
            seek_distance = abs(closest - current_position)
            self.total_seek_time += seek_distance
            current_position = closest
            self.seek_sequence.append(current_position)
            
            remaining_requests.remove(closest)
    
    def simulate_scan(self, initial_head, disk_size):
        self.seek_sequence = [initial_head]
        current_position = initial_head
        direction = self.direction_var.get()
        
        # Separate requests into left and right of current position
        left_requests = sorted([r for r in self.requests if r < current_position], reverse=True)
        right_requests = sorted([r for r in self.requests if r >= current_position])
        
        if direction == "right":
            # Service right side first
            for request in right_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
            
            # Go to end if there were requests on right
            if right_requests:
                seek_distance = abs((disk_size - 1) - current_position)
                self.total_seek_time += seek_distance
                current_position = disk_size - 1
                self.seek_sequence.append(current_position)
            
            # Service left side
            for request in left_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
        else:
            # Service left side first
            for request in left_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
            
            # Go to beginning if there were requests on left
            if left_requests:
                seek_distance = abs(0 - current_position)
                self.total_seek_time += seek_distance
                current_position = 0
                self.seek_sequence.append(current_position)
            
            # Service right side
            for request in right_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
    
    def simulate_cscan(self, initial_head, disk_size):
        self.seek_sequence = [initial_head]
        current_position = initial_head
        
        # Separate requests into left and right
        left_requests = sorted([r for r in self.requests if r < current_position])
        right_requests = sorted([r for r in self.requests if r >= current_position])
        
        # Always move right first in C-SCAN
        # Service right side
        for request in right_requests:
            seek_distance = abs(request - current_position)
            self.total_seek_time += seek_distance
            current_position = request
            self.seek_sequence.append(current_position)
        
        # Go to end if we serviced any right requests
        if right_requests:
            seek_distance = abs((disk_size - 1) - current_position)
            self.total_seek_time += seek_distance
            current_position = disk_size - 1
            self.seek_sequence.append(current_position)
            
            # Jump to beginning (count this as seek time)
            seek_distance = disk_size - 1
            self.total_seek_time += seek_distance
            current_position = 0
            self.seek_sequence.append(current_position)
        
        # Service left side (which is now in front)
        for request in left_requests:
            seek_distance = abs(request - current_position)
            self.total_seek_time += seek_distance
            current_position = request
            self.seek_sequence.append(current_position)
    
    def simulate_look(self, initial_head):
        self.seek_sequence = [initial_head]
        current_position = initial_head
        direction = self.direction_var.get()
        
        # Separate requests into left and right
        left_requests = sorted([r for r in self.requests if r < current_position], reverse=True)
        right_requests = sorted([r for r in self.requests if r >= current_position])
        
        if direction == "right":
            # Service right side
            for request in right_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
            
            # Service left side
            for request in left_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
        else:
            # Service left side
            for request in left_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
            
            # Service right side
            for request in right_requests:
                seek_distance = abs(request - current_position)
                self.total_seek_time += seek_distance
                current_position = request
                self.seek_sequence.append(current_position)
    
    def simulate_clook(self, initial_head):
        self.seek_sequence = [initial_head]
        current_position = initial_head
        
        # Separate requests into left and right
        left_requests = sorted([r for r in self.requests if r < current_position])
        right_requests = sorted([r for r in self.requests if r >= current_position])
        
        # Service right side
        for request in right_requests:
            seek_distance = abs(request - current_position)
            self.total_seek_time += seek_distance
            current_position = request
            self.seek_sequence.append(current_position)
        
        # Jump to first request on left (if any)
        if left_requests and right_requests:
            # Jump from last right request to first left request
            first_left = left_requests[0]
            seek_distance = abs(first_left - current_position)
            self.total_seek_time += seek_distance
            current_position = first_left
            self.seek_sequence.append(current_position)
            left_requests = left_requests[1:]  # Remove first as we just serviced it
        
        # Service remaining left side
        for request in left_requests:
            seek_distance = abs(request - current_position)
            self.total_seek_time += seek_distance
            current_position = request
            self.seek_sequence.append(current_position)
    
    def draw_visualization(self):
        self.canvas.delete("all")
        
        if not self.seek_sequence:
            return
        
        # Get canvas dimensions
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas has no size, use defaults
        if canvas_width < 100:
            canvas_width = 700
        if canvas_height < 100:
            canvas_height = 400
        
        # Calculate dimensions
        disk_size = int(self.disk_size_var.get())
        scale = (canvas_width - 60) / disk_size
        y_spacing = (canvas_height - 50) / len(self.seek_sequence) if len(self.seek_sequence) > 1 else 30
        x_start = 40
        y_top = 30
        
        # Draw horizontal axis (track numbers)
        self.canvas.create_line(x_start, y_top, x_start + (canvas_width - 60), y_top,
                               fill="#7f8c8d", width=2)
        
        # Draw tick marks and labels on axis
        tick_interval = max(1, disk_size // 10) if disk_size > 0 else 20
        tick_positions = list(range(0, disk_size - 1, tick_interval))
        # Always add the last track number (disk_size - 1)
        tick_positions.append(disk_size - 1)
        
        for i in tick_positions:
            x = x_start + i * scale
            self.canvas.create_line(x, y_top - 5, x, y_top + 5, 
                                   fill="#95a5a6", width=1)
            self.canvas.create_text(x, y_top - 12, text=str(i),
                                   font=("Arial", 8), fill="#7f8c8d")
        
        # Color palette for lines
        colors = ['#00d4aa', '#3fb950', '#d29922', '#f85149', '#a371f7',
                  '#79c0ff', '#ff7b72', '#7ee787', '#ffa657', '#d2a8ff']
        
        # Start position
        prev_x = x_start + self.seek_sequence[0] * scale
        prev_y = y_top + 15
        
        # Draw start marker
        marker_size = 6
        self.canvas.create_oval(prev_x - marker_size, prev_y - marker_size, 
                               prev_x + marker_size, prev_y + marker_size,
                               fill="#2ecc71", outline="")
        self.canvas.create_text(prev_x, prev_y + 15, 
                               text=f"Start: {self.seek_sequence[0]}",
                               font=("Arial", 8), fill="#2c3e50")
        
        # Draw movement path
        for i in range(1, len(self.seek_sequence)):
            curr_x = x_start + self.seek_sequence[i] * scale
            curr_y = prev_y + y_spacing
            color = colors[(i - 1) % len(colors)]
            
            # Draw line with arrow
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                   fill=color, width=2, arrow=tk.LAST, 
                                   arrowshape=(10, 12, 5))
            
            # Check if this is a requested track or intermediate
            is_request = self.seek_sequence[i] in self.requests
            point_color = "#e74c3c" if is_request else "#95a5a6"
            point_size = 4 if is_request else 3
            
            # Draw point
            self.canvas.create_oval(curr_x - point_size, curr_y - point_size,
                                   curr_x + point_size, curr_y + point_size,
                                   fill=point_color, outline="")
            
            # Draw label
            self.canvas.create_text(curr_x + 20, curr_y, 
                                   text=str(self.seek_sequence[i]),
                                   font=("Arial", 8), fill="#2c3e50")
            
            prev_x = curr_x
            prev_y = curr_y
    
    def display_results(self):
        self.results_text.delete(1.0, tk.END)
        
        # Header
        self.results_text.insert(tk.END, f"{'='*60}\n")
        self.results_text.insert(tk.END, f" {self.algorithm_var.get()} Disk Scheduling Results\n")
        self.results_text.insert(tk.END, f"{'='*60}\n\n")
        
        # Display seek sequence
        self.results_text.insert(tk.END, "Seek Sequence:\n")
        sequence_str = " → ".join(str(track) for track in self.seek_sequence)
        
        # Word wrap for long sequences
        words = sequence_str.split(" → ")
        line = ""
        for i, word in enumerate(words):
            if len(line) + len(word) + 4 > 60:
                self.results_text.insert(tk.END, f"  {line}→\n")
                line = word
            else:
                if line:
                    line += " → " + word
                else:
                    line = word
        if line:
            self.results_text.insert(tk.END, f"  {line}\n")
        
        self.results_text.insert(tk.END, f"\n{'-'*60}\n")
        
        # Display statistics
        self.results_text.insert(tk.END, f"Initial Head Position:  {self.seek_sequence[0]}\n")
        self.results_text.insert(tk.END, f"Total Requests:         {len(self.requests)}\n")
        self.results_text.insert(tk.END, f"Total Seek Time:        {self.total_seek_time} tracks\n")
        
        if len(self.requests) > 0:
            avg_seek = self.total_seek_time / len(self.requests)
            self.results_text.insert(tk.END, f"Average Seek Time:      {avg_seek:.2f} tracks/request\n")
        
        self.results_text.insert(tk.END, f"{'='*60}\n")
        
        # Show individual movements
        self.results_text.insert(tk.END, f"\nDetailed Movements:\n")
        for i in range(len(self.seek_sequence) - 1):
            from_track = self.seek_sequence[i]
            to_track = self.seek_sequence[i + 1]
            distance = abs(to_track - from_track)
            
            if i == 0:
                self.results_text.insert(tk.END,
                                        f"  Start: {from_track} → {to_track} "
                                        f"(seek: {distance})\n")
            else:
                self.results_text.insert(tk.END,
                                        f"  {from_track} → {to_track} "
                                        f"(seek: {distance})\n")
