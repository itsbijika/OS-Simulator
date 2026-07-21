import tkinter as tk
from typing import List, Tuple


def generate_colors(n: int) -> List[str]:
    base_colors = [
        "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
        "#1abc9c", "#34495e", "#e67e22", "#95a5a6", "#d35400",
        "#c0392b", "#8e44ad", "#16a085", "#27ae60", "#2980b9",
        "#f1c40f", "#e74c3c", "#bdc3c7", "#7f8c8d", "#2c3e50"
    ]
    
    # Repeat colors if needed
    colors = []
    for i in range(n):
        colors.append(base_colors[i % len(base_colors)])
    
    return colors


def lighten_color(color: str, factor: float = 0.3) -> str:
    # Remove '#' and convert to RGB
    color = color.lstrip('#')
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    
    # Lighten
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    
    return f"#{r:02x}{g:02x}{b:02x}"


def darken_color(color: str, factor: float = 0.3) -> str:
    # Remove '#' and convert to RGB
    color = color.lstrip('#')
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    
    # Darken
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))
    
    return f"#{r:02x}{g:02x}{b:02x}"


def draw_arrow(canvas: tk.Canvas, x1: float, y1: float, x2: float, y2: float,
               color: str = "black", width: int = 2) -> None:
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width, arrow=tk.LAST)


def draw_grid(canvas: tk.Canvas, x_start: float, y_start: float,
              width: float, height: float, grid_size: int = 50,
              color: str = "#e0e0e0") -> None:
    # Vertical lines
    x = x_start
    while x <= x_start + width:
        canvas.create_line(x, y_start, x, y_start + height,
                          fill=color, dash=(2, 2))
        x += grid_size
    
    # Horizontal lines
    y = y_start
    while y <= y_start + height:
        canvas.create_line(x_start, y, x_start + width, y,
                          fill=color, dash=(2, 2))
        y += grid_size


def calculate_average(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def format_time(milliseconds: int) -> str:
    if milliseconds < 1000:
        return f"{milliseconds}ms"
    
    seconds = milliseconds / 1000
    if seconds < 60:
        return f"{seconds:.2f}s"
    
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes}m {seconds:.2f}s"


def create_tooltip(widget: tk.Widget, text: str) -> None:
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = tk.Label(tooltip, text=text, background="lightyellow",
                        relief=tk.SOLID, borderwidth=1, font=("Arial", 9))
        label.pack()
        
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)


def validate_numeric_input(text: str, allow_negative: bool = False,
                           allow_decimal: bool = False) -> bool:
    if not text:
        return True
    
    try:
        if allow_decimal:
            value = float(text)
        else:
            value = int(text)
        
        if not allow_negative and value < 0:
            return False
        
        return True
    except ValueError:
        return False


def center_window(window: tk.Tk | tk.Toplevel, width: int = None,
                  height: int = None) -> None:
    window.update_idletasks()
    
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f'{width}x{height}+{x}+{y}')


def create_styled_button(parent: tk.Widget, text: str, command,
                        bg_color: str = "#3498db", fg_color: str = "white",
                        width: int = 15, height: int = 2) -> tk.Button:
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        font=("Arial", 10, "bold"),
        width=width,
        height=height,
        cursor="hand2",
        relief=tk.FLAT,
        activebackground=darken_color(bg_color, 0.2),
        activeforeground=fg_color
    )
    
    return button


def create_info_label(parent: tk.Widget, text: str,
                     bg_color: str = "#ecf0f1") -> tk.Label:
    label = tk.Label(
        parent,
        text=text,
        font=("Arial", 10),
        bg=bg_color,
        fg="#2c3e50",
        padx=10,
        pady=5,
        justify=tk.LEFT,
        wraplength=400
    )
    
    return label


