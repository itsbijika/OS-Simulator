import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import time


class DiskBlock:
    def __init__(self, block_num):
        self.block_num = block_num
        self.is_allocated = False
        self.file_name = None
        self.next_block = None
        self.is_index_block = False
        self.indexed_blocks = []


class FileEntry:
    def __init__(self, name, size, start_block=None):
        self.name = name
        self.size = size
        self.start_block = start_block
        self.blocks = []
        self.color = None


class FileManagementModule:
    def __init__(self, parent, back_callback):
        self.parent = parent
        self.back_callback = back_callback
        self.total_blocks = 64
        self.blocks = [DiskBlock(i) for i in range(self.total_blocks)]
        self.files = []
        self.selected_file = None
        self.animation_speed = 300
        
        self.colors = [
            "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#3f4b97",
            "#1abc9c", "#e67e22", "#95a5a6", "#34495e", "#16a085"
        ]
        self.used_colors = []
        
        self.setup_ui()
    
    def setup_ui(self):
        header_frame = tk.Frame(self.parent, bg="#495b92", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(
            header_frame,
            text="← Back to Home",
            font=("Arial", 11),
            bg="#495b92",
            fg="white",
            command=self.back_callback,
            cursor="hand2",
            relief=tk.FLAT
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title = tk.Label(
            header_frame,
            text="File Allocation Methods",
            font=("Arial", 18, "bold"),
            bg="#495b92",
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=20)
        
        content_frame = tk.Frame(self.parent, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        left_panel.config(width=350)
        left_panel.pack_propagate(False)
        
        algo_frame = tk.LabelFrame(left_panel, text="Allocation Method",
                                   font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        algo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.algorithm_var = tk.StringVar(value="Contiguous")
        algorithms = [
            ("Contiguous Allocation", "Contiguous"),
            ("Linked List Allocation", "Linked"),
            ("Indexed Allocation", "Indexed")
        ]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var,
                               value=value, bg="white", font=("Arial", 10),
                               command=self.on_algorithm_change)
            rb.pack(anchor=tk.W)
        
        file_frame = tk.LabelFrame(left_panel, text="Create File",
                                   font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        name_frame = tk.Frame(file_frame, bg="white")
        name_frame.pack(fill=tk.X, pady=2)
        tk.Label(name_frame, text="File Name:", width=12, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.filename_var = tk.StringVar(value="file1.txt")
        tk.Entry(name_frame, textvariable=self.filename_var, width=12,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        size_frame = tk.Frame(file_frame, bg="white")
        size_frame.pack(fill=tk.X, pady=2)
        tk.Label(size_frame, text="Size (KB):", width=12, anchor='w',
                bg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.filesize_var = tk.StringVar(value="4")
        tk.Entry(size_frame, textvariable=self.filesize_var, width=12,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        tk.Button(file_frame, text="Create & Allocate File", command=self.create_file,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=(10, 0))
        
        files_list_frame = tk.LabelFrame(left_panel, text="Files on Disk",
                                         font=("Arial", 11, "bold"), bg="white", padx=5, pady=5)
        files_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Name", "Size", "Blocks")
        self.files_tree = ttk.Treeview(files_list_frame, columns=columns, show="headings", height=8)
        self.files_tree.heading("Name", text="Name")
        self.files_tree.heading("Size", text="Size")
        self.files_tree.heading("Blocks", text="Blocks")
        
        self.files_tree.column("Name", width=100)
        self.files_tree.column("Size", width=50)
        self.files_tree.column("Blocks", width=80)
        
        self.files_tree.pack(fill=tk.BOTH, expand=True)
        self.files_tree.bind('<<TreeviewSelect>>', self.on_file_select)
        
        tk.Button(files_list_frame, text="Delete Selected File", command=self.delete_file,
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=(5, 0))
        
        control_frame = tk.Frame(left_panel, bg="white")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(control_frame, text="Reset Disk", command=self.reset_disk,
                 bg="#95a5a6", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        
        right_panel = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
        
        disk_frame = tk.LabelFrame(right_panel, text="Disk Blocks",
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        disk_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas_container = tk.Frame(disk_frame, bg="white")
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.disk_canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
        self.disk_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.disk_canvas.bind('<Button-1>', self.on_block_click)
        
        legend_frame = tk.Frame(right_panel, bg="white", padx=10, pady=5)
        legend_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(legend_frame, text="Legend:", font=("Arial", 10, "bold"),
                bg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_legend_item(legend_frame, "#ecf0f1", "Free")
        self.create_legend_item(legend_frame, "#3498db", "Allocated")
        self.create_legend_item(legend_frame, "#e67e22", "Index Block")
        
        self.draw_disk()
    
    def create_legend_item(self, parent, color, text):
        frame = tk.Frame(parent, bg="white")
        frame.pack(side=tk.LEFT, padx=5)
        
        canvas = tk.Canvas(frame, width=20, height=20, bg="white", highlightthickness=0)
        canvas.pack(side=tk.LEFT)
        canvas.create_rectangle(2, 2, 18, 18, fill=color, outline="black")
        
        tk.Label(frame, text=text, font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=2)
    
    def on_algorithm_change(self):
        self.reset_disk()
    
    def get_next_color(self):
        available = [c for c in self.colors if c not in self.used_colors]
        if not available:
            self.used_colors.clear()
            available = self.colors
        color = random.choice(available)
        self.used_colors.append(color)
        return color
    
    def create_file(self):
        try:
            name = self.filename_var.get().strip()
            size = int(self.filesize_var.get())
            
            if not name:
                messagebox.showerror("Error", "File name cannot be empty")
                return
            
            if size <= 0 or size > self.total_blocks:
                messagebox.showerror("Error", f"Size must be between 1 and {self.total_blocks}")
                return
            
            if any(f.name == name for f in self.files):
                messagebox.showerror("Error", "File with this name already exists")
                return
            
            free_blocks = sum(1 for b in self.blocks if not b.is_allocated)
            required_blocks = size + (1 if self.algorithm_var.get() == "Indexed" else 0)
            
            if free_blocks < required_blocks:
                messagebox.showerror("Error", f"Not enough free blocks. Need {required_blocks}, have {free_blocks}")
                return
            
            file_entry = FileEntry(name, size)
            file_entry.color = self.get_next_color()
            
            algo = self.algorithm_var.get()
            if algo == "Contiguous":
                success = self.allocate_contiguous(file_entry)
            elif algo == "Linked":
                success = self.allocate_linked(file_entry)
            else:
                success = self.allocate_indexed(file_entry)
            
            if success:
                self.files.append(file_entry)
                self.update_files_list()
                self.draw_disk()
                
                if name[-4:] != ".txt":
                    base = name.split('.')[0] if '.' in name else name
                    num = ''.join(filter(str.isdigit, base))
                    if num:
                        next_num = int(num) + 1
                        self.filename_var.set(f"file{next_num}.txt")
                    else:
                        self.filename_var.set(f"{base}2.txt")
                else:
                    base = name[:-4]
                    num = ''.join(filter(str.isdigit, base))
                    if num:
                        next_num = int(num) + 1
                        self.filename_var.set(f"file{next_num}.txt")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric size")
    
    def allocate_contiguous(self, file_entry):
        size = file_entry.size
        
        for start in range(self.total_blocks - size + 1):
            if all(not self.blocks[i].is_allocated for i in range(start, start + size)):
                file_entry.start_block = start
                for i in range(start, start + size):
                    self.blocks[i].is_allocated = True
                    self.blocks[i].file_name = file_entry.name
                    file_entry.blocks.append(i)
                return True
        
        messagebox.showerror("Error", "Cannot find contiguous space for file")
        return False
    
    def allocate_linked(self, file_entry):
        size = file_entry.size
        free_blocks = [i for i, b in enumerate(self.blocks) if not b.is_allocated]
        
        if len(free_blocks) < size:
            return False
        
        selected_blocks = random.sample(free_blocks, size)
        selected_blocks.sort()
        
        file_entry.start_block = selected_blocks[0]
        
        for idx, block_num in enumerate(selected_blocks):
            self.blocks[block_num].is_allocated = True
            self.blocks[block_num].file_name = file_entry.name
            file_entry.blocks.append(block_num)
            
            if idx < len(selected_blocks) - 1:
                self.blocks[block_num].next_block = selected_blocks[idx + 1]
            else:
                self.blocks[block_num].next_block = None
        
        return True
    
    def allocate_indexed(self, file_entry):
        size = file_entry.size
        free_blocks = [i for i, b in enumerate(self.blocks) if not b.is_allocated]
        
        if len(free_blocks) < size + 1:
            return False
        
        index_block = free_blocks[0]
        data_blocks = random.sample(free_blocks[1:], size)
        data_blocks.sort()
        
        self.blocks[index_block].is_allocated = True
        self.blocks[index_block].file_name = file_entry.name
        self.blocks[index_block].is_index_block = True
        self.blocks[index_block].indexed_blocks = data_blocks
        
        file_entry.start_block = index_block
        file_entry.blocks.append(index_block)
        
        for block_num in data_blocks:
            self.blocks[block_num].is_allocated = True
            self.blocks[block_num].file_name = file_entry.name
            file_entry.blocks.append(block_num)
        
        return True
    
    def delete_file(self):
        selection = self.files_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file to delete")
            return
        
        item = selection[0]
        values = self.files_tree.item(item, "values")
        filename = values[0]
        
        file_entry = next((f for f in self.files if f.name == filename), None)
        if not file_entry:
            return
        
        for block_num in file_entry.blocks:
            self.blocks[block_num].is_allocated = False
            self.blocks[block_num].file_name = None
            self.blocks[block_num].next_block = None
            self.blocks[block_num].is_index_block = False
            self.blocks[block_num].indexed_blocks = []
        
        if file_entry.color in self.used_colors:
            self.used_colors.remove(file_entry.color)
        
        self.files.remove(file_entry)
        self.update_files_list()
        self.draw_disk()
    
    def reset_disk(self):
        self.blocks = [DiskBlock(i) for i in range(self.total_blocks)]
        self.files.clear()
        self.used_colors.clear()
        self.selected_file = None
        self.update_files_list()
        self.draw_disk()
    
    def update_files_list(self):
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        for file_entry in self.files:
            blocks_str = f"{len(file_entry.blocks)} blocks"
            self.files_tree.insert("", tk.END, values=(file_entry.name, file_entry.size, blocks_str))
    
    def on_file_select(self, event):
        selection = self.files_tree.selection()
        if not selection:
            self.selected_file = None
            self.draw_disk()
            return
        
        item = selection[0]
        values = self.files_tree.item(item, "values")
        filename = values[0]
        
        self.selected_file = next((f for f in self.files if f.name == filename), None)
        self.draw_disk()
    
    def draw_disk(self):
        self.disk_canvas.delete("all")
        
        canvas_width = self.disk_canvas.winfo_width()
        canvas_height = self.disk_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 600
        
        rows = 8
        cols = 8
        
        margin = 20
        available_width = canvas_width - 2 * margin
        available_height = canvas_height - 2 * margin - 60
        
        block_size = min(available_width // cols, available_height // rows) - 5
        
        start_x = (canvas_width - (cols * (block_size + 5))) // 2
        start_y = 40
        
        self.disk_canvas.create_text(canvas_width // 2, 20,
                                     text=f"Disk Blocks (0-{self.total_blocks-1}) - {self.algorithm_var.get()} Allocation",
                                     font=("Arial", 12, "bold"))
        
        self.block_positions = {}
        
        for i in range(self.total_blocks):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (block_size + 5)
            y = start_y + row * (block_size + 5)
            
            self.block_positions[i] = (x + block_size // 2, y + block_size // 2)
            
            block = self.blocks[i]
            
            if block.is_allocated:
                file_entry = next((f for f in self.files if f.name == block.file_name), None)
                if file_entry:
                    fill_color = file_entry.color
                else:
                    fill_color = "#95a5a6"
                
                if block.is_index_block:
                    fill_color = "#e67e22"
            else:
                fill_color = "#ecf0f1"
            
            outline_color = "black"
            outline_width = 1
            
            if self.selected_file and block.file_name == self.selected_file.name:
                outline_color = "#2c3e50"
                outline_width = 3
            
            self.disk_canvas.create_rectangle(x, y, x + block_size, y + block_size,
                                             fill=fill_color, outline=outline_color,
                                             width=outline_width, tags=f"block_{i}")
            
            self.disk_canvas.create_text(x + block_size // 2, y + block_size // 2,
                                         text=str(i), font=("Arial", 10, "bold"),
                                         fill="white" if block.is_allocated else "black",
                                         tags=f"block_{i}")
            
            if block.is_index_block:
                self.disk_canvas.create_text(x + block_size // 2, y + block_size + 12,
                                            text="I", font=("Arial", 9, "bold"),
                                            fill="#e67e22", tags=f"block_{i}")
        
        if self.algorithm_var.get() == "Linked":
            for block in self.blocks:
                if block.is_allocated and block.next_block is not None:
                    from_pos = self.block_positions[block.block_num]
                    to_pos = self.block_positions[block.next_block]
                    
                    self.disk_canvas.create_line(from_pos[0], from_pos[1],
                                                 to_pos[0], to_pos[1],
                                                 arrow=tk.LAST, fill="#2c3e50",
                                                 width=2, dash=(4, 2))
        
        elif self.algorithm_var.get() == "Indexed":
            for block in self.blocks:
                if block.is_index_block and block.indexed_blocks:
                    from_pos = self.block_positions[block.block_num]
                    for data_block in block.indexed_blocks:
                        to_pos = self.block_positions[data_block]
                        self.disk_canvas.create_line(from_pos[0], from_pos[1],
                                                     to_pos[0], to_pos[1],
                                                     fill="#e67e22", width=1, dash=(2, 4))
    
    def on_block_click(self, event):
        x, y = event.x, event.y
        
        items = self.disk_canvas.find_overlapping(x, y, x, y)
        for item in items:
            tags = self.disk_canvas.gettags(item)
            for tag in tags:
                if tag.startswith("block_"):
                    block_num = int(tag.split("_")[1])
                    self.show_block_info(block_num)
                    return
    
    def show_block_info(self, block_num):
        block = self.blocks[block_num]
        
        if not block.is_allocated:
            info = f"Block {block_num}\nStatus: Free"
            messagebox.showinfo("Block Information", info)
            return
        
        info = f"Block {block_num}\nFile: {block.file_name}\n"
        
        if block.is_index_block:
            info += "Type: Index Block\n"
            info += f"Points to blocks: {', '.join(map(str, block.indexed_blocks))}"
            
            detail_window = tk.Toplevel(self.parent)
            detail_window.title(f"Index Block {block_num}")
            
            window_width = 320
            window_height = 170 + (len(block.indexed_blocks) * 30)
            detail_window.geometry(f"{window_width}x{window_height}")
            detail_window.configure(bg="white")
            
            tk.Label(detail_window, text=f"Index Block {block_num}",
                    font=("Arial", 14, "bold"), bg="white").pack(pady=10)
            
            tk.Label(detail_window, text=f"File: {block.file_name}",
                    font=("Arial", 11), bg="white").pack(pady=5)
            
            tk.Label(detail_window, text="Index Table:",
                    font=("Arial", 11, "bold"), bg="white").pack(pady=5)
            
            table_frame = tk.Frame(detail_window, bg="white")
            table_frame.pack(pady=5)
            
            for idx, data_block in enumerate(block.indexed_blocks):
                tk.Label(table_frame, text=f"{idx}: Block {data_block}",
                        font=("Arial", 10), bg="white",
                        relief=tk.RIDGE, padx=10, pady=2).pack()
            
            tk.Button(detail_window, text="Close", command=detail_window.destroy,
                     bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        elif block.next_block is not None:
            info += f"Type: Data Block (Linked)\nNext Block: {block.next_block}"
            messagebox.showinfo("Block Information", info)
        else:
            if self.algorithm_var.get() == "Linked" and block.is_allocated:
                info += "Type: Data Block (Linked)\nNext Block: NULL (End)"
            else:
                info += "Type: Data Block"
            messagebox.showinfo("Block Information", info)
