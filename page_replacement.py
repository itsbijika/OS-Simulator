# Page Replacement Module for Operating System Algorithm Simulator
import tkinter as tk
from tkinter import messagebox
import utils
from theme import (
    FONT, BG_APP, BG_HEADER, BG_CARD, BORDER, ACCENT, ACCENT_DARK, ACCENT_LIGHT,
    SUCCESS, SUCCESS_DARK, SUCCESS_LIGHT, DANGER, DANGER_DARK, DANGER_LIGHT,
    WARNING, TEXT_DARK, TEXT_MUTED, TEXT_ON_DARK,
    make_button, make_card, section_title, build_header
)


class PageReplacementModule:
    def __init__(self, parent, back_callback):
        self.parent = parent
        self.back_callback = back_callback
        self.reference_string = []
        self.steps = []
        self.page_faults = 0
        self.page_hits = 0
        self.page_color_map = {}
        self.num_frames = 3

        self.anim = utils.AnimationController()
        self.anim.delay = 700
        self.anim.add_callback(self.on_step_change)

        self.setup_ui()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------
    def setup_ui(self):
        self.parent.configure(bg=BG_APP)

        self.build_header()

        content_frame = tk.Frame(self.parent, bg=BG_APP)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        self.build_left_panel(content_frame)
        self.build_right_panel(content_frame)

    def build_header(self):
        build_header(
            self.parent,
            "🗂  Page Replacement Algorithms",
            "Visualize how the OS decides which page to evict",
            back_callback=self.back_callback
        )

    def build_left_panel(self, content_frame):
        outer = tk.Frame(content_frame, bg=BG_APP, width=330)
        outer.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))
        outer.pack_propagate(False)

        canvas = tk.Canvas(outer, bg=BG_APP, highlightthickness=0)
        vscroll = tk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        panel = tk.Frame(canvas, bg=BG_APP)

        panel.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=panel, anchor="nw", width=310)
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # --- Algorithm card ---
        card_outer, card = make_card(panel)
        card_outer.pack(fill=tk.X, pady=(0, 12))
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.X, padx=16, pady=14)

        section_title(pad, "⚡", "Algorithm").pack(anchor=tk.W, pady=(0, 8))

        self.algorithm_var = tk.StringVar(value="FIFO")
        algo_options = [
            ("FIFO", "First In First Out"),
            ("LRU", "Least Recently Used"),
            ("Optimal", "Belady's Algorithm"),
            ("Basic", "Basic Page Replacement"),
        ]
        for value, label in algo_options:
            row = tk.Frame(pad, bg=BG_CARD)
            row.pack(fill=tk.X, pady=2)
            tk.Radiobutton(row, text=value, variable=self.algorithm_var, value=value,
                          bg=BG_CARD, fg=TEXT_DARK, selectcolor=ACCENT_LIGHT,
                          activebackground=BG_CARD, font=(FONT, 10, "bold"),
                          anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=label, bg=BG_CARD, fg=TEXT_MUTED,
                    font=(FONT, 8)).pack(side=tk.LEFT, padx=(4, 0))

        # --- Parameters card ---
        card_outer, card = make_card(panel)
        card_outer.pack(fill=tk.X, pady=(0, 12))
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.X, padx=16, pady=14)

        section_title(pad, "🎛", "Parameters").pack(anchor=tk.W, pady=(0, 8))

        tk.Label(pad, text="Number of Frames", bg=BG_CARD, fg=TEXT_MUTED,
                font=(FONT, 8)).pack(anchor=tk.W)
        self.num_frames_var = tk.StringVar(value="3")
        tk.Entry(pad, textvariable=self.num_frames_var, font=(FONT, 10),
                relief=tk.FLAT, highlightbackground=BORDER, highlightthickness=1,
                bg="#fafbff").pack(fill=tk.X, ipady=5, pady=(2, 10))

        tk.Label(pad, text="Reference String (comma separated)", bg=BG_CARD,
                fg=TEXT_MUTED, font=(FONT, 8)).pack(anchor=tk.W)
        self.ref_string_var = tk.StringVar(value="7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1")
        tk.Entry(pad, textvariable=self.ref_string_var, font=(FONT, 10),
                relief=tk.FLAT, highlightbackground=BORDER, highlightthickness=1,
                bg="#fafbff").pack(fill=tk.X, ipady=5, pady=(2, 10))

        make_button(pad, "Quick Setup (Classic Example)", self.quick_setup,
                   style="muted", font_size=9).pack(fill=tk.X)

        # --- Actions card ---
        card_outer, card = make_card(panel)
        card_outer.pack(fill=tk.X, pady=(0, 12))
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.X, padx=16, pady=14)

        section_title(pad, "▶", "Run").pack(anchor=tk.W, pady=(0, 8))

        make_button(pad, "Run Simulation", self.run_simulation,
                   style="primary", font_size=11).pack(fill=tk.X, pady=(0, 8))
        make_button(pad, "Compare All Algorithms", self.compare_algorithms,
                   style="success", font_size=10).pack(fill=tk.X, pady=(0, 8))
        make_button(pad, "Clear", self.clear_all,
                   style="danger", font_size=9).pack(fill=tk.X)

        # --- Speed card ---
        card_outer, card = make_card(panel)
        card_outer.pack(fill=tk.X, pady=(0, 12))
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.X, padx=16, pady=14)

        section_title(pad, "⏱", "Playback Speed").pack(anchor=tk.W, pady=(0, 8))

        self.speed_var = tk.StringVar(value="Normal")
        speed_row = tk.Frame(pad, bg=BG_CARD)
        speed_row.pack(fill=tk.X)
        for text, delay in [("Slow", 1400), ("Normal", 700), ("Fast", 300)]:
            tk.Radiobutton(speed_row, text=text, variable=self.speed_var, value=text,
                          bg=BG_CARD, fg=TEXT_DARK, selectcolor=ACCENT_LIGHT,
                          activebackground=BG_CARD, font=(FONT, 9),
                          command=lambda d=delay: self.set_speed(d)).pack(side=tk.LEFT, padx=(0, 8))

    def build_right_panel(self, content_frame):
        right = tk.Frame(content_frame, bg=BG_APP)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Timeline card ---
        card_outer, card = make_card(right)
        card_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.BOTH, expand=True, padx=16, pady=14)

        section_title(pad, "📊", "Frame Timeline").pack(anchor=tk.W, pady=(0, 10))

        # Playback control bar
        playback_bar = tk.Frame(pad, bg=ACCENT_LIGHT)
        playback_bar.pack(fill=tk.X, pady=(0, 10))
        inner_bar = tk.Frame(playback_bar, bg=ACCENT_LIGHT)
        inner_bar.pack(fill=tk.X, padx=8, pady=8)

        self.prev_btn = make_button(inner_bar, "⏮", self.step_backward,
                                    style="muted", state=tk.DISABLED, font_size=10)
        self.prev_btn.pack(side=tk.LEFT, padx=2)

        self.play_btn = make_button(inner_bar, "▶ Play", self.toggle_play,
                                    style="success", state=tk.DISABLED, font_size=10)
        self.play_btn.pack(side=tk.LEFT, padx=2)

        self.next_btn = make_button(inner_bar, "⏭", self.step_forward,
                                    style="muted", state=tk.DISABLED, font_size=10)
        self.next_btn.pack(side=tk.LEFT, padx=2)

        self.reset_btn = make_button(inner_bar, "⟲ Reset", self.reset_animation,
                                     style="muted", state=tk.DISABLED, font_size=10)
        self.reset_btn.pack(side=tk.LEFT, padx=2)

        self.step_label = tk.Label(inner_bar, text="Step 0 / 0", bg=ACCENT_LIGHT,
                                   fg=ACCENT_DARK, font=(FONT, 10, "bold"))
        self.step_label.pack(side=tk.RIGHT, padx=8)

        # Canvas with horizontal scroll
        canvas_container = tk.Frame(pad, bg=BG_CARD)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_container, bg="#fdfdff", highlightthickness=1,
                                highlightbackground=BORDER)
        h_scroll = tk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=h_scroll.set)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Explanation banner (accent bar + text)
        banner_outer = tk.Frame(pad, bg=BG_CARD)
        banner_outer.pack(fill=tk.X, pady=(10, 0))
        self.banner_bar = tk.Frame(banner_outer, bg=TEXT_MUTED, width=5)
        self.banner_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.explanation_label = tk.Label(
            banner_outer,
            text="Enter a reference string and click \"Run Simulation\" to begin.",
            bg="#f7f7fb", fg=TEXT_MUTED, font=(FONT, 10),
            anchor=tk.W, justify=tk.LEFT, wraplength=680, padx=12, pady=8
        )
        self.explanation_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- Stats card ---
        card_outer, card = make_card(right)
        card_outer.pack(fill=tk.X)
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.X, padx=16, pady=14)

        section_title(pad, "📈", "Results & Statistics").pack(anchor=tk.W, pady=(0, 10))

        tiles_row = tk.Frame(pad, bg=BG_CARD)
        tiles_row.pack(fill=tk.X, pady=(0, 10))

        self.tile_frames = tk.StringVar(value="0")
        self.tile_faults = tk.StringVar(value="0")
        self.tile_hits = tk.StringVar(value="0")
        self.tile_ratio = tk.StringVar(value="0%")

        self._make_stat_tile(tiles_row, "Frames", self.tile_frames, ACCENT, ACCENT_LIGHT)
        self._make_stat_tile(tiles_row, "Page Faults", self.tile_faults, DANGER, DANGER_LIGHT)
        self._make_stat_tile(tiles_row, "Page Hits", self.tile_hits, SUCCESS, SUCCESS_LIGHT)
        self._make_stat_tile(tiles_row, "Hit Ratio", self.tile_ratio, ACCENT, ACCENT_LIGHT)

        self.results_text = tk.Text(pad, height=6, font=("Consolas", 9),
                                    bg="#fafbff", fg=TEXT_DARK, relief=tk.FLAT,
                                    highlightbackground=BORDER, highlightthickness=1,
                                    wrap=tk.WORD, padx=8, pady=8)
        self.results_text.pack(fill=tk.X)
        self.results_text.insert(tk.END, "Run a simulation or comparison to see a detailed log here.")
        self.results_text.config(state=tk.DISABLED)

    def _make_stat_tile(self, parent, label, var, color, bg_color):
        tile = tk.Frame(parent, bg=bg_color)
        tile.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        tk.Label(tile, textvariable=var, bg=bg_color, fg=color,
                font=(FONT, 18, "bold")).pack(pady=(10, 0))
        tk.Label(tile, text=label, bg=bg_color, fg=TEXT_MUTED,
                font=(FONT, 8, "bold")).pack(pady=(0, 10))

    def _set_results_text(self, content):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, content)
        self.results_text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------
    def quick_setup(self):
        self.ref_string_var.set("7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1")
        self.num_frames_var.set("3")

    def set_speed(self, delay):
        self.anim.delay = delay

    def clear_all(self):
        self.anim.pause()
        self.reference_string = []
        self.steps = []
        self.page_faults = 0
        self.page_hits = 0
        self.page_color_map = {}
        self.canvas.delete("all")
        self._set_results_text("Run a simulation or comparison to see a detailed log here.")
        self.tile_frames.set("0")
        self.tile_faults.set("0")
        self.tile_hits.set("0")
        self.tile_ratio.set("0%")
        self.explanation_label.config(
            text="Enter a reference string and click \"Run Simulation\" to begin.",
            bg="#f7f7fb", fg=TEXT_MUTED
        )
        self.banner_bar.config(bg=TEXT_MUTED)
        self.step_label.config(text="Step 0 / 0")
        self._set_controls_state(tk.DISABLED)

    def parse_reference_string(self):
        raw = self.ref_string_var.get().strip()
        if not raw:
            messagebox.showerror("Input Error", "Please enter a reference string.")
            return None
        try:
            pages = [int(p.strip()) for p in raw.split(",") if p.strip() != ""]
            if not pages:
                raise ValueError
            return pages
        except ValueError:
            messagebox.showerror("Input Error", "Reference string must be comma-separated integers.")
            return None

    def parse_num_frames(self):
        try:
            num_frames = int(self.num_frames_var.get())
            if num_frames <= 0:
                raise ValueError
            return num_frames
        except ValueError:
            messagebox.showerror("Input Error", "Number of frames must be a positive integer.")
            return None

    # ------------------------------------------------------------------
    # Algorithms
    # ------------------------------------------------------------------
    def simulate_fifo(self, ref_string, num_frames):
        frames = [None] * num_frames
        queue = []
        steps = []

        for page in ref_string:
            fault = page not in frames
            evicted = None
            slot = None

            if fault:
                if None in frames:
                    idx = frames.index(None)
                    frames[idx] = page
                    queue.append(idx)
                    slot = idx
                else:
                    idx = queue.pop(0)
                    evicted = frames[idx]
                    frames[idx] = page
                    queue.append(idx)
                    slot = idx
                explanation = (f"Page {page} loaded into empty Frame {slot + 1} → FAULT" if evicted is None
                              else f"Page {page} replaces Page {evicted} in Frame {slot + 1} (oldest) → FAULT")
            else:
                slot = frames.index(page)
                explanation = f"Page {page} already in Frame {slot + 1} → HIT"

            steps.append({"page": page, "frames": frames.copy(), "fault": fault,
                         "evicted": evicted, "slot": slot, "explanation": explanation})

        return steps

    def simulate_lru(self, ref_string, num_frames):
        frames = [None] * num_frames
        last_used = {}
        steps = []

        for i, page in enumerate(ref_string):
            fault = page not in frames
            evicted = None
            slot = None

            if fault:
                if None in frames:
                    idx = frames.index(None)
                    frames[idx] = page
                    slot = idx
                    explanation = f"Page {page} loaded into empty Frame {slot + 1} → FAULT"
                else:
                    lru_page = min(
                        (p for p in frames if p is not None),
                        key=lambda p: last_used.get(p, -1)
                    )
                    idx = frames.index(lru_page)
                    evicted = lru_page
                    frames[idx] = page
                    slot = idx
                    explanation = (f"Page {page} replaces Page {evicted} in Frame {slot + 1} "
                                  f"(least recently used) → FAULT")
            else:
                slot = frames.index(page)
                explanation = f"Page {page} already in Frame {slot + 1} → HIT"

            last_used[page] = i
            steps.append({"page": page, "frames": frames.copy(), "fault": fault,
                         "evicted": evicted, "slot": slot, "explanation": explanation})

        return steps

    def simulate_optimal(self, ref_string, num_frames):
        frames = [None] * num_frames
        steps = []

        for i, page in enumerate(ref_string):
            fault = page not in frames
            evicted = None
            slot = None

            if fault:
                if None in frames:
                    idx = frames.index(None)
                    frames[idx] = page
                    slot = idx
                    explanation = f"Page {page} loaded into empty Frame {slot + 1} → FAULT"
                else:
                    future = ref_string[i + 1:]
                    farthest = -1
                    idx_to_replace = 0

                    for idx, p in enumerate(frames):
                        if p not in future:
                            idx_to_replace = idx
                            break
                        next_use = future.index(p)
                        if next_use > farthest:
                            farthest = next_use
                            idx_to_replace = idx

                    evicted = frames[idx_to_replace]
                    frames[idx_to_replace] = page
                    slot = idx_to_replace
                    explanation = (f"Page {page} replaces Page {evicted} in Frame {slot + 1} "
                                  f"(not needed again for longest time) → FAULT")
            else:
                slot = frames.index(page)
                explanation = f"Page {page} already in Frame {slot + 1} → HIT"

            steps.append({"page": page, "frames": frames.copy(), "fault": fault,
                         "evicted": evicted, "slot": slot, "explanation": explanation})

        return steps

    def simulate_basic(self, ref_string, num_frames):
        frames = [None] * num_frames
        ref_bit = [0] * num_frames
        pointer = 0
        steps = []

        for page in ref_string:
            if page in frames:
                idx = frames.index(page)
                ref_bit[idx] = 1
                fault = False
                evicted = None
                slot = idx
                explanation = f"Page {page} already in Frame {slot + 1} → HIT (reference bit set to 1)"
            else:
                fault = True
                evicted = None

                if None in frames:
                    idx = frames.index(None)
                    frames[idx] = page
                    ref_bit[idx] = 1
                    slot = idx
                    explanation = f"Page {page} loaded into empty Frame {slot + 1} → FAULT"
                else:
                    skipped = 0
                    while True:
                        if ref_bit[pointer] == 0:
                            evicted = frames[pointer]
                            frames[pointer] = page
                            ref_bit[pointer] = 1
                            slot = pointer
                            pointer = (pointer + 1) % num_frames
                            break
                        else:
                            ref_bit[pointer] = 0
                            pointer = (pointer + 1) % num_frames
                            skipped += 1
                    explanation = (f"Page {page} replaces Page {evicted} in Frame {slot + 1} "
                                  f"(clock hand gave {skipped} page(s) a second chance) → FAULT")

            steps.append({"page": page, "frames": frames.copy(), "fault": fault,
                         "evicted": evicted, "slot": slot, "explanation": explanation})

        return steps

    # ------------------------------------------------------------------
    # Run + Animate
    # ------------------------------------------------------------------
    def run_simulation(self):
        ref_string = self.parse_reference_string()
        if ref_string is None:
            return
        num_frames = self.parse_num_frames()
        if num_frames is None:
            return

        self.anim.pause()
        self.play_btn.config(text="▶ Play")
        self.reference_string = ref_string
        self.num_frames = num_frames

        algo = self.algorithm_var.get()
        if algo == "FIFO":
            self.steps = self.simulate_fifo(ref_string, num_frames)
        elif algo == "LRU":
            self.steps = self.simulate_lru(ref_string, num_frames)
        elif algo == "Optimal":
            self.steps = self.simulate_optimal(ref_string, num_frames)
        elif algo == "Basic":
            self.steps = self.simulate_basic(ref_string, num_frames)

        self.page_faults = sum(1 for s in self.steps if s["fault"])
        self.page_hits = len(self.steps) - self.page_faults

        unique_pages = sorted(set(ref_string))
        colors = utils.generate_colors(len(unique_pages))
        self.page_color_map = dict(zip(unique_pages, colors))

        self.anim.set_steps(len(self.steps) - 1)
        self._set_controls_state(tk.NORMAL)
        self.update_final_statistics()
        self.parent.after(50, lambda: self.render_step(0))

    def _set_controls_state(self, state):
        self.prev_btn.config(state=state)
        self.play_btn.config(state=state)
        self.next_btn.config(state=state)
        self.reset_btn.config(state=state)

    def toggle_play(self):
        if self.anim.is_playing:
            self.anim.pause()
            self.play_btn.config(text="▶ Play")
        else:
            if self.anim.current_step >= self.anim.max_steps:
                self.anim.reset()
            self.anim.play(self.parent)
            self.play_btn.config(text="⏸ Pause")

    def step_forward(self):
        self.anim.pause()
        self.play_btn.config(text="▶ Play")
        self.anim.step_forward()

    def step_backward(self):
        self.anim.pause()
        self.play_btn.config(text="▶ Play")
        self.anim.step_backward()

    def reset_animation(self):
        self.anim.pause()
        self.play_btn.config(text="▶ Play")
        self.anim.reset()

    def on_step_change(self, current_step):
        self.render_step(current_step)

    def render_step(self, step_idx):
        if not self.steps:
            return
        self.draw_timeline(self.num_frames, highlight_idx=step_idx)

        step = self.steps[step_idx]
        faults_so_far = sum(1 for s in self.steps[:step_idx + 1] if s["fault"])
        hits_so_far = (step_idx + 1) - faults_so_far

        if step["fault"]:
            bg, fg, bar = DANGER_LIGHT, DANGER_DARK, DANGER
        else:
            bg, fg, bar = SUCCESS_LIGHT, SUCCESS_DARK, SUCCESS

        self.explanation_label.config(
            text=(f"Step {step_idx + 1}/{len(self.steps)} — {step['explanation']}   "
                  f"|   Running total: {faults_so_far} faults, {hits_so_far} hits"),
            bg=bg, fg=fg
        )
        self.banner_bar.config(bg=bar)
        self.step_label.config(text=f"Step {step_idx + 1} / {len(self.steps)}")

        self.prev_btn.config(state=tk.NORMAL if step_idx > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if step_idx < len(self.steps) - 1 else tk.DISABLED)

    def draw_timeline(self, num_frames, highlight_idx=None):
        self.canvas.delete("all")

        if not self.steps:
            self.canvas.create_text(350, 150,
                                   text="No simulation run yet\nEnter a reference string and click Run",
                                   font=(FONT, 12), fill=TEXT_MUTED)
            return

        margin_left = 95
        margin_top = 55
        col_width = 46
        row_height = 42
        header_height = 32

        num_steps = len(self.steps)
        total_width = margin_left + num_steps * col_width + 40
        total_height = margin_top + header_height + num_frames * row_height + 100

        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

        self.canvas.create_text(
            margin_left, 20,
            text=f"{self.algorithm_var.get()} — {num_frames} Frame(s), {num_steps} References",
            font=(FONT, 12, "bold"), anchor=tk.W, fill=TEXT_DARK
        )

        self.canvas.create_text(margin_left, margin_top - 22,
                               text="Reference sequence →", font=(FONT, 9, "italic"),
                               fill=TEXT_MUTED, anchor=tk.W)

        for i, step in enumerate(self.steps):
            x = margin_left + i * col_width
            header_color = DANGER if step["fault"] else SUCCESS
            self.canvas.create_rectangle(x, margin_top, x + col_width, margin_top + header_height,
                                         fill=header_color, outline="white", width=1)
            self.canvas.create_text(x + col_width / 2, margin_top + header_height / 2,
                                   text=str(step["page"]), font=(FONT, 11, "bold"),
                                   fill="white")
            self.canvas.create_text(x + col_width / 2, margin_top + header_height + 10,
                                   text=str(i + 1), font=(FONT, 7), fill=TEXT_MUTED)

        self.canvas.create_text(margin_left - 60, margin_top + header_height + 20 + (num_frames * row_height) / 2,
                               text="Frames\n↓", font=(FONT, 9, "italic"), fill=TEXT_MUTED,
                               justify=tk.CENTER)

        frame_top = margin_top + header_height + 20
        for f in range(num_frames):
            y = frame_top + f * row_height
            row_bg = "#fbfbff" if f % 2 == 0 else "#f2f2fb"
            self.canvas.create_rectangle(margin_left, y, margin_left + num_steps * col_width,
                                         y + row_height, fill=row_bg, outline="")
            self.canvas.create_text(margin_left - 15, y + row_height / 2,
                                   text=f"F{f + 1}", font=(FONT, 10, "bold"),
                                   fill=TEXT_DARK, anchor=tk.E)

            for i, step in enumerate(self.steps):
                x = margin_left + i * col_width
                value = step["frames"][f]

                if value is None:
                    fill_color = "#ecedf7"
                    text = ""
                    outline_w = 1
                    outline_c = BORDER
                else:
                    fill_color = self.page_color_map.get(value, ACCENT_LIGHT)
                    text = str(value)
                    just_loaded = (step["fault"] and step["slot"] == f)
                    outline_w = 3 if just_loaded else 1
                    outline_c = ACCENT_DARK if just_loaded else "#c9cbe6"

                self.canvas.create_rectangle(x, y, x + col_width, y + row_height,
                                             fill=fill_color, outline=outline_c, width=outline_w)
                if text:
                    self.canvas.create_text(x + col_width / 2, y + row_height / 2,
                                           text=text, font=(FONT, 10, "bold"), fill="#1c2833")

        grid_bottom = frame_top + num_frames * row_height

        if highlight_idx is not None and 0 <= highlight_idx < num_steps:
            x = margin_left + highlight_idx * col_width
            self.canvas.create_rectangle(x, margin_top, x + col_width, grid_bottom,
                                         outline=WARNING, width=3)
            cx = x + col_width / 2
            self.canvas.create_polygon(cx - 7, margin_top - 12, cx + 7, margin_top - 12,
                                       cx, margin_top - 2, fill=WARNING, outline="")

        legend_y = grid_bottom + 25
        lx = margin_left
        self.canvas.create_rectangle(lx, legend_y, lx + 16, legend_y + 16,
                                     fill=DANGER, outline="")
        self.canvas.create_text(lx + 23, legend_y + 8, text="Fault reference",
                               anchor=tk.W, font=(FONT, 9), fill=TEXT_DARK)
        lx += 150
        self.canvas.create_rectangle(lx, legend_y, lx + 16, legend_y + 16,
                                     fill=SUCCESS, outline="")
        self.canvas.create_text(lx + 23, legend_y + 8, text="Hit reference",
                               anchor=tk.W, font=(FONT, 9), fill=TEXT_DARK)
        lx += 150
        self.canvas.create_rectangle(lx, legend_y, lx + 16, legend_y + 16,
                                     fill=ACCENT_LIGHT, outline=ACCENT_DARK, width=3)
        self.canvas.create_text(lx + 23, legend_y + 8, text="Newly loaded page",
                               anchor=tk.W, font=(FONT, 9), fill=TEXT_DARK)

        legend_y2 = legend_y + 30
        self.canvas.create_text(margin_left, legend_y2, text="Page colors:",
                               anchor=tk.W, font=(FONT, 9, "bold"), fill=TEXT_DARK)
        lx = margin_left + 90
        for page, color in self.page_color_map.items():
            self.canvas.create_rectangle(lx, legend_y2 - 8, lx + 16, legend_y2 + 8,
                                         fill=color, outline="")
            self.canvas.create_text(lx + 23, legend_y2, text=str(page),
                                   anchor=tk.W, font=(FONT, 9), fill=TEXT_DARK)
            lx += 48

    def update_final_statistics(self):
        total = len(self.steps)
        hit_ratio = (self.page_hits / total * 100) if total else 0

        self.tile_frames.set(str(self.num_frames))
        self.tile_faults.set(str(self.page_faults))
        self.tile_hits.set(str(self.page_hits))
        self.tile_ratio.set(f"{hit_ratio:.0f}%")

        log = (
            f"{self.algorithm_var.get()} Page Replacement — {total} references, "
            f"{self.num_frames} frame(s)\n"
            f"Faults: {self.page_faults}  |  Hits: {self.page_hits}  |  "
            f"Hit Ratio: {hit_ratio:.1f}%\n\n"
            f"Use Play / Next / Prev above the timeline to step through the\n"
            f"simulation reference by reference."
        )
        self._set_results_text(log)

    def compare_algorithms(self):
        ref_string = self.parse_reference_string()
        if ref_string is None:
            return
        num_frames = self.parse_num_frames()
        if num_frames is None:
            return

        self.anim.pause()
        self.play_btn.config(text="▶ Play")

        results = {
            "FIFO": self.simulate_fifo(ref_string, num_frames),
            "LRU": self.simulate_lru(ref_string, num_frames),
            "Optimal": self.simulate_optimal(ref_string, num_frames),
            "Basic": self.simulate_basic(ref_string, num_frames),
        }

        lines = [f"Algorithm Comparison — {num_frames} Frame(s)", "-" * 46,
                f"{'Algorithm':<12}{'Faults':<10}{'Hits':<10}{'Hit Ratio':<10}"]

        best_algo, best_faults = None, None
        for name, steps in results.items():
            faults = sum(1 for s in steps if s["fault"])
            hits = len(steps) - faults
            hit_ratio = (hits / len(steps) * 100) if steps else 0
            lines.append(f"{name:<12}{faults:<10}{hits:<10}{hit_ratio:.1f}%")
            if best_faults is None or faults < best_faults:
                best_faults, best_algo = faults, name

        lines.append("")
        lines.append(f"Best for this reference string: {best_algo} ({best_faults} faults)")
        self._set_results_text("\n".join(lines))

        self.reference_string = ref_string
        self.num_frames = num_frames
        self.steps = results[self.algorithm_var.get()]
        self.page_faults = sum(1 for s in self.steps if s["fault"])
        self.page_hits = len(self.steps) - self.page_faults

        unique_pages = sorted(set(ref_string))
        colors = utils.generate_colors(len(unique_pages))
        self.page_color_map = dict(zip(unique_pages, colors))

        total = len(self.steps)
        hit_ratio = (self.page_hits / total * 100) if total else 0
        self.tile_frames.set(str(num_frames))
        self.tile_faults.set(str(self.page_faults))
        self.tile_hits.set(str(self.page_hits))
        self.tile_ratio.set(f"{hit_ratio:.0f}%")

        self.anim.set_steps(len(self.steps) - 1)
        self._set_controls_state(tk.NORMAL)
        self.parent.after(50, lambda: self.render_step(0))
