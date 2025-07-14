import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import time
import base64
import random

# Global variables
root = tk.Tk()
video_label = None
bg_label = None
url_var = tk.StringVar()
encrypted_data = ""
bg_cap = None

def module1_intro():
    cap = cv2.VideoCapture("intro_video.mp4")
    play_video(cap, module2_setup, delay=10)

def play_video(cap, next_module, delay=0):
    def stream():
        global video_label
        start_time = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (1280, 720))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))

            if video_label is None:
                video_label = tk.Label(root)
                video_label.pack(fill="both", expand=True)

            video_label.imgtk = img
            video_label.configure(image=img)

            if time.time() - start_time > delay:
                break
            time.sleep(0.03)

        cap.release()
        if video_label:
            video_label.destroy()
        next_module()

    threading.Thread(target=stream, daemon=True).start()

def module2_setup():
    bg_video("animated_bg_module2.mp4")

    title = tk.Label(root, text="ERKEN", font=("Helvetica", 32, "bold"), bg="black", fg="white")
    title.place(relx=0.5, y=20, anchor="n")

    url_label = tk.Label(root, text="Enter Form URL:", font=("Helvetica", 14), bg="black", fg="white")
    url_label.place(relx=0.5, rely=0.3, anchor="center")

    url_entry = ttk.Entry(root, width=50, textvariable=url_var)
    url_entry.place(relx=0.5, rely=0.4, anchor="center")

    proceed_button = ttk.Button(root, text="Proceed", command=module3_setup)
    proceed_button.place(relx=0.5, rely=0.5, anchor="center")

def module3_setup():
    clear_widgets()
    bg_video("animated_bg_module3.mp4")

    title = tk.Label(root, text="Monitoring Form for 24 Hours", font=("Helvetica", 20, "bold"), bg="black", fg="white")
    title.place(relx=0.5, y=20, anchor="n")

    url_info = tk.Label(root, text=f"URL: {url_var.get()}", font=("Helvetica", 12), bg="black", fg="white")
    url_info.place(relx=0.5, y=70, anchor="n")

    monitor_label = tk.Label(root, text="Monitoring Started...", font=("Helvetica", 14), bg="black", fg="lightgreen")
    monitor_label.place(relx=0.5, y=120, anchor="n")

    terminate_btn = ttk.Button(root, text="Terminate Monitoring",
                               command=lambda: monitor_label.config(text="Monitoring Terminated!", fg="red"))
    terminate_btn.place(relx=0.5, y=170, anchor="n")

    encrypt_btn = ttk.Button(root, text="Encrypt Sample Data", command=encrypt_data)
    encrypt_btn.place(relx=0.4, y=250, anchor="n")

    decrypt_btn = ttk.Button(root, text="Decrypt Data", command=decrypt_data)
    decrypt_btn.place(relx=0.6, y=250, anchor="n")

    global data_label
    data_label = tk.Label(root, text="", font=("Courier", 12), wraplength=1000, bg="black", fg="white")
    data_label.place(relx=0.5, rely=0.5, anchor="center")

def encrypt_data():
    global encrypted_data, data_label
    sample_text = f"UserFormData{random.randint(1000,9999)}"
    encrypted = base64.b64encode(sample_text.encode()).decode()
    encrypted_data = encrypted
    data_label.config(text=f"Encrypted Data: {encrypted}", fg="cyan")

def decrypt_data():
    global encrypted_data, data_label
    if encrypted_data:
        try:
            decrypted = base64.b64decode(encrypted_data.encode()).decode()
            data_label.config(text=f"Decrypted Data: {decrypted}", fg="lime")
        except Exception as e:
            data_label.config(text=f"Decryption failed: {str(e)}", fg="red")
    else:
        data_label.config(text="No data to decrypt", fg="red")

def bg_video(video_path):
    global bg_cap, bg_label
    bg_cap = cv2.VideoCapture(video_path)
    bg_label = tk.Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_bg():
        global bg_cap, bg_label
        while bg_cap.isOpened():
            ret, frame = bg_cap.read()
            if not ret:
                bg_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            frame = cv2.resize(frame, (1280, 720))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            bg_label.imgtk = img
            bg_label.configure(image=img)
            time.sleep(0.03)

    threading.Thread(target=update_bg, daemon=True).start()

def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

# Initialize
root.title("ERKEN")
root.geometry("1280x720")
root.resizable(False, False)

# Start Module 1 (Intro)
module1_intro()
root.mainloop()
