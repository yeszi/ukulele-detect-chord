import tkinter as tk
from tkinter import ttk, messagebox, font
import pyaudio
import numpy as np
import librosa
import threading
import time

class CozyUkuleleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌺 UkCozy Chord Detector")
        self.root.geometry("500x700")
        
        # PALET WARNA COZY 
        self.COLORS = {
            "bg": "#FFF8E1",          
            "header": "#8D6E63",      
            "card": "#FFE0B2",       
            "text": "#4E342E",       
            "accent": "#FF7043",    
            "btn_start": "#66BB6A",  
            "btn_stop": "#EF5350",    
            "bar_fill": "#8D6E63",  
            "bar_bg": "#FFCCBC"       
        }

        self.root.configure(bg=self.COLORS["bg"])

        # --- STYLE CONFIGURATION (TTK) ---
        self.style = ttk.Style()
        self.style.theme_use('clam') 
        
        # Custom Combobox
        self.style.configure("TCombobox", fieldbackground=self.COLORS["bg"], 
                             background=self.COLORS["card"], foreground=self.COLORS["text"])
        
        # Custom Progress Bar (Volume)
        self.style.configure("Cozy.Horizontal.TProgressbar", 
                             background=self.COLORS["bar_fill"], 
                             troughcolor=self.COLORS["bar_bg"], 
                             bordercolor=self.COLORS["bg"],
                             lightcolor=self.COLORS["bar_fill"], 
                             darkcolor=self.COLORS["bar_fill"])

        # ================= UI SETUP =================

        # 1. HEADER FRAME
        header_frame = tk.Frame(root, bg=self.COLORS["header"], height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="🎸 UkCozy Detector Live", font=("Verdana", 22, "bold"),
                 bg=self.COLORS["header"], fg="#FFFFFF").pack(pady=20)

        # 2. MAIN CONTAINER (Penting untuk padding)
        main_frame = tk.Frame(root, bg=self.COLORS["bg"])
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # 3. CHORD DISPLAY (Card Style)
        chord_card = tk.Frame(main_frame, bg=self.COLORS["card"], bd=0, 
                              highlightbackground=self.COLORS["text"], highlightthickness=1)
        chord_card.pack(fill="x", pady=(0, 20), ipady=20)
        
        tk.Label(chord_card, text="Chord Saat Ini:", font=("Helvetica", 10, "italic"),
                 bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(pady=(10,0))
        
        self.lbl_chord = tk.Label(chord_card, text="--", font=("Verdana", 80, "bold"),
                                  bg=self.COLORS["card"], fg=self.COLORS["text"])
        self.lbl_chord.pack()

        # 4. STATUS LABEL
        self.lbl_status = tk.Label(main_frame, text="💤 Menunggu petikan...", font=("Helvetica", 11),
                                   bg=self.COLORS["bg"], fg="#9E9E9E")
        self.lbl_status.pack(pady=(0, 15))

        # 5. CONTROLS FRAME
        control_frame = tk.LabelFrame(main_frame, text=" Pengaturan Audio 🎼 ", 
                                      font=("Helvetica", 10, "bold"),
                                      bg=self.COLORS["bg"], fg=self.COLORS["text"],
                                      bd=2, relief="groove")
        control_frame.pack(fill="x", pady=10, ipady=10, ipadx=10)

        # Microphone Selection
        tk.Label(control_frame, text="Input Microphone:", bg=self.COLORS["bg"], 
                 fg=self.COLORS["text"], font=("Helvetica", 9)).pack(anchor="w", padx=5)
        self.device_combo = ttk.Combobox(control_frame, state="readonly")
        self.device_combo.pack(fill="x", padx=5, pady=(2, 10))

        # Volume Visualizer
        tk.Label(control_frame, text="Volume Input:", bg=self.COLORS["bg"], 
                 fg=self.COLORS["text"], font=("Helvetica", 9)).pack(anchor="w", padx=5)
        self.vol_bar = ttk.Progressbar(control_frame, orient="horizontal",
                                       length=100, mode="determinate", 
                                       style="Cozy.Horizontal.TProgressbar")
        self.vol_bar.pack(fill="x", padx=5, pady=(2, 10))

        # Sensitivity Slider
        tk.Label(control_frame, text="Sensitivitas (Threshold):", bg=self.COLORS["bg"], 
                 fg=self.COLORS["text"], font=("Helvetica", 9)).pack(anchor="w", padx=5)
        
        self.threshold_slider = tk.Scale(control_frame, from_=0, to=100,
                                         orient="horizontal", bg=self.COLORS["bg"], 
                                         fg=self.COLORS["text"], highlightthickness=0,
                                         activebackground=self.COLORS["card"],
                                         troughcolor=self.COLORS["bar_bg"])
        self.threshold_slider.set(20)
        self.threshold_slider.pack(fill="x", padx=5)

        # 6. BIG BUTTON
        self.is_running = False
        self.btn_toggle = tk.Button(main_frame, text="MULAI MAIN 🎵", 
                                    font=("Verdana", 14, "bold"),
                                    bg=self.COLORS["btn_start"], fg="white", 
                                    activebackground="#43A047", activeforeground="white",
                                    relief="flat", cursor="hand2",
                                    command=self.toggle_recording)
        self.btn_toggle.pack(fill="x", pady=20, ipady=8)

        # ================= LOGIC SETUP =================
        self.CHUNK = 2048
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = None

        self.populate_devices()

        # Chord Templates (Sama seperti sebelumnya)
        self.templates = {
            'C':  [1,0,0,0,1,0,0,1,0,0,0,0],
            'D':  [0,0,1,0,0,0,1,0,0,1,0,0],
            'E':  [0,0,0,0,1,0,0,0,1,0,0,1],
            'F':  [1,0,0,0,0,1,0,0,0,1,0,0],
            'G':  [0,0,1,0,0,0,0,1,0,0,0,1],
            'A':  [0,1,0,0,1,0,0,0,0,1,0,0],
            'B':  [0,0,0,1,0,0,1,0,0,0,0,1],
            'Am': [1,0,0,0,0,0,0,0,0,1,0,0],
            'Dm': [0,0,1,0,0,1,0,0,0,1,0,0],
            'Em': [0,0,0,0,1,0,0,1,0,0,0,1],
        }

    # ===================== LOGIC METHODS =======================
    def populate_devices(self):
        devices = []
        count = self.p.get_device_count()
        for i in range(count):
            info = self.p.get_device_info_by_index(i)
            if info.get('maxInputChannels') > 0:
                devices.append(f"{i}: {info.get('name')}")
        self.device_combo['values'] = devices
        if devices: self.device_combo.current(0)

    def toggle_recording(self):
        if not self.is_running:
            try:
                device_idx = int(self.device_combo.get().split(":")[0])
                self.start_audio(device_idx)
            except:
                messagebox.showerror("Oops", "Pilih microphone dulu ya! 🎤")
        else:
            self.stop_audio()

    def start_audio(self, device_idx):
        self.is_running = True
        self.btn_toggle.config(text="STOP 🛑", bg=self.COLORS["btn_stop"])
        self.lbl_status.config(text="🎶 Mendengarkan petikanmu...", fg=self.COLORS["header"])
        
        self.thread = threading.Thread(target=self.audio_loop, args=(device_idx,))
        self.thread.daemon = True
        self.thread.start()

    def stop_audio(self):
        self.is_running = False
        time.sleep(0.1)
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
        except: pass
        
        self.lbl_status.config(text="💤 Istirahat", fg="#9E9E9E")
        self.lbl_chord.config(text="--", fg=self.COLORS["text"])
        self.vol_bar['value'] = 0
        self.btn_toggle.config(text="MULAI MAIN 🎵", bg=self.COLORS["btn_start"])

    def audio_loop(self, device_index):
        try:
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                      rate=self.RATE, input=True,
                                      input_device_index=device_index,
                                      frames_per_buffer=self.CHUNK)

            while self.is_running:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

                vol = np.linalg.norm(audio_data)
                self.vol_bar['value'] = min(vol * 120, 100)

                if vol < (self.threshold_slider.get() / 100):
                    continue

                chroma = librosa.feature.chroma_stft(y=audio_data, sr=self.RATE)
                mean_chroma = np.mean(chroma, axis=1)

                best_chord = "--"
                best_score = 0

                for chord, template in self.templates.items():
                    score = np.dot(mean_chroma, template) / (
                        np.linalg.norm(mean_chroma) * np.linalg.norm(template) + 1e-9
                    )
                    if score > best_score:
                        best_score = score
                        best_chord = chord

                if best_score >= 0.6: # Sedikit lebih strict
                    self.update_gui_chord(best_chord)

        except Exception as e:
            print("Error:", e)
            self.stop_audio()

    def update_gui_chord(self, chord_text):
        # Logic warna dinamis sesuai chord
        color = self.COLORS["accent"] # Default Major (Orange)
        suffix = ""
        
        if chord_text.endswith("m"):
            color = "#5D4037"  # Minor chords warnanya lebih gelap (Dark Brown)
            suffix = " min"
        
        self.lbl_chord.config(text=f"{chord_text}", fg=color)

if __name__ == "__main__":
    root = tk.Tk()
    # Opsional: Tambahkan icon jika punya file .ico
    # root.iconbitmap('ukulele.ico') 
    app = CozyUkuleleApp(root)
    root.mainloop()