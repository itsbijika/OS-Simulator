import tkinter as tk
import cpu_scheduling
import memory_management
import disk_scheduling
import process_manager
import file_management
import page_replacement
from theme import (
    FONT, BG_APP, BG_HEADER, BG_CARD, BORDER, TEXT_DARK, TEXT_MUTED,
    MODULE_COLORS, make_button, make_card
)


class OSSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Operating System Algorithm Simulator")
        self.root.geometry("1200x820")
        self.root.configure(bg=BG_APP)

        self.center_window()

        self.main_frame = tk.Frame(root, bg=BG_APP)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.show_home()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_frame()

        self.build_hero()

        # Scrollable container for module cards
        container = tk.Frame(self.main_frame, bg=BG_APP)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 0))

        canvas = tk.Canvas(container, bg=BG_APP, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        grid_frame = tk.Frame(canvas, bg=BG_APP)

        canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        modules = [
            ("🧮", "Process Manager", "Create processes with live memory allocation",
             self.show_process_manager),
            ("⚡", "CPU Scheduling", "FCFS, SJF, Priority, and Round Robin with Gantt charts",
             self.show_cpu_scheduling),
            ("💾", "Memory Management", "First Fit, Best Fit, and Worst Fit allocation",
             self.show_memory_management),
            ("💿", "Disk Scheduling", "FCFS, SSTF, SCAN, C-SCAN, LOOK, and C-LOOK",
             self.show_disk_scheduling),
            ("📁", "File Allocation", "Contiguous, linked, and indexed allocation methods",
             self.show_file_management),
            ("🗂", "Page Replacement", "FIFO, LRU, Optimal, and Clock algorithms",
             self.show_page_replacement),
        ]

        columns = 2
        for i, (icon, title, description, command) in enumerate(modules):
            row, col = divmod(i, columns)
            accent, accent_dark, accent_light = MODULE_COLORS[i % len(MODULE_COLORS)]
            self.build_module_card(grid_frame, icon, title, description, command,
                                   accent, accent_dark, accent_light, row, col)

        grid_frame.grid_columnconfigure(0, weight=1, uniform="col")
        grid_frame.grid_columnconfigure(1, weight=1, uniform="col")

        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        grid_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    def build_hero(self):
        hero = tk.Frame(self.main_frame, bg=BG_HEADER)
        hero.pack(fill=tk.X)

        inner = tk.Frame(hero, bg=BG_HEADER)
        inner.pack(pady=28)

        tk.Label(inner, text="🖥  OS Algorithm Simulator",
                font=(FONT, 26, "bold"), bg=BG_HEADER, fg="white").pack()

    def build_module_card(self, parent, icon, title, description, command,
                          accent, accent_dark, accent_light, row, col):
        outer, card = make_card(parent, bg=BG_CARD)
        outer.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)

        # Icon badge
        badge = tk.Frame(pad, bg=accent_light, width=52, height=52)
        badge.pack(anchor=tk.W)
        badge.pack_propagate(False)
        tk.Label(badge, text=icon, font=(FONT, 20), bg=accent_light).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(pad, text=title, font=(FONT, 15, "bold"), bg=BG_CARD,
                fg=TEXT_DARK, anchor=tk.W).pack(fill=tk.X, pady=(12, 4))

        tk.Label(pad, text=description, font=(FONT, 9), bg=BG_CARD,
                fg=TEXT_MUTED, anchor=tk.W, justify=tk.LEFT,
                wraplength=380).pack(fill=tk.X, pady=(0, 14))

        btn = tk.Button(
            pad, text="Launch Module  →", command=command,
            bg=accent, fg="white", activebackground=accent_dark, activeforeground="white",
            font=(FONT, 10, "bold"), relief=tk.FLAT, bd=0, cursor="hand2",
            padx=14, pady=8, anchor=tk.W
        )
        btn.pack(fill=tk.X)

        def on_enter(_):
            btn.config(bg=accent_dark)

        def on_leave(_):
            btn.config(bg=accent)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)


    
    def show_cpu_scheduling(self):
        self.clear_frame()
        cpu_scheduling.CPUSchedulingModule(self.main_frame, self.show_home)

    def show_memory_management(self):
        self.clear_frame()
        memory_management.MemoryManagementModule(self.main_frame, self.show_home)

    def show_disk_scheduling(self):
        self.clear_frame()
        disk_scheduling.DiskSchedulingModule(self.main_frame, self.show_home)

    def show_process_manager(self):
        self.clear_frame()
        process_manager.ProcessManagerModule(self.main_frame, self.show_home)

    def show_file_management(self):
        self.clear_frame()
        file_management.FileManagementModule(self.main_frame, self.show_home)

    def show_page_replacement(self):
        self.clear_frame()
        page_replacement.PageReplacementModule(self.main_frame, self.show_home)


def main():
    root = tk.Tk()
    app = OSSimulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
