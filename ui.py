import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
from brain.vision import analyze_image
from brain.visual_state import set_image, clear_image
from brain.visual_memory import clear_visual_memory
import threading

from core.assistant import Assistant


class ArchonUI:

    def __init__(self, root):

        self.root = root

        self.running = True

        self.root.title("ARCHON")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0b0f14")
        self.current_image_path = None
        self.current_image = None
        self.assistant = None

        self.current_image = None

        # =====================================================
        # SCROLLABLE WINDOW
        # =====================================================

        self.canvas = tk.Canvas(
            root,
            bg="#0b0f14",
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.main_frame = tk.Frame(
            self.canvas,
            bg="#0b0f14"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.main_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_frame
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

        # =====================================================
        # HEADER
        # =====================================================

        title = tk.Label(
            self.main_frame,
            text="ARCHON",
            font=("Arial", 30, "bold"),
            fg="#00d9ff",
            bg="#0b0f14"
        )

        title.pack(pady=(30, 5))

        subtitle = tk.Label(
            self.main_frame,
            text="PERSONAL AI SYSTEM",
            font=("Arial", 11),
            fg="#8b9aaa",
            bg="#0b0f14"
        )

        subtitle.pack()

        # =====================================================
        # STATUS
        # =====================================================

        self.status = tk.Label(
            self.main_frame,
            text="● SYSTEM READY",
            font=("Arial", 14, "bold"),
            fg="#00ff99",
            bg="#111820"
        )

        self.status.pack(
            fill="x",
            padx=40,
            pady=30,
            ipady=18
        )

        # =====================================================
        # CURRENT TASK
        # =====================================================

        self.task_label = tk.Label(
            self.main_frame,
            text="CURRENT TASK: IDLE",
            font=("Arial", 11, "bold"),
            fg="#8b9aaa",
            bg="#0b0f14"
        )

        self.task_label.pack(
            pady=(0, 20)
        )

        # =====================================================
        # VISUAL WORKSPACE
        # =====================================================

        tk.Label(
            self.main_frame,
            text="VISUAL WORKSPACE",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#0b0f14"
        ).pack(
            anchor="w",
            padx=50,
            pady=(10, 10)
        )

        self.visual_workspace = tk.Frame(
            self.main_frame,
            bg="#111820",
            height=350
        )

        self.visual_workspace.pack(
            fill="x",
            padx=40,
            pady=(0, 15)
        )

        self.visual_workspace.pack_propagate(False)

        self.visual_label = tk.Label(
            self.visual_workspace,
            text="ARCHON VISUAL SYSTEM\nREADY",
            font=("Arial", 16, "bold"),
            fg="#00d9ff",
            bg="#111820"
        )

        self.visual_label.pack(
            expand=True
        )

        tk.Label(
            self.main_frame,
            text="ARCHON VISION",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#0b0f14"
        ).pack(
            anchor="w",
            padx=50,
            pady=(10, 10)
        )

        self.vision_result = tk.Text(
            self.main_frame,
            height=6,
            bg="#111820",
            fg="#b9c7d5",
            font=("Consolas", 10),
            relief="flat",
            padx=15,
            pady=15,
            wrap="word"
        )

        # =========================================================
        # VISION QUESTION
        # =========================================================

        tk.Label(
            self.main_frame,
            text="ASK ARCHON ABOUT THIS IMAGE",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#0b0f14"
        ).pack(
            anchor="w",
            padx=50,
            pady=(5, 10)
        )

        self.question_entry = tk.Entry(
            self.main_frame,
            font=("Arial", 12),
            bg="#111820",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.question_entry.pack(
            fill="x",
            padx=40,
            ipady=12
        )

        self.question_entry.insert(
            0,
            "What is in this image?"
        )

        self.ask_button = tk.Button(
            self.main_frame,
            text="🧠 ASK ARCHON",
            command=self.ask_about_image,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#17232d",
            activebackground="#263746",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            state="disabled"
        )

        self.ask_button.pack(
            pady=(12, 30)
        )

        self.vision_result.pack(
            fill="x",
            padx=40,
            pady=(0, 25)
        )

        self.vision_result.insert(
            "end",
            "ARCHON Vision is ready.\n"
        )

        # =====================================================
        # IMAGE BUTTONS
        # =====================================================

        button_frame = tk.Frame(
            self.main_frame,
            bg="#0b0f14"
        )

        button_frame.pack(
            pady=(0, 30)
        )

        self.upload_button = tk.Button(
            button_frame,
            text="🖼  UPLOAD IMAGE",
            command=self.upload_image,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#17232d",
            activebackground="#263746",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )

        self.upload_button.pack(
            side="left",
            padx=8
        )

        self.analyze_button = tk.Button(
            button_frame,
            text="🧠 ANALYZE IMAGE",
            command=self.analyze_current_image,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#17232d",
            activebackground="#263746",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2",
            state="disabled"
        )

        self.analyze_button.pack(
            side="left",
            padx=8
        )

        self.clear_button = tk.Button(
            button_frame,
            text="CLEAR",
            command=self.clear_visual,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#17232d",
            activebackground="#263746",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )

        self.clear_button.pack(
            side="left",
            padx=8
        )

        # =====================================================
        # ACTIVITY
        # =====================================================

        tk.Label(
            self.main_frame,
            text="ACTIVITY",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#0b0f14"
        ).pack(
            anchor="w",
            padx=50,
            pady=(0, 10)
        )

        activity_frame = tk.Frame(
            self.main_frame,
            bg="#111820"
        )

        activity_frame.pack(
            fill="x",
            padx=40,
            pady=(0, 25)
        )

        self.activity = tk.Text(
            activity_frame,
            height=12,
            bg="#111820",
            fg="#b9c7d5",
            font=("Consolas", 10),
            relief="flat",
            padx=15,
            pady=15
        )

        self.activity.pack(
            side="left",
            fill="both",
            expand=True
        )

        activity_scroll = tk.Scrollbar(
            activity_frame,
            command=self.activity.yview
        )

        activity_scroll.pack(
            side="right",
            fill="y"
        )

        self.activity.configure(
            yscrollcommand=activity_scroll.set
        )

        # =====================================================
        # LOGS
        # =====================================================

        self.log("ARCHON UI initialized.")
        self.log("AI Brain: READY")
        self.log("Voice System: READY")
        self.log("Browser System: READY")
        self.log("Memory System: READY")
        self.log("Visual System: READY")

        # =====================================================
        # START BUTTON
        # =====================================================

        self.start_button = tk.Button(
            self.main_frame,
            text="START ARCHON",
            command=self.start_archon,
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#17232d",
            activebackground="#263746",
            activeforeground="white",
            relief="flat",
            padx=40,
            pady=15,
            cursor="hand2"
        )

        self.start_button.pack(
            pady=(0, 40)
        )

        self.stop_button = tk.Button(
            self.main_frame,
            text="🛑 STOP ARCHON",
            command=self.stop_archon,
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#7a1f1f",
            activebackground="#a52a2a",
            activeforeground="white",
            relief="flat",
            padx=40,
            pady=15,
            cursor="hand2",
            state="disabled"
        )

        self.stop_button.pack(
            pady=(0, 40)
        )

    # =========================================================
    # IMAGE UPLOAD
    # =========================================================

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:

            image = Image.open(file_path)

            max_width = 800
            max_height = 300

            image.thumbnail(
                (max_width, max_height)
            )

            self.current_image = ImageTk.PhotoImage(image)

            self.visual_label.config(
                image=self.current_image,
                text=""
            )

            # New image = new visual conversation
            clear_visual_memory()

            self.current_image_path = file_path
            set_image(file_path)

            self.task_label.config(
                text="🖼 IMAGE READY"
            )

            self.log(
                f"Image loaded: {file_path}"
            )

            self.analyze_button.config(
                state="normal"
            )

            self.ask_button.config(
                state="normal"
            )

        except Exception as e:

            self.log(
                f"IMAGE ERROR: {e}"
            )

    def analyze_current_image(self):

        if not self.current_image_path:
            self.log("No image selected.")
            return

        self.analyze_button.config(
            state="disabled"
        )

        self.task_label.config(
            text="🧠 ANALYZING IMAGE..."
        )

        self.log("ARCHON Vision analyzing image...")

        thread = threading.Thread(
            target=self.run_vision,
            daemon=True
        )

        thread.start()

    def run_vision(self):

        try:

            result = analyze_image(
                self.current_image_path,
                "Describe this image clearly and explain the important things visible in it."
            )

            self.root.after(
                0,
                lambda: self.show_vision_result(result)
            )

        except Exception as e:

            error_message = str(e)

            self.root.after(
                0,
                lambda msg=error_message:
                    self.show_vision_result(
                        f"Vision error: {msg}"
                    )
            )

    def show_vision_result(self, result):

        self.vision_result.delete(
            "1.0",
            "end"
        )

        self.vision_result.insert(
            "end",
            result
        )

        self.task_label.config(
            text="🧠 VISION COMPLETE"
        )

        self.log(
            "ARCHON Vision analysis complete."
        )

        self.analyze_button.config(
            state="normal"
        )

        self.ask_button.config(
            state="normal"
        )

    def ask_about_image(self):

        if not self.current_image_path:

            self.log(
                "No image selected."
            )

            return

        question = self.question_entry.get().strip()

        if not question:

            self.log(
                "Please enter a question."
            )

            return

        self.ask_button.config(
            state="disabled"
        )

        self.task_label.config(
            text="🧠 THINKING ABOUT IMAGE..."
        )

        self.log(
            f"Vision question: {question}"
        )

        thread = threading.Thread(
            target=self.run_image_question,
            args=(question,),
            daemon=True
        )

        thread.start()

    def run_image_question(self, question):

        try:

            result = analyze_image(
                self.current_image_path,
                question
            )

            self.root.after(
                0,
                lambda: self.show_vision_result(result)
            )

        except Exception as e:

            error_message = str(e)

            self.root.after(
                0,
                lambda msg=error_message:
                    self.show_vision_result(
                        f"Vision error: {msg}"
                    )
            )

    

    # =========================================================
    # CLEAR VISUAL
    # =========================================================

    def clear_visual(self):

        self.current_image = None
        self.current_image_path = None
        clear_image()
        clear_visual_memory()

        self.visual_label.config(
            image="",
            text="ARCHON VISUAL SYSTEM\nREADY"
        )

        self.vision_result.delete(
            "1.0",
            "end"
        )

        self.vision_result.insert(
            "end",
            "ARCHON Vision is ready.\n"
        )

        self.task_label.config(
            text="CURRENT TASK: IDLE"
        )

        self.analyze_button.config(
            state="disabled"
        )

        self.ask_button.config(
            state="disabled"
        )

        self.log(
            "Visual workspace cleared."
        )

    # =========================================================
    # SCROLL
    # =========================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # =========================================================
    # LOGGER
    # =========================================================

    def log(self, message):

        self.activity.insert(
            "end",
            f"[ARCHON] {message}\n"
        )

        self.activity.see("end")

    # =========================================================
    # STATUS
    # =========================================================

    def update_status_display(self, status):

        self.status.config(
            text=f"● {status}"
        )

        if status.startswith("TASK:"):

            task = status.replace(
                "TASK:",
                ""
            ).strip()

            task_display = {
                "BROWSER": "🌐 BROWSER MODE",
                "WEBPAGE": "📄 WEBPAGE MODE",
                "AI": "🧠 AI MODE",
                "SYSTEM": "⚙️ SYSTEM MODE",
                "IDLE": "⚪ STANDBY"
            }

            display_text = task_display.get(
                task,
                f"⚙️ {task} MODE"
            )

            self.task_label.config(
                text=display_text
            )

        self.log(status)

    # =========================================================
    # START ARCHON
    # =========================================================

    def start_archon(self):

        # Do not start another ARCHON if one is already running
        if self.assistant is not None and self.assistant.running:
            self.log("ARCHON is already running.")
            return

        self.start_button.config(
            state="disabled"
        )

        self.stop_button.config(
            state="normal"
        )

        self.status.config(
            text="● ARCHON ACTIVE",
            fg="#00ff99"
        )

        self.log(
            "Starting ARCHON assistant..."
        )

        thread = threading.Thread(
            target=self.run_assistant,
            daemon=True
        )

        self.assistant_thread = thread

        thread.start()


    def stop_archon(self):

        if not hasattr(self, "assistant"):
            return

        if not self.assistant.running:
            return

        self.log(
            "STOP button pressed."
        )

        self.stop_button.config(
            state="disabled"
        )

        self.status.config(
            text="● STOPPING ARCHON...",
            fg="#ffaa00"
        )

        self.log(
            "STOPPING"
        )

        self.assistant.stop()

    # =========================================================
    # ASSISTANT
    # =========================================================

    def run_assistant(self):

        try:

            def update_archon_status(status):

                self.root.after(
                    0,
                    lambda: self.update_status_display(status)
                )

            self.assistant = Assistant(
                status_callback=update_archon_status
            )

            self.root.after(
                0,
                lambda: self.log(
                    "Voice assistant started."
                )
            )

            self.assistant.run()

        except Exception as e:

            error_message = str(e)

            self.root.after(
                0,
                lambda msg=error_message:
                    self.log(
                        f"ERROR: {msg}"
                    )
            )

        finally:

            # Assistant thread has completely finished
            self.root.after(
                0,
                self.archon_finished
            )

    def archon_finished(self):

        self.stop_button.config(
            state="disabled"
        )

        self.start_button.config(
            state="normal"
        )

        self.status.config(
            text="● ARCHON STOPPED",
            fg="#ff5555"
        )

        self.task_label.config(
            text="CURRENT TASK: IDLE"
        )

        self.log(
            "ARCHON completely stopped."
        )


# =============================================================
# START UI
# =============================================================

def start_ui():

    root = tk.Tk()

    app = ArchonUI(root)

    root.mainloop()


if __name__ == "__main__":
    start_ui()