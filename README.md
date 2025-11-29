# 🌺 UkCozy Real-Time Chord Detector

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Librosa](https://img.shields.io/badge/Audio-Librosa-E1620E?style=for-the-badge&logo=soundcloud&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-2C3E50?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **"Strum your ukulele, sip your coffee, and let UkuBuddy detect your chords in style."**

**UkuBuddy** is a desktop application built with Python that detects Ukulele chords in real-time. Unlike traditional tuners or chord detectors that look technical and rigid, UkuBuddy features a **"Coffee Shop Aesthetic"** UI—designed to make your jamming session feel warm, organic, and cozy.

---

## 📸 Screenshots

![App Screenshot](https://via.placeholder.com/600x400?text=Place+Your+Screenshot+Here)

---

## ✨ Key Features

* **🎧 Real-Time Detection:** Instantly identifies chords as you play using microphone input.
* **☕ Cozy UI/UX:** A warm *Latte & Wood* color palette designed for a relaxing user experience.
* **🎨 Dynamic Feedback:**
    * **Major Chords:** Glow in **Sunset Orange**.
    * **Minor Chords:** Displayed in **Dark Coffee Brown**.
* **🎚️ Audio Control:**
    * Select input device (External/Internal Mic).
    * Visual Volume Bar (Custom styled).
    * Adjustable Sensitivity Threshold (to filter background noise).

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI:** Tkinter (with `ttk` styling)
* **Audio Input:** PyAudio
* **Signal Processing:** Librosa & NumPy (Chroma Feature Extraction)
* **Concurrency:** Python Threading

---

## 🚀 Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/ukubuddy.git](https://github.com/yourusername/ukubuddy.git)
cd ukubuddy
