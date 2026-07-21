import tkinter as tk
from tkinter import ttk, messagebox
import time


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = -1


class CPUSchedulingModule:
    def __init__(self, parent, back_callback):
        self.parent = parent
        self.back_callback = back_callback
        self.processes = []
        self.gantt_data = []
        self.current_step = 0
        self.is_animating = False
        
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
            text="CPU Scheduling Algorithms",
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
        algo_frame = tk.LabelFrame(left_panel, text="Select Algorithm", font=("Arial", 11, "bold"),
                                   bg="white", padx=10, pady=10)
        algo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = [("FCFS", "FCFS"), ("SJF", "SJF"), 
                     ("Priority", "Priority"), ("Round Robin", "RR")]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var,
                               value=value, bg="white", font=("Arial", 10))
            rb.pack(anchor=tk.W)
        
        # Time Quantum for Round Robin
        tq_frame = tk.Frame(algo_frame, bg="white")
        tq_frame.pack(fill=tk.X, pady=(5, 0))
        tk.Label(tq_frame, text="Time Quantum (RR):", bg="white", 
                font=("Arial", 9)).pack(side=tk.LEFT)
        self.time_quantum_var = tk.StringVar(value="2")
        tk.Entry(tq_frame, textvariable=self.time_quantum_var, width=5,
                font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        # Process input
        input_frame = tk.LabelFrame(left_panel, text="Add Process", 
                                    font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # PID
        pid_frame = tk.Frame(input_frame, bg="white")
        pid_frame.pack(fill=tk.X, pady=2)
        tk.Label(pid_frame, text="Process ID:", width=12, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.pid_var = tk.StringVar(value="P1")
        tk.Entry(pid_frame, textvariable=self.pid_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Arrival Time
        at_frame = tk.Frame(input_frame, bg="white")
        at_frame.pack(fill=tk.X, pady=2)
        tk.Label(at_frame, text="Arrival Time:", width=12, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.arrival_var = tk.StringVar(value="0")
        tk.Entry(at_frame, textvariable=self.arrival_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Burst Time
        bt_frame = tk.Frame(input_frame, bg="white")
        bt_frame.pack(fill=tk.X, pady=2)
        tk.Label(bt_frame, text="Burst Time:", width=12, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.burst_var = tk.StringVar(value="5")
        tk.Entry(bt_frame, textvariable=self.burst_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Priority
        pr_frame = tk.Frame(input_frame, bg="white")
        pr_frame.pack(fill=tk.X, pady=2)
        tk.Label(pr_frame, text="Priority:", width=12, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.priority_var = tk.StringVar(value="1")
        tk.Entry(pr_frame, textvariable=self.priority_var, width=10,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Add button
        tk.Button(input_frame, text="Add Process", command=self.add_process,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=(10, 0))
        tk.Button(input_frame, text="Quick Setup (Example)", command=self.quick_setup,
                 bg="#16a085", fg="white", font=("Arial", 9), cursor="hand2").pack(pady=(5, 0))
        
        # Process list
        list_frame = tk.LabelFrame(left_panel, text="Process List",
                                   font=("Arial", 11, "bold"), bg="white", padx=5, pady=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for processes
        columns = ("PID", "AT", "BT", "Priority")
        self.process_tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                                         height=6)
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("AT", text="Arrival")
        self.process_tree.heading("BT", text="Burst")
        self.process_tree.heading("Priority", text="Priority")
        
        self.process_tree.column("PID", width=60)
        self.process_tree.column("AT", width=60)
        self.process_tree.column("BT", width=60)
        self.process_tree.column("Priority", width=60)
        
        self.process_tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(list_frame, text="Remove Selected", command=self.remove_selected_process,
             bg="#e67e22", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=(5, 0))
        
        # Control buttons
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Clear All", command=self.clear_processes,
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Simulate", command=self.simulate,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Reset Simulation", command=self.reset_simulation,
                 bg="#95a5a6", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        
        # Right panel - Visualization
        right_panel = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
        
        # Canvas for Gantt chart
        canvas_frame = tk.LabelFrame(right_panel, text="Gantt Chart",
                                     font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Results frame
        results_frame = tk.LabelFrame(right_panel, text="Results",
                                      font=("Arial", 12, "bold"), bg="white", padx=5, pady=5)
        results_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.results_text = tk.Text(results_frame, height=10, font=("Courier", 9),
                                   bg="#f8f9fa", relief=tk.FLAT)
        self.results_text.pack(fill=tk.X, padx=5, pady=5)
    
    def add_process(self):
        try:
            pid = self.pid_var.get().strip()
            arrival = int(self.arrival_var.get())
            burst = int(self.burst_var.get())
            priority = int(self.priority_var.get())
            
            if not pid:
                messagebox.showerror("Error", "Process ID cannot be empty")
                return
            
            if burst <= 0:
                messagebox.showerror("Error", "Burst time must be positive")
                return
            
            if arrival < 0:
                messagebox.showerror("Error", "Arrival time cannot be negative")
                return
            
            # Create process
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)
            
            # Add to treeview
            self.process_tree.insert("", tk.END, values=(pid, arrival, burst, priority))
            
            # Auto-increment PID
            if pid.startswith("P") and pid[1:].isdigit():
                next_num = int(pid[1:]) + 1
                self.pid_var.set(f"P{next_num}")
            
            # Clear other fields
            self.arrival_var.set("0")
            self.burst_var.set("5")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def quick_setup(self):
        self.clear_processes()
        sample_processes = [
            ("P1", 0, 8, 2),
            ("P2", 1, 4, 1),
            ("P3", 2, 9, 3),
            ("P4", 3, 5, 2)
        ]
        for pid, at, bt, pr in sample_processes:
            proc = Process(pid, at, bt, pr)
            self.processes.append(proc)
            self.process_tree.insert("", tk.END, values=(pid, at, bt, pr))
        # Set next PID suggestion
        self.pid_var.set("P5")
        self.arrival_var.set("0")
        self.burst_var.set("5")
        self.priority_var.set("1")
        # Ensure simulation visuals are reset
        self.reset_simulation()
    
    def clear_processes(self):
        self.processes.clear()
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        self.reset_simulation()

    def remove_selected_process(self):
        selection = self.process_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to remove")
            return

        item = selection[0]
        values = self.process_tree.item(item, "values")
        if values:
            pid = values[0]
            self.processes = [proc for proc in self.processes if proc.pid != pid]
        self.process_tree.delete(item)
        self.reset_simulation()
    
    def reset_simulation(self):
        self.gantt_data.clear()
        self.current_step = 0
        self.canvas.delete("all")
        self.results_text.delete(1.0, tk.END)
        
        # Reset process states
        for process in self.processes:
            process.remaining_time = process.burst_time
            process.completion_time = 0
            process.turnaround_time = 0
            process.waiting_time = 0
            process.start_time = -1
    
    def simulate(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add at least one process")
            return
        
        self.reset_simulation()
        algorithm = self.algorithm_var.get()
        
        if algorithm == "FCFS":
            self.simulate_fcfs()
        elif algorithm == "SJF":
            self.simulate_sjf()
        elif algorithm == "Priority":
            self.simulate_priority()
        elif algorithm == "RR":
            try:
                tq = int(self.time_quantum_var.get())
                if tq <= 0:
                    messagebox.showerror("Error", "Time quantum must be positive")
                    return
                self.simulate_round_robin(tq)
            except ValueError:
                messagebox.showerror("Error", "Invalid time quantum")
                return
        
        self.draw_gantt_chart()
        self.display_results()
    
    def simulate_fcfs(self):
        # Sort by arrival time
        sorted_processes = sorted(self.processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        
        for process in sorted_processes:
            # If process hasn't arrived yet, CPU is idle
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Process starts execution
            process.start_time = current_time
            
            # Add to Gantt chart
            self.gantt_data.append({
                'pid': process.pid,
                'start': current_time,
                'end': current_time + process.burst_time
            })
            
            # Process completes
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
    
    def simulate_sjf(self):
        completed = []
        current_time = 0
        
        while len(completed) < len(self.processes):
            # Find processes that have arrived and not completed
            available = [p for p in self.processes if p.arrival_time <= current_time 
                        and p not in completed]
            
            if not available:
                # CPU idle - jump to next arrival
                next_arrival = min(p.arrival_time for p in self.processes if p not in completed)
                current_time = next_arrival
                continue
            
            # Select process with shortest burst time
            selected = min(available, key=lambda p: p.burst_time)
            
            # Execute process
            selected.start_time = current_time
            self.gantt_data.append({
                'pid': selected.pid,
                'start': current_time,
                'end': current_time + selected.burst_time
            })
            
            current_time += selected.burst_time
            selected.completion_time = current_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            
            completed.append(selected)
    
    def simulate_priority(self):
        completed = []
        current_time = 0
        
        while len(completed) < len(self.processes):
            # Find processes that have arrived and not completed
            available = [p for p in self.processes if p.arrival_time <= current_time 
                        and p not in completed]
            
            if not available:
                # CPU idle - jump to next arrival
                next_arrival = min(p.arrival_time for p in self.processes if p not in completed)
                current_time = next_arrival
                continue
            
            # Select process with highest priority (lowest priority number)
            selected = min(available, key=lambda p: (p.priority, p.arrival_time))
            
            # Execute process
            selected.start_time = current_time
            self.gantt_data.append({
                'pid': selected.pid,
                'start': current_time,
                'end': current_time + selected.burst_time
            })
            
            current_time += selected.burst_time
            selected.completion_time = current_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            
            completed.append(selected)
    
    def simulate_round_robin(self, time_quantum):
        from collections import deque
        
        # Create a copy of processes to track remaining time
        process_queue = deque()
        current_time = 0
        completed = []
        
        # Sort by arrival time to handle arrivals correctly
        sorted_processes = sorted(self.processes, key=lambda p: p.arrival_time)
        process_index = 0
        
        # Add first arrived process(es) to queue
        while process_index < len(sorted_processes) and \
              sorted_processes[process_index].arrival_time <= current_time:
            process_queue.append(sorted_processes[process_index])
            process_index += 1
        
        while process_queue or process_index < len(sorted_processes):
            if not process_queue:
                # CPU idle - jump to next arrival
                current_time = sorted_processes[process_index].arrival_time
                process_queue.append(sorted_processes[process_index])
                process_index += 1
                continue
            
            # Get next process from queue
            process = process_queue.popleft()
            
            # Record start time if first execution
            if process.start_time == -1:
                process.start_time = current_time
            
            # Execute for time quantum or remaining time
            execution_time = min(time_quantum, process.remaining_time)
            
            # Add to Gantt chart
            self.gantt_data.append({
                'pid': process.pid,
                'start': current_time,
                'end': current_time + execution_time
            })
            
            current_time += execution_time
            process.remaining_time -= execution_time
            
            # Add newly arrived processes to queue
            while process_index < len(sorted_processes) and \
                  sorted_processes[process_index].arrival_time <= current_time:
                process_queue.append(sorted_processes[process_index])
                process_index += 1
            
            # Check if process is complete
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed.append(process)
            else:
                # Process not complete, add back to queue
                process_queue.append(process)
    
    def draw_gantt_chart(self):
        self.canvas.delete("all")
        
        if not self.gantt_data:
            return
        
        # Calculate dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 300
        
        # Margins
        margin_left = 50
        margin_right = 50
        margin_top = 50
        margin_bottom = 100
        
        chart_width = canvas_width - margin_left - margin_right
        chart_height = 80
        
        # Find time range
        max_time = max(item['end'] for item in self.gantt_data)
        time_scale = chart_width / max_time if max_time > 0 else 1
        
        # Title
        self.canvas.create_text(canvas_width // 2, 20,
                               text=f"Gantt Chart - {self.algorithm_var.get()} Scheduling",
                               font=("Arial", 14, "bold"))
        
        # Draw timeline
        y_pos = margin_top
        
        # Color palette for different processes
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", 
                 "#1abc9c", "#34495e", "#e67e22"]
        pid_colors = {}
        color_index = 0
        
        for item in self.gantt_data:
            pid = item['pid']
            if pid not in pid_colors:
                pid_colors[pid] = colors[color_index % len(colors)]
                color_index += 1
            
            x1 = margin_left + item['start'] * time_scale
            x2 = margin_left + item['end'] * time_scale
            y1 = y_pos
            y2 = y_pos + chart_height
            
            # Draw rectangle for process
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill=pid_colors[pid],
                                         outline="black",
                                         width=2)
            
            # Draw process ID in the middle
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                   text=pid,
                                   font=("Arial", 12, "bold"),
                                   fill="white")
            
            # Draw time markers at bottom
            self.canvas.create_line(x1, y2, x1, y2 + 10, width=2)
            self.canvas.create_text(x1, y2 + 25,
                                   text=str(item['start']),
                                   font=("Arial", 10))
        
        # Draw final time marker
        final_x = margin_left + max_time * time_scale
        self.canvas.create_line(final_x, y_pos + chart_height,
                               final_x, y_pos + chart_height + 10, width=2)
        self.canvas.create_text(final_x, y_pos + chart_height + 25,
                               text=str(max_time),
                               font=("Arial", 10))
        
        # Draw time axis label
        self.canvas.create_text(canvas_width // 2, y_pos + chart_height + 50,
                               text="Time",
                               font=("Arial", 11, "bold"))
    
    def display_results(self):
        self.results_text.delete(1.0, tk.END)
        
        # Header
        self.results_text.insert(tk.END, f"{'='*70}\n")
        self.results_text.insert(tk.END, f" {self.algorithm_var.get()} Scheduling Results\n")
        self.results_text.insert(tk.END, f"{'='*70}\n\n")
        
        # Process details table
        show_priority = self.algorithm_var.get() == "Priority"
        if show_priority:
            header = f"{'PID':<8} {'Arrival':<10} {'Burst':<10} {'Priority':<10} {'Complete':<10} {'TAT':<8} {'WT':<8}\n"
            divider = '-' * 80
        else:
            header = f"{'PID':<8} {'Arrival':<10} {'Burst':<10} {'Complete':<10} {'TAT':<8} {'WT':<8}\n"
            divider = '-' * 70
        self.results_text.insert(tk.END, header)
        self.results_text.insert(tk.END, f"{divider}\n")
        
        total_tat = 0
        total_wt = 0
        
        for process in sorted(self.processes, key=lambda p: p.arrival_time):
            if show_priority:
                row = f"{process.pid:<8} {process.arrival_time:<10} {process.burst_time:<10} " \
                      f"{process.priority:<10} {process.completion_time:<10} {process.turnaround_time:<8} {process.waiting_time:<8}\n"
            else:
                row = f"{process.pid:<8} {process.arrival_time:<10} {process.burst_time:<10} " \
                      f"{process.completion_time:<10} {process.turnaround_time:<8} {process.waiting_time:<8}\n"
            self.results_text.insert(tk.END, row)
            total_tat += process.turnaround_time
            total_wt += process.waiting_time
        
        # Calculate averages
        n = len(self.processes)
        avg_tat = total_tat / n
        avg_wt = total_wt / n
        
        if self.algorithm_var.get() == "RR":
            self.results_text.insert(tk.END, f"\n{divider}\n")
            ready_queue = " -> ".join(item['pid'] for item in self.gantt_data)
            self.results_text.insert(tk.END, f"Ready Queue: {ready_queue}\n")
        self.results_text.insert(tk.END, f"\n{divider}\n")
        self.results_text.insert(tk.END, f"Average Turnaround Time: {avg_tat:.2f}\n")
        self.results_text.insert(tk.END, f"Average Waiting Time: {avg_wt:.2f}\n")
        self.results_text.insert(tk.END, f"{'='*70}\n")
