import os
import sys
import time
import threading
import datetime
import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional, Tuple

# GUI
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox, filedialog

# Capture and video
import mss
import cv2
import numpy as np
from collections import deque

# Optional: global hotkeys and mouse events (may not be available in all envs)
try:
    from pynput import keyboard, mouse as pynput_mouse
    _HAVE_PYNPUT = True
except Exception:
    _HAVE_PYNPUT = False


@dataclass
class BBox:
    left: int
    top: int
    width: int
    height: int

    def as_mss(self):
        return {
            "left": int(self.left),
            "top": int(self.top),
            "width": int(self.width),
            "height": int(self.height),
        }


class ScreenRecorderApp:
    """
    Main application class encapsulating GUI, state, and recording logic.
    """

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("HRaJi Screen Recorder")
        self.master.iconphoto(True, PhotoImage(file="sc_icon.png"))
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # State flags
        self.is_recording = False
        self.is_paused = False
        self.stop_event = threading.Event()
        self.record_thread: Optional[threading.Thread] = None

        # Capture region and writer
        self.capture_bbox: Optional[BBox] = None
        self.writer: Optional[cv2.VideoWriter] = None
        self.writer_size: Optional[Tuple[int, int]] = None  # (w, h)
        self.target_fps = 30.0

        # UI variables
        self.status_var = tk.StringVar(value="Ready")
        self.ratio_var = tk.StringVar(value="Full Screen")
        self.follow_var = tk.BooleanVar(value=False)
        self.size_var = tk.StringVar(value="Area: -")
        self.elapsed_var = tk.StringVar(value="00:00:00")
        self.show_border_var = tk.BooleanVar(value=True)
        # Output settings
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        self.filename_tpl_var = tk.StringVar(value="HRaJi.mp4")

        # Countdown seconds before recording
        self.countdown_secs_var = tk.IntVar(value=3)

        # Cursor and clicks visualization
        self.show_cursor_var = tk.BooleanVar(value=True)
        self.show_clicks_var = tk.BooleanVar(value=True)

        # Timer bookkeeping (uses monotonic time to avoid clock jumps)
        self._elapsed_accum: float = 0.0
        self._current_resume_t0: Optional[float] = None
        self._timer_after_id: Optional[str] = None

        # Mini floating window refs
        self.mini_win: Optional[tk.Toplevel] = None
        self.mini_timer_var: Optional[tk.StringVar] = None
        self._mini_btn_pause: Optional[ttk.Button] = None
        self._mini_btn_continue: Optional[ttk.Button] = None
        self._mini_btn_stop: Optional[ttk.Button] = None
        self._drag_start_x: int = 0
        self._drag_start_y: int = 0

        # Frame scheduling to keep CFR duration matching timer
        self._next_frame_time: Optional[float] = None
        self._paused_at: Optional[float] = None
        self._last_frame_bgr: Optional[np.ndarray] = None

        # Border overlay windows
        self._border_windows: Optional[dict] = None  # keys: top,bottom,left,right
        self._border_thickness = 3
        self._border_color = "#ff3b30"  # red-ish

        # Stats overlay configs and runtime
        self.show_stats_var = tk.BooleanVar(value=False)
        self.stats_alpha_var = tk.DoubleVar(value=0.5)
        self.stats_font_size_var = tk.IntVar(value=10)
        self.stats_width_var = tk.IntVar(value=140)
        self.stats_height_var = tk.IntVar(value=40)
        self.stats_position_var = tk.StringVar(value="Bottem-Right")  # TL,TR,BL,BR
        self._stats_win: Optional[tk.Toplevel] = None
        self._stats_lbl: Optional[tk.Label] = None
        self._stats_after_id: Optional[str] = None
        self._capture_count_current = 0
        self._write_count_current = 0
        self._dup_count_current = 0
        self._last_stats_time = time.monotonic()

        # Mouse tracking state
        self._mouse_lock = threading.Lock()
        self._mouse_pos_abs: Tuple[int, int] = (0, 0)
        self._click_ripples = deque()  # list of (time_start, (x,y), button)
        self._mouse_listener = None
        self._hotkey_listener = None

        # Build UI and initialize region
        self._build_ui()
        self._refresh_region()
        # Start global hotkeys listener (runs regardless of recording state)
        self._start_hotkeys()

    # ------------------------- UI SETUP -------------------------
    def _build_ui(self) -> None:
        root = self.master
        root.geometry("800x550")
        root.minsize(800, 550)

        padding = {"padx": 10, "pady": 10}

        # Controls frame
        controls = ttk.Frame(root)
        controls.pack(side=tk.TOP, fill=tk.X, **padding)

        # Aspect ratio selection
        ttk.Label(controls, text="Aspect Ratio:").pack(side=tk.LEFT)
        ratios = ["Full Screen", "16:9", "9:16", "4:3"]
        self.ratio_menu = ttk.OptionMenu(controls, self.ratio_var, self.ratio_var.get(), *ratios, command=lambda _=None: self._refresh_region())
        self.ratio_menu.pack(side=tk.LEFT, padx=8)

        # Follow full screen
        self.follow_chk = ttk.Checkbutton(controls, text="Follow Full Screen", variable=self.follow_var)
        self.follow_chk.pack(side=tk.LEFT, padx=8)

        # Show border toggle
        self.border_chk = ttk.Checkbutton(controls, text="Show Capture Border", variable=self.show_border_var, command=self._update_border)
        self.border_chk.pack(side=tk.LEFT, padx=8)

        # Area size label
        self.size_lbl = ttk.Label(root, textvariable=self.size_var)
        self.size_lbl.pack(side=tk.TOP, anchor=tk.W, **padding)

        # Output and options frame
        out = ttk.Labelframe(root, text="Output & Options")
        out.pack(side=tk.TOP, fill=tk.X, **padding)
        # Save dir
        ttk.Label(out, text="Save to:").grid(row=0, column=0, sticky=tk.W, padx=(8, 4), pady=4)
        self.out_dir_entry = ttk.Entry(out, textvariable=self.output_dir_var, width=36)
        self.out_dir_entry.grid(row=0, column=1, sticky=tk.W)
        ttk.Button(out, text="Browse...", command=self._choose_output_dir).grid(row=0, column=2, padx=6)
        # Filename template
        ttk.Label(out, text="Filename:").grid(row=1, column=0, sticky=tk.W, padx=(8, 4), pady=4)
        self.tpl_entry = ttk.Entry(out, textvariable=self.filename_tpl_var, width=36)
        self.tpl_entry.grid(row=1, column=1, sticky=tk.W)
        ttk.Label(out, text="(strftime) e.g., HRaJi.mp4").grid(row=1, column=2, sticky=tk.W)
        # Countdown
        ttk.Label(out, text="Countdown (s):").grid(row=2, column=0, sticky=tk.W, padx=(8,4), pady=4)
        self.countdown_spin = ttk.Spinbox(out, from_=0, to=10, textvariable=self.countdown_secs_var, width=5)
        self.countdown_spin.grid(row=2, column=1, sticky=tk.W)
        # Cursor/clicks checkboxes
        self.cursor_chk = ttk.Checkbutton(out, text="Show cursor", variable=self.show_cursor_var)
        self.cursor_chk.grid(row=3, column=0, sticky=tk.W, padx=(8,4), pady=2)
        self.clicks_chk = ttk.Checkbutton(out, text="Show clicks", variable=self.show_clicks_var)
        self.clicks_chk.grid(row=3, column=1, sticky=tk.W, padx=(8,4), pady=2)

        # Stats overlay
        stats = ttk.Labelframe(root, text="Live Stats Overlay")
        stats.pack(side=tk.TOP, fill=tk.X, **padding)
        self.stats_show_chk = ttk.Checkbutton(stats, text="Show stats", variable=self.show_stats_var, command=self._update_stats_overlay)
        self.stats_show_chk.grid(row=0, column=0, sticky=tk.W, padx=(8,4))
        ttk.Label(stats, text="Opacity").grid(row=0, column=1, sticky=tk.W)
        self.stats_alpha = ttk.Spinbox(stats, from_=0.2, to=1.0, increment=0.05, textvariable=self.stats_alpha_var, width=6, command=self._update_stats_overlay)
        self.stats_alpha.grid(row=0, column=2, sticky=tk.W)
        ttk.Label(stats, text="Font").grid(row=0, column=3, sticky=tk.W)
        self.stats_font = ttk.Spinbox(stats, from_=8, to=24, textvariable=self.stats_font_size_var, width=6, command=self._update_stats_overlay)
        self.stats_font.grid(row=0, column=4, sticky=tk.W)
        ttk.Label(stats, text="Size WxH").grid(row=0, column=5, sticky=tk.W)
        self.stats_w = ttk.Spinbox(stats, from_=140, to=600, textvariable=self.stats_width_var, width=6, command=self._update_stats_overlay)
        self.stats_w.grid(row=0, column=6, sticky=tk.W)
        self.stats_h = ttk.Spinbox(stats, from_=40, to=400, textvariable=self.stats_height_var, width=6, command=self._update_stats_overlay)
        self.stats_h.grid(row=0, column=7, sticky=tk.W)
        ttk.Label(stats, text="Position").grid(row=0, column=8, sticky=tk.W)
        pos_menu = ttk.OptionMenu(stats, self.stats_position_var, self.stats_position_var.get(), "Top-Left","Top-Right","Bottom-Left","Bottom-Right", command=lambda _=None: self._update_stats_overlay())
        pos_menu.grid(row=0, column=9, sticky=tk.W)

        # Region selection
        actions = ttk.Frame(root)
        actions.pack(side=tk.TOP, fill=tk.X, **padding)
        ttk.Button(actions, text="Select Area...", command=self._start_area_selection).pack(side=tk.LEFT)

        # Buttons
        btns = ttk.Frame(root)
        btns.pack(side=tk.TOP, fill=tk.X, **padding)

        self.start_btn = ttk.Button(btns, text="Start", command=self.start_recording)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(btns, text="Pause", command=self.pause_recording, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.resume_btn = ttk.Button(btns, text="Resume", command=self.resume_recording, state=tk.DISABLED)
        self.resume_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btns, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        status_frame = ttk.Frame(root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, **padding)
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_lbl = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_lbl.pack(side=tk.LEFT, padx=6)
        ttk.Label(status_frame, text="Elapsed:").pack(side=tk.LEFT, padx=(16, 4))
        self.elapsed_lbl = ttk.Label(status_frame, textvariable=self.elapsed_var)
        self.elapsed_lbl.pack(side=tk.LEFT)

    # ----------------------- REGION LOGIC -----------------------
    def _get_primary_monitor_rect(self) -> BBox:
        """Detect the primary monitor via mss.
        In mss, monitors[1] is usually the primary monitor on most platforms.
        """
        with mss.mss() as sct:
            monitors = sct.monitors
            if len(monitors) > 1:
                m = monitors[1]
            else:
                m = monitors[0]
            return BBox(left=m["left"], top=m["top"], width=m["width"], height=m["height"])

    @staticmethod
    def _even(n: int) -> int:
        return int(n) - (int(n) % 2)

    def _calc_centered_bbox(self, ratio: Optional[Tuple[int, int]]) -> BBox:
        mon = self._get_primary_monitor_rect()
        if ratio is None:
            # Full screen
            width = self._even(mon.width)
            height = self._even(mon.height)
            return BBox(mon.left, mon.top, width, height)

        rw, rh = ratio
        W, H = mon.width, mon.height
        # Compute the largest rectangle of aspect rw:rh that fits within W x H
        # Try width-constrained
        h_by_w = int(W * rh / rw)
        if h_by_w <= H:
            width = W
            height = h_by_w
        else:
            width = int(H * rw / rh)
            height = H
        width = self._even(width)
        height = self._even(height)
        left = mon.left + (W - width) // 2
        top = mon.top + (H - height) // 2
        return BBox(left, top, width, height)

    def _ratio_tuple(self) -> Optional[Tuple[int, int]]:
        val = self.ratio_var.get()
        if val == "16:9":
            return (16, 9)
        if val == "9:16":
            return (9, 16)
        if val == "4:3":
            return (4, 3)
        # Full Screen
        return None

    def _refresh_region(self) -> None:
        bbox = self._calc_centered_bbox(self._ratio_tuple())
        self.capture_bbox = bbox
        self.writer_size = (bbox.width, bbox.height)
        self.size_var.set(f"Area: {bbox.width}x{bbox.height} @ ({bbox.left},{bbox.top})")
        # Update overlay border if enabled
        self._update_border()

    # ----------------------- BUTTON HANDLERS -----------------------
    def start_recording(self) -> None:
        if self.is_recording:
            return
        # Ensure region set
        self._refresh_region()

        # Optional countdown overlay (before writer starts)
        cd = max(0, int(self.countdown_secs_var.get()))
        if cd > 0:
            if not self._show_countdown(cd):
                return

        # Prepare writer (use chosen directory + template)
        timestamp = datetime.datetime.now()
        try:
            base = timestamp.strftime(self.filename_tpl_var.get())
        except Exception:
            base = timestamp.strftime("HRaJi_%Y-%m-%d_%H-%M-%S.mp4")
        out_dir = self.output_dir_var.get().strip() or os.getcwd()
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, base)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # widely supported
        w, h = self.writer_size
        self.writer = cv2.VideoWriter(filename, fourcc, self.target_fps, (int(w), int(h)))
        if not self.writer or not self.writer.isOpened():
            self.writer = None
            messagebox.showerror("Error", "Failed to create video writer. Check codec and permissions.")
            return

        # Update state & UI
        self.is_recording = True
        self.is_paused = False
        self.stop_event.clear()
        self.status_var.set("Recording...")
        self._set_buttons_state(recording=True, paused=False)

        # Start background thread
        self.record_thread = threading.Thread(target=self._record_loop, name="ScreenRecorderThread", daemon=True)
        self.record_thread.start()

        # Start timer and open mini control window
        self._timer_reset()
        self._timer_resume()
        self._open_mini_window()

        # Initialize frame schedule
        self._next_frame_time = time.monotonic() + (1.0 / float(self.target_fps))
        self._paused_at = None

        # Start overlays as needed
        self._start_mouse_listener()
        self._update_stats_overlay()

    def pause_recording(self) -> None:
        if not self.is_recording or self.is_paused:
            return
        self.is_paused = True
        self.status_var.set("Paused")
        self._set_buttons_state(recording=True, paused=True)
        self._timer_pause()
        # Note pause moment to shift schedule on resume
        self._paused_at = time.monotonic()

    def resume_recording(self) -> None:
        if not self.is_recording or not self.is_paused:
            return
        self.is_paused = False
        self.status_var.set("Recording...")
        self._set_buttons_state(recording=True, paused=False)
        self._timer_resume()
        # Shift next frame time by paused duration to keep timeline contiguous
        if self._paused_at is not None and self._next_frame_time is not None:
            paused_dur = max(0.0, time.monotonic() - self._paused_at)
            self._next_frame_time += paused_dur
        self._paused_at = None

    def stop_recording(self) -> None:
        if not self.is_recording:
            return
        # Signal thread to stop
        self.status_var.set("Saving video...")
        self.stop_event.set()
        try:
            if self.record_thread and self.record_thread.is_alive():
                self.record_thread.join(timeout=5.0)
        except Exception:
            pass
        finally:
            self.record_thread = None
            self.is_recording = False
            self.is_paused = False

        # Release writer
        try:
            if self.writer is not None:
                self.writer.release()
        finally:
            self.writer = None

        # Reset UI
        self.status_var.set("Ready")
        self._set_buttons_state(recording=False, paused=False)
        self._timer_reset()
        self._destroy_mini_window()
        # Keep border visible if toggled; update in case ratio changed during rec
        self._update_border()
        self._stop_mouse_listener()
        self._destroy_stats_overlay()

    def _set_buttons_state(self, recording: bool, paused: bool) -> None:
        if not recording:
            # Idle state
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
            self.ratio_menu.config(state=tk.NORMAL)
            self.follow_chk.config(state=tk.NORMAL)
        else:
            # During recording
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.ratio_menu.config(state=tk.DISABLED)
            self.follow_chk.config(state=tk.NORMAL)
            if paused:
                self.pause_btn.config(state=tk.DISABLED)
                self.resume_btn.config(state=tk.NORMAL)
            else:
                self.pause_btn.config(state=tk.NORMAL)
                self.resume_btn.config(state=tk.DISABLED)

        # Mirror state to mini window buttons if present
        if self.mini_win is not None and self._mini_btn_pause is not None and self._mini_btn_continue is not None and self._mini_btn_stop is not None:
            if not recording:
                self._mini_btn_pause.config(state=tk.DISABLED)
                self._mini_btn_continue.config(state=tk.DISABLED)
                self._mini_btn_stop.config(state=tk.DISABLED)
            else:
                self._mini_btn_stop.config(state=tk.NORMAL)
                if paused:
                    self._mini_btn_pause.config(state=tk.DISABLED)
                    self._mini_btn_continue.config(state=tk.NORMAL)
                else:
                    self._mini_btn_pause.config(state=tk.NORMAL)
                    self._mini_btn_continue.config(state=tk.DISABLED)

    # ----------------------- RECORDING LOOP -----------------------
    def _record_loop(self) -> None:
        """
        Runs in a background thread. Captures frames using MSS and writes them via OpenCV.
        - Caps FPS to ~target_fps.
        - Honors pause without tearing down the writer.
        - If "Follow Full Screen" is enabled, periodically updates the capture bbox
          (writer frame size stays constant; frames are resized to writer_size if needed).
        """
        frame_interval = 1.0 / float(self.target_fps)
        last_follow_check = 0.0

        try:
            with mss.mss() as sct:
                while not self.stop_event.is_set():
                    start_time = time.monotonic()

                    if self.is_paused:
                        # When paused, don't capture or write frames; keep CPU usage low
                        time.sleep(0.1)
                        # Optionally still respond to follow fullscreen
                        if self.follow_var.get() and (start_time - last_follow_check) >= 0.5:
                            self._maybe_update_bbox_follow(sct)
                            last_follow_check = start_time
                        continue

                    # Follow full-screen window if enabled (best-effort)
                    if self.follow_var.get() and (start_time - last_follow_check) >= 0.5:
                        self._maybe_update_bbox_follow(sct)
                        last_follow_check = start_time

                    bbox = self.capture_bbox
                    if bbox is None:
                        time.sleep(0.05)
                        continue

                    # Capture frame
                    img = sct.grab(bbox.as_mss())
                    frame = np.array(img, dtype=np.uint8)  # BGRA
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # BGRA -> BGR
                    # Overlay cursor and clicks if enabled
                    frame_bgr = self._draw_cursor_and_clicks(frame_bgr, bbox)
                    self._last_frame_bgr = frame_bgr

                    # Write frames according to schedule to maintain CFR duration
                    now = time.monotonic()
                    if self._next_frame_time is None:
                        self._next_frame_time = now

                    # Prepare sized frame once; duplicates reuse it
                    w0, h0 = frame_bgr.shape[1], frame_bgr.shape[0]
                    w, h = self.writer_size
                    if (w0 != w) or (h0 != h):
                        interp = cv2.INTER_AREA if (w0 > w or h0 > h) else cv2.INTER_LINEAR
                        sized_frame = cv2.resize(frame_bgr, (int(w), int(h)), interpolation=interp)
                    else:
                        sized_frame = frame_bgr

                    duplicates_written = 0
                    max_dup_per_loop = 5  # safety bound
                    while (not self.is_paused) and (not self.stop_event.is_set()) and (now + 1e-5) >= self._next_frame_time:
                        if self.writer is not None:
                            self.writer.write(sized_frame)
                            self._write_count_current += 1
                            if duplicates_written > 0:
                                self._dup_count_current += 1
                        self._next_frame_time += frame_interval
                        duplicates_written += 1
                        if duplicates_written >= max_dup_per_loop:
                            break
                        now = time.monotonic()

                    # Sleep until next frame time to avoid busy loop
                    now = time.monotonic()
                    sleep_for = self._next_frame_time - now
                    if sleep_for > 0:
                        time.sleep(min(sleep_for, 0.02))
                    # Update capture count and maybe refresh stats overlay
                    self._capture_count_current += 1
                    self._maybe_update_stats()
        except Exception as e:
            # Ensure UI reflects failure and we attempt a clean stop
            self.status_var.set(f"Error: {e}")
        finally:
            # Safe release in case of exceptions
            try:
                if self.writer is not None:
                    self.writer.release()
            finally:
                self.writer = None
                self.is_recording = False
                self.is_paused = False
                self.stop_event.set()
                # UI updates must be scheduled on the main thread
                self.master.after(0, lambda: self._set_buttons_state(recording=False, paused=False))
                self.master.after(0, lambda: self.status_var.set("Ready"))
                self.master.after(0, self._timer_reset)
                self.master.after(0, self._destroy_mini_window)
                self.master.after(0, self._update_border)
                self.master.after(0, self._destroy_stats_overlay)

    # -------------------- FOLLOW FULL SCREEN (X11) --------------------
    def _maybe_update_bbox_follow(self, sct: mss.mss) -> None:
        """Best-effort detection of active full-screen window on X11.
        Requires 'xprop' and 'xwininfo'. If not available or error occurs, silently ignore.
        The capture bbox is updated if a full-screen app is detected.
        """
        try:
            bbox = self._detect_active_fullscreen_bbox(sct)
            if bbox is not None:
                self.capture_bbox = bbox
                # Schedule border update on main thread
                self.master.after(0, self._update_border)
                # Keep writer_size unchanged; we will resize frames as needed
        except Exception:
            pass

    def _detect_active_fullscreen_bbox(self, sct: mss.mss) -> Optional[BBox]:
        # Tools required
        if shutil.which("xprop") is None or shutil.which("xwininfo") is None:
            return None
        # Get active window id
        try:
            out = subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stderr=subprocess.DEVNULL, text=True)
            # Example: _NET_ACTIVE_WINDOW(WINDOW): window id # 0x06000007
            wid_hex = out.strip().split()[-1]
            if wid_hex == "0x0":
                return None
        except Exception:
            return None

        # Check if window is fullscreen
        try:
            state_out = subprocess.check_output(["xprop", "-id", wid_hex, "_NET_WM_STATE"], stderr=subprocess.DEVNULL, text=True)
            is_fullscreen = "_NET_WM_STATE_FULLSCREEN" in state_out
        except Exception:
            is_fullscreen = False

        # Get window geometry
        try:
            winfo = subprocess.check_output(["xwininfo", "-id", wid_hex], stderr=subprocess.DEVNULL, text=True)
        except Exception:
            return None

        # Parse geometry
        # Lines of interest:
        #   Absolute upper-left X:  0
        #   Absolute upper-left Y:  0
        #   Width: 1920
        #   Height: 1080
        x = y = w = h = None
        for line in winfo.splitlines():
            line = line.strip()
            if line.startswith("Absolute upper-left X:"):
                x = int(line.split(":")[1])
            elif line.startswith("Absolute upper-left Y:"):
                y = int(line.split(":")[1])
            elif line.startswith("Width:"):
                w = int(line.split(":")[1])
            elif line.startswith("Height:"):
                h = int(line.split(":")[1])
        if None in (x, y, w, h):
            return None

        # If not marked fullscreen, heuristically check if it matches monitor size
        mon = self._get_primary_monitor_rect()
        if not is_fullscreen:
            if abs(w - mon.width) <= 2 and abs(h - mon.height) <= 2:
                is_fullscreen = True
        if not is_fullscreen:
            return None

        # Ensure even dims
        w = self._even(w)
        h = self._even(h)
        return BBox(left=x, top=y, width=w, height=h)

    # -------------------------- LIFECYCLE --------------------------
    def on_close(self) -> None:
        if self.is_recording:
            if messagebox.askyesno("Quit", "Recording is in progress. Stop and quit?"):
                try:
                    self.stop_recording()
                finally:
                    self.master.after(100, self.master.destroy)
            else:
                return
        else:
            self.master.destroy()
        self._stop_hotkeys()
        self._stop_mouse_listener()

    # --------------------- BORDER OVERLAY WINDOWS ---------------------
    def _ensure_border_windows(self) -> None:
        if self._border_windows is not None:
            return
        self._border_windows = {}
        for key in ("top", "bottom", "left", "right"):
            w = tk.Toplevel(self.master)
            w.overrideredirect(True)
            try:
                w.attributes("-topmost", True)
            except Exception:
                pass
            try:
                w.attributes("-alpha", 0.9)
            except Exception:
                pass
            # Use a label to set background color
            frame = tk.Frame(w, bg=self._border_color)
            frame.pack(fill=tk.BOTH, expand=True)
            # Prevent focus stealing
            w.withdraw()
            self._border_windows[key] = w

    def _hide_border(self) -> None:
        if self._border_windows:
            for w in self._border_windows.values():
                try:
                    w.destroy()
                except Exception:
                    pass
        self._border_windows = None

    def _update_border(self) -> None:
        # Toggle via checkbox
        if not self.show_border_var.get():
            self._hide_border()
            return
        bbox = self.capture_bbox
        if bbox is None:
            self._hide_border()
            return
        self._ensure_border_windows()
        bw = self._border_thickness
        # Calculate geometries
        x, y, w, h = bbox.left, bbox.top, bbox.width, bbox.height
        sides = {
            "top":    (x, y, w, bw),
            "bottom": (x, y + h - bw, w, bw),
            "left":   (x, y, bw, h),
            "right":  (x + w - bw, y, bw, h),
        }
        for key, geom in sides.items():
            wdw = self._border_windows.get(key)
            if wdw is None:
                continue
            wdw.deiconify()
            gx, gy, gw, gh = geom
            try:
                wdw.geometry(f"{int(gw)}x{int(gh)}+{int(gx)}+{int(gy)}")
            except Exception:
                pass

    # --------------------------- COUNTDOWN ---------------------------
    def _show_countdown(self, seconds: int) -> bool:
        # Overlay a centered countdown on the primary monitor
        try:
            mon = self._get_primary_monitor_rect()
            win = tk.Toplevel(self.master)
            win.overrideredirect(True)
            try:
                win.attributes("-topmost", True)
                win.attributes("-alpha", 0.8)
            except Exception:
                pass
            # Cover whole monitor (transparent background)
            win.geometry(f"{mon.width}x{mon.height}+{mon.left}+{mon.top}")
            frame = tk.Frame(win, bg="#000000")
            frame.pack(fill=tk.BOTH, expand=True)
            frame.configure(bg="black")
            try:
                win.attributes("-alpha", 0.25)
            except Exception:
                pass
            lbl_var = tk.StringVar(value=str(seconds))
            lbl = tk.Label(frame, textvariable=lbl_var, fg="white", bg="black", font=("TkDefaultFont", 72, "bold"))
            lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            # Block until countdown finishes (without freezing UI via update)
            end = time.monotonic() + seconds
            while True:
                remaining = int(round(end - time.monotonic()))
                if remaining <= 0:
                    break
                lbl_var.set(str(remaining))
                self.master.update()
                time.sleep(0.1)
            win.destroy()
            return True
        except Exception:
            return True

    # ------------------------ GLOBAL HOTKEYS ------------------------
    def _start_hotkeys(self) -> None:
        if not _HAVE_PYNPUT:
            return
        if self._hotkey_listener is not None:
            return
        try:
            self._hotkey_listener = keyboard.GlobalHotKeys({
                '<alt>+<shift>+s': self._hotkey_start_stop,
                '<alt>+<shift>+p': self._hotkey_pause,
                '<alt>+<shift>+r': self._hotkey_resume,
            })
            self._hotkey_listener.start()
        except Exception:
            self._hotkey_listener = None

    def _stop_hotkeys(self) -> None:
        if self._hotkey_listener is not None:
            try:
                self._hotkey_listener.stop()
            except Exception:
                pass
            self._hotkey_listener = None

    # ------------------------ FILE DIALOG ------------------------
    def _choose_output_dir(self) -> None:
        try:
            d = filedialog.askdirectory(initialdir=self.output_dir_var.get())
            if d:
                self.output_dir_var.set(d)
        except Exception:
            pass

    def _hotkey_start_stop(self) -> None:
        # Alt+Shift+S: Start or Stop depending on state
        self.master.after(0, lambda: self.stop_recording() if self.is_recording else self.start_recording())

    def _hotkey_pause(self) -> None:
        if self.is_recording and not self.is_paused:
            self.master.after(0, self.pause_recording)

    def _hotkey_resume(self) -> None:
        if self.is_recording and self.is_paused:
            self.master.after(0, self.resume_recording)

    # -------------------- MOUSE CURSOR & CLICKS --------------------
    def _start_mouse_listener(self) -> None:
        if not _HAVE_PYNPUT or self._mouse_listener is not None:
            return
        try:
            def on_move(x, y):
                with self._mouse_lock:
                    self._mouse_pos_abs = (x, y)
            def on_click(x, y, button, pressed):
                if pressed and self.show_clicks_var.get():
                    with self._mouse_lock:
                        self._click_ripples.append((time.monotonic(), (x, y), str(button)))
            self._mouse_listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click)
            self._mouse_listener.start()
        except Exception:
            self._mouse_listener = None

    def _stop_mouse_listener(self) -> None:
        if self._mouse_listener is not None:
            try:
                self._mouse_listener.stop()
            except Exception:
                pass
            self._mouse_listener = None

    def _draw_cursor_and_clicks(self, frame_bgr: np.ndarray, bbox: BBox) -> np.ndarray:
        h, w = frame_bgr.shape[:2]
        # Cursor overlay
        with self._mouse_lock:
            mx, my = self._mouse_pos_abs
            ripples = list(self._click_ripples)
        # Translate absolute to local bbox
        cx = mx - bbox.left
        cy = my - bbox.top
        # Draw cursor dot if enabled and in bounds
        if self.show_cursor_var.get() and 0 <= cx < w and 0 <= cy < h:
            cv2.circle(frame_bgr, (int(cx), int(cy)), 6, (0, 255, 255), thickness=-1)  # yellow dot
            cv2.circle(frame_bgr, (int(cx), int(cy)), 10, (0, 200, 200), thickness=2)
        # Draw click ripples (fade over 0.6s)
        if self.show_clicks_var.get():
            now = time.monotonic()
            new_ripples = deque()
            for t0, (rx, ry), btn in ripples:
                age = now - t0
                if age > 0.6:
                    continue
                lx = rx - bbox.left
                ly = ry - bbox.top
                if 0 <= lx < w and 0 <= ly < h:
                    radius = int(10 + 60 * (age / 0.6))
                    alpha = max(0.0, 1.0 - (age / 0.6))
                    color = (0, 0, 255) if 'left' in btn else (255, 0, 0)
                    cv2.circle(frame_bgr, (int(lx), int(ly)), radius, color, thickness=2)
                    # A simple fade by drawing thinner circles
                new_ripples.append((t0, (rx, ry), btn))
            with self._mouse_lock:
                self._click_ripples = new_ripples
        return frame_bgr

    # -------------------------- STATS OVERLAY --------------------------
    def _maybe_update_stats(self) -> None:
        if not self.show_stats_var.get():
            return
        now = time.monotonic()
        if now - self._last_stats_time < 1.0:
            return
        # Compute rates and reset counters
        dt = now - self._last_stats_time
        cap_fps = self._capture_count_current / dt if dt > 0 else 0.0
        write_fps = self._write_count_current / dt if dt > 0 else 0.0
        dup = self._dup_count_current
        self._capture_count_current = 0
        self._write_count_current = 0
        self._dup_count_current = 0
        self._last_stats_time = now
        # Update overlay text
        if self._stats_lbl is not None:
            txt = f"Capture FPS: {cap_fps:.1f}\nWritten FPS: {write_fps:.1f}\nDup frames/s: {dup}"
            try:
                self._stats_lbl.config(text=txt)
            except Exception:
                pass

    def _update_stats_overlay(self) -> None:
        if not self.show_stats_var.get():
            self._destroy_stats_overlay()
            return
        # Create if missing
        if self._stats_win is None:
            win = tk.Toplevel(self.master)
            self._stats_win = win
            win.overrideredirect(True)
            try:
                win.attributes("-topmost", True)
                win.attributes("-alpha", float(self.stats_alpha_var.get()))
            except Exception:
                pass
            self._stats_lbl = tk.Label(win, text="",
                                       justify=tk.LEFT,
                                       anchor=tk.NW,
                                       bg="#202020", fg="#f0f0f0")
            self._stats_lbl.pack(fill=tk.BOTH, expand=True)
        # Resize and reposition
        try:
            w = int(self.stats_width_var.get())
            h = int(self.stats_height_var.get())
            self._stats_win.geometry(f"{w}x{h}+0+0")
            # Position relative to capture bbox
            bbox = self.capture_bbox or self._get_primary_monitor_rect()
            x, y = bbox.left, bbox.top
            if self.stats_position_var.get().lower().startswith("top-right"):
                x = bbox.left + bbox.width - w
            if self.stats_position_var.get().lower().startswith("bottom"):
                y = bbox.top + bbox.height - h
            self._stats_win.geometry(f"{w}x{h}+{x}+{y}")
            # Font and alpha
            try:
                self._stats_lbl.config(font=("TkDefaultFont", int(self.stats_font_size_var.get())))
                self._stats_win.attributes("-alpha", float(self.stats_alpha_var.get()))
            except Exception:
                pass
        except Exception:
            pass

    def _destroy_stats_overlay(self) -> None:
        if self._stats_win is not None:
            try:
                self._stats_win.destroy()
            except Exception:
                pass
        self._stats_win = None
        self._stats_lbl = None
        self._stats_after_id = None

    # ----------------------- AREA SELECTION -----------------------
    def _start_area_selection(self) -> None:
        mon = self._get_primary_monitor_rect()
        sel = tk.Toplevel(self.master)
        sel.overrideredirect(True)
        try:
            sel.attributes("-topmost", True)
            sel.attributes("-alpha", 0.25)
        except Exception:
            pass
        sel.geometry(f"{mon.width}x{mon.height}+{mon.left}+{mon.top}")
        canvas = tk.Canvas(sel, bg='black', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        rect_id = None
        start = {'x':0,'y':0}

        def on_down(e):
            start['x'] = e.x
            start['y'] = e.y
            nonlocal rect_id
            if rect_id is not None:
                canvas.delete(rect_id)
                rect_id = None

        def on_drag(e):
            nonlocal rect_id
            if rect_id is not None:
                canvas.delete(rect_id)
            rect_id = canvas.create_rectangle(start['x'], start['y'], e.x, e.y, outline='red', width=2)

        def on_up(e):
            x0, y0 = start['x'], start['y']
            x1, y1 = e.x, e.y
            left = min(x0, x1) + mon.left
            top = min(y0, y1) + mon.top
            width = abs(x1 - x0)
            height = abs(y1 - y0)
            # Ensure even
            width = self._even(width)
            height = self._even(height)
            if width >= 4 and height >= 4:
                self.capture_bbox = BBox(left=left, top=top, width=width, height=height)
                self.writer_size = (width, height)
                self.size_var.set(f"Area: {width}x{height} @ ({left},{top})")
                self._update_border()
            sel.destroy()

        canvas.bind('<ButtonPress-1>', on_down)
        canvas.bind('<B1-Motion>', on_drag)
        canvas.bind('<ButtonRelease-1>', on_up)

    # -------------------------- TIMER LOGIC --------------------------
    @staticmethod
    def _format_secs(secs: float) -> str:
        total = int(secs)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        return f"{hh:02d}:{mm:02d}:{ss:02d}"

    def _timer_reset(self) -> None:
        # Consolidate any running span into accum, then reset
        if self._current_resume_t0 is not None:
            self._elapsed_accum += (time.monotonic() - self._current_resume_t0)
        self._current_resume_t0 = None
        self._elapsed_accum = 0.0
        self.elapsed_var.set("00:00:00")
        if self.mini_timer_var is not None:
            self.mini_timer_var.set("00:00:00")
        if self._timer_after_id is not None:
            try:
                self.master.after_cancel(self._timer_after_id)
            except Exception:
                pass
            self._timer_after_id = None

    def _timer_pause(self) -> None:
        # Move running span into accum and stop counting
        if self._current_resume_t0 is not None:
            self._elapsed_accum += (time.monotonic() - self._current_resume_t0)
            self._current_resume_t0 = None

    def _timer_resume(self) -> None:
        # Start counting from now if not already
        if self._current_resume_t0 is None:
            self._current_resume_t0 = time.monotonic()
        # Kick off periodic updates if not running
        if self._timer_after_id is None:
            self._schedule_timer_update()

    def _schedule_timer_update(self) -> None:
        # Update elapsed and reschedule while recording
        def _tick():
            self._timer_after_id = None
            # Compute elapsed
            elapsed = self._elapsed_accum
            if self._current_resume_t0 is not None:
                elapsed += (time.monotonic() - self._current_resume_t0)
            text = self._format_secs(elapsed)
            self.elapsed_var.set(text)
            if self.mini_timer_var is not None:
                self.mini_timer_var.set(text)
            # Continue ticking while recording
            if self.is_recording:
                self._timer_after_id = self.master.after(200, _tick)

        self._timer_after_id = self.master.after(200, _tick)

    # --------------------- MINI CONTROL WINDOW ---------------------
    def _open_mini_window(self) -> None:
        # Destroy any existing
        self._destroy_mini_window()

        win = tk.Toplevel(self.master)
        self.mini_win = win
        win.title("Recorder")
        try:
            win.attributes("-topmost", True)
        except Exception:
            pass
        # Borderless window for a cleaner floating widget
        try:
            win.overrideredirect(True)
        except Exception:
            pass

        frame = ttk.Frame(win, padding=(8, 6))
        frame.pack(fill=tk.BOTH, expand=True)

        # Dragging support: click anywhere to drag
        frame.bind("<ButtonPress-1>", self._mini_on_start_drag)
        frame.bind("<B1-Motion>", self._mini_on_drag)

        # Timer label
        self.mini_timer_var = tk.StringVar(value=self.elapsed_var.get())
        lbl = ttk.Label(frame, textvariable=self.mini_timer_var, font=("TkDefaultFont", 10, "bold"))
        lbl.pack(side=tk.LEFT, padx=(0, 8))
        lbl.bind("<ButtonPress-1>", self._mini_on_start_drag)
        lbl.bind("<B1-Motion>", self._mini_on_drag)

        # Buttons: Pause, Continue, Stop
        self._mini_btn_pause = ttk.Button(frame, text="Pause", command=self.pause_recording, width=7)
        self._mini_btn_pause.pack(side=tk.LEFT, padx=2)
        self._mini_btn_continue = ttk.Button(frame, text="Continue", command=self.resume_recording, width=8)
        self._mini_btn_continue.pack(side=tk.LEFT, padx=2)
        self._mini_btn_stop = ttk.Button(frame, text="Stop", command=self.stop_recording, width=6)
        self._mini_btn_stop.pack(side=tk.LEFT, padx=2)

        # Initial state sync
        self._set_buttons_state(recording=self.is_recording, paused=self.is_paused)

        # Place near top-center of primary monitor
        mon = self._get_primary_monitor_rect()
        win.update_idletasks()
        ww = win.winfo_width()
        wh = win.winfo_height()
        x = mon.left + (mon.width - ww) // 2
        y = mon.top + int(0.05 * mon.height)
        win.geometry(f"+{x}+{y}")

        # Closing mini window should just close it (not stop recording)
        win.protocol("WM_DELETE_WINDOW", self._destroy_mini_window)

    def _destroy_mini_window(self) -> None:
        if self.mini_win is not None:
            try:
                self.mini_win.destroy()
            except Exception:
                pass
        self.mini_win = None
        self.mini_timer_var = None
        self._mini_btn_pause = None
        self._mini_btn_continue = None
        self._mini_btn_stop = None

    def _mini_on_start_drag(self, event) -> None:
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _mini_on_drag(self, event) -> None:
        if self.mini_win is None:
            return
        # Compute new position: root coordinates minus click offset
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        try:
            self.mini_win.geometry(f"+{int(x)}+{int(y)}")
        except Exception:
            pass


def ensure_dependencies() -> bool:
    """Optional check to provide a helpful message if MSS/OpenCV are missing.
    Returns True when everything looks okay.
    """
    missing = []
    try:
        import mss as _  # noqa: F401
    except Exception:
        missing.append("mss")
    try:
        import cv2 as _  # noqa: F401
    except Exception:
        missing.append("opencv-python")
    try:
        import numpy as _  # noqa: F401
    except Exception:
        missing.append("numpy")

    if missing:
        msg = (
            "Missing dependencies: " + ", ".join(missing) +
            "\nInstall them with:\n  pip install mss opencv-python numpy"
        )
        print(msg, file=sys.stderr)
        return False
    return True


if __name__ == "__main__":
    if not ensure_dependencies():
        # Continue launching anyway; tkinter UI will still show
        pass

    root = tk.Tk()
    # Use Tk themed widgets (ttk) default theme
    try:
        style = ttk.Style()
        if sys.platform.startswith("linux") and "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app = ScreenRecorderApp(root)
    root.mainloop()