def show_algorithm_info(algorithm_name: str, description: str,
                       time_complexity: str, space_complexity: str) -> None:
    info_window = tk.Toplevel()
    info_window.title(f"{algorithm_name} - Algorithm Information")
    info_window.geometry("500x400")
    info_window.configure(bg="white")
    
    center_window(info_window, 500, 400)
    
    # Title
    title_label = tk.Label(
        info_window,
        text=algorithm_name,
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#2c3e50"
    )
    title_label.pack(pady=20)
    
    # Description
    desc_frame = tk.Frame(info_window, bg="white")
    desc_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    desc_label = tk.Label(
        desc_frame,
        text=description,
        font=("Arial", 11),
        bg="white",
        fg="#34495e",
        justify=tk.LEFT,
        wraplength=450
    )
    desc_label.pack(pady=10)
    
    # Complexity info
    complexity_frame = tk.LabelFrame(
        info_window,
        text="Complexity Analysis",
        font=("Arial", 12, "bold"),
        bg="white",
        padx=10,
        pady=10
    )
    complexity_frame.pack(fill=tk.X, padx=20, pady=10)
    
    time_label = tk.Label(
        complexity_frame,
        text=f"Time Complexity: {time_complexity}",
        font=("Arial", 10),
        bg="white",
        fg="#16a085"
    )
    time_label.pack(anchor=tk.W, pady=5)
    
    space_label = tk.Label(
        complexity_frame,
        text=f"Space Complexity: {space_complexity}",
        font=("Arial", 10),
        bg="white",
        fg="#16a085"
    )
    space_label.pack(anchor=tk.W, pady=5)
    
    # Close button
    close_btn = create_styled_button(
        info_window,
        "Close",
        info_window.destroy,
        bg_color="#95a5a6"
    )
    close_btn.pack(pady=20)


class AnimationController:
    
    def __init__(self):
        self.is_playing = False
        self.current_step = 0
        self.max_steps = 0
        self.delay = 1000  # milliseconds
        self.callbacks = []
    
    def set_steps(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_step = 0
    
    def add_callback(self, callback) -> None:
        self.callbacks.append(callback)
    
    def step_forward(self) -> bool:
        if self.current_step < self.max_steps:
            self.current_step += 1
            self._execute_callbacks()
            return True
        return False
    
    def step_backward(self) -> bool:
        if self.current_step > 0:
            self.current_step -= 1
            self._execute_callbacks()
            return True
        return False
    
    def reset(self) -> None:
        self.current_step = 0
        self.is_playing = False
        self._execute_callbacks()
    
    def play(self, root: tk.Tk) -> None:
        self.is_playing = True
        self._auto_play(root)
    
    def pause(self) -> None:
        self.is_playing = False
    
    def _auto_play(self, root: tk.Tk) -> None:
        if self.is_playing:
            if self.step_forward():
                root.after(self.delay, lambda: self._auto_play(root))
            else:
                self.is_playing = False
    
    def _execute_callbacks(self) -> None:
        for callback in self.callbacks:
            callback(self.current_step)


# Algorithm information database
ALGORITHM_INFO = {
    "FCFS": {
        "name": "First Come First Serve",
        "description": "Processes are executed in the order they arrive. Simple and fair, "
                      "but may lead to convoy effect where short processes wait for long ones.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    "SJF": {
        "name": "Shortest Job First",
        "description": "Selects the process with the smallest burst time. Minimizes average "
                      "waiting time but may cause starvation of longer processes.",
        "time_complexity": "O(n²) or O(n log n) with priority queue",
        "space_complexity": "O(1)"
    },
    "Priority": {
        "name": "Priority Scheduling",
        "description": "Processes are executed based on priority. Lower priority number means "
                      "higher priority. May cause starvation of low-priority processes.",
        "time_complexity": "O(n²) or O(n log n) with priority queue",
        "space_complexity": "O(1)"
    },
    "RR": {
        "name": "Round Robin",
        "description": "Each process gets a small time quantum in circular order. Fair and "
                      "responsive but context switching overhead can be high.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n) for queue"
    },
    "FirstFit": {
        "name": "First Fit",
        "description": "Allocates the first available block that is large enough. Fast but "
                      "may lead to external fragmentation.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    "BestFit": {
        "name": "Best Fit",
        "description": "Allocates the smallest block that is large enough. Minimizes wasted "
                      "space but slower than First Fit.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    "WorstFit": {
        "name": "Worst Fit",
        "description": "Allocates the largest available block. Leaves large fragments but "
                      "may lead to more fragmentation overall.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    }
}
