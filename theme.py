import tkinter as tk

FONT = "Segoe UI"

BG_APP = "#f4f5fa"
BG_HEADER = "#1e1b3a"
BG_CARD = "#ffffff"
BORDER = "#e4e6f0"

ACCENT = "#6c5ce7"
ACCENT_DARK = "#5847d1"
ACCENT_LIGHT = "#eeecfc"

SUCCESS = "#00b894"
SUCCESS_DARK = "#00997a"
SUCCESS_LIGHT = "#e3faf4"

DANGER = "#ff6b6b"
DANGER_DARK = "#e05555"
DANGER_LIGHT = "#ffefef"

WARNING = "#f6a609"
WARNING_DARK = "#d38f00"
WARNING_LIGHT = "#fef3e0"

INFO = "#0984e3"
INFO_DARK = "#0870c4"
INFO_LIGHT = "#e6f3fd"

TEXT_DARK = "#2d2b45"
TEXT_MUTED = "#8a89a6"
TEXT_ON_DARK = "#f1f0fb"

# Palette used to give each module card on the home screen its own identity
MODULE_COLORS = [
    (ACCENT, ACCENT_DARK, ACCENT_LIGHT),
    (INFO, INFO_DARK, INFO_LIGHT),
    (SUCCESS, SUCCESS_DARK, SUCCESS_LIGHT),
    (WARNING, WARNING_DARK, WARNING_LIGHT),
    (DANGER, DANGER_DARK, DANGER_LIGHT),
]


def make_button(parent, text, command, style="primary", state=tk.NORMAL, font_size=10):
    """A flat, hover-responsive button in one of the theme's standard styles."""
    palette = {
        "primary": (ACCENT, ACCENT_DARK, "white"),
        "success": (SUCCESS, SUCCESS_DARK, "white"),
        "danger": (DANGER, DANGER_DARK, "white"),
        "warning": (WARNING, WARNING_DARK, "white"),
        "info": (INFO, INFO_DARK, "white"),
        "muted": ("#eceef7", "#dcdfef", TEXT_DARK),
        "dark": (BG_HEADER, "#2a2650", TEXT_ON_DARK),
    }
    bg, hover_bg, fg = palette.get(style, palette["primary"])

    btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                    activebackground=hover_bg, activeforeground=fg,
                    font=(FONT, font_size, "bold"), relief=tk.FLAT, bd=0,
                    cursor="hand2", padx=14, pady=8, state=state)

    def on_enter(_):
        if btn["state"] != tk.DISABLED:
            btn.config(bg=hover_bg)

    def on_leave(_):
        if btn["state"] != tk.DISABLED:
            btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def make_card(parent, bg=BG_CARD):
    """A white card with a thin border. Returns (outer_frame, inner_frame) —
    place content inside inner_frame."""
    outer = tk.Frame(parent, bg=BORDER)
    inner = tk.Frame(outer, bg=bg)
    inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    return outer, inner


def section_title(parent, icon, text, bg=BG_CARD):
    return tk.Label(parent, text=f"{icon}  {text}", bg=bg, fg=TEXT_DARK,
                    font=(FONT, 10, "bold"), anchor=tk.W)


def build_header(parent, title, subtitle, back_callback=None):
    """Standard dark header bar used on every screen. If back_callback is
    None, no back button is shown (used on the home screen)."""
    header = tk.Frame(parent, bg=BG_HEADER, height=72)
    header.pack(fill=tk.X)
    header.pack_propagate(False)

    left_group = tk.Frame(header, bg=BG_HEADER)
    left_group.pack(side=tk.LEFT, padx=18, pady=10)

    if back_callback is not None:
        back_btn = make_button(left_group, "←  Home", back_callback, style="dark", font_size=10)
        back_btn.pack(side=tk.LEFT, padx=(0, 18))

    title_box = tk.Frame(left_group, bg=BG_HEADER)
    title_box.pack(side=tk.LEFT)

    tk.Label(title_box, text=title, font=(FONT, 16, "bold"),
            bg=BG_HEADER, fg="white").pack(anchor=tk.W)
    tk.Label(title_box, text=subtitle, font=(FONT, 9),
            bg=BG_HEADER, fg="#a9a6cf").pack(anchor=tk.W)

    return header
