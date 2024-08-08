import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from PIL import Image, ImageTk

def detect_formjacking():
    detected = random.choice([True, False])  # Simulating detection
    if detected:
        messagebox.showwarning("Detection", "Formjacking detected!")
        detection_status.set("Formjacking detected!")
    else:
        messagebox.showinfo("Detection", "No formjacking detected.")
        detection_status.set("No formjacking detected.")

def save_to_database():
    status = detection_status.get()
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="yourdatabase"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO detections (status) VALUES (%s)", (status,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Database", "Detection saved to database.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def show_histogram():
    data = [random.randint(0, 100) for _ in range(100)]

    fig, ax = plt.subplots()
    ax.hist(data, bins=20, color='blue', edgecolor='black')
    ax.set_title('Formjacking Detection Histogram')
    ax.set_xlabel('Detection Scores')
    ax.set_ylabel('Frequency')

    canvas_histogram = FigureCanvasTkAgg(fig, master=frame_histogram)
    canvas_histogram.draw()
    canvas_histogram.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def show_pie_chart():
    labels = 'Formjacking Detected', 'No Formjacking'
    sizes = [random.randint(0, 50), random.randint(50, 100)]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode the 1st slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    canvas_piechart = FigureCanvasTkAgg(fig, master=frame_piechart)
    canvas_piechart.draw()
    canvas_piechart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def set_background():
    # Create a Canvas widget to display the background image
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    background = canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.background_photo = background_photo  # Keep a reference to prevent garbage collection

# Initialize ThemedTk
root = ThemedTk(theme="arc")
root.title("ERKEN")
root.geometry("1920x1080")

# Load and set the background image
background_image = Image.open("Erken Background 3.jpg")  # Replace with your image file path
background_image = background_image.resize((1920, 1080), Image.LANCZOS)  # Resize to fit window size
background_photo = ImageTk.PhotoImage(background_image)

# Set the background image on the canvas
set_background()

# Add widgets to the window
detection_status = tk.StringVar()
detection_status.set("Status: Not checked")

# Title label (Above status label)
title_label = ttk.Label(root, text="ERKEN", font=("Helvetica", 24, "bold"))
title_label.place(x=790, y=20, anchor="n")  # Top center

# URL label (Below title label)
url_label = ttk.Label(root, text="Enter Form URL:", font=("Times New Roman", 12))
url_label.place(x=650, y=150, anchor="n")  # Below title label

# URL entry (Below URL label)
url_entry = ttk.Entry(root, width=60)
url_entry.place(x=900, y=150, anchor="n")  # Below URL label

# Status label (Below title label)
label_status = ttk.Label(root, textvariable=detection_status)
label_status.place(x=800, y=200, anchor="n")  # Below title

# Button positions (Middle center)
detect_button = ttk.Button(root, text="Detect Formjacking", command=detect_formjacking)
detect_button.place(x=300, y=250, anchor="center")

save_button = ttk.Button(root, text="Save to Database", command=save_to_database)
save_button.place(x=600, y=250, anchor="center")

histogram_button = ttk.Button(root, text="Show Histogram", command=show_histogram)
histogram_button.place(x=1000, y=250, anchor="center")

piechart_button = ttk.Button(root, text="Show Pie Chart", command=show_pie_chart)
piechart_button.place(x=1300, y=250, anchor="center")

# Frame for histogram (Position at specific x and y coordinates)
frame_histogram = ttk.Frame(root, width=500, height=350)
frame_histogram.place(x=100, y=300)  # Adjust x and y for desired position

# Frame for pie chart (Position at specific x and y coordinates)
frame_piechart = ttk.Frame(root, width=500, height=350)
frame_piechart.place(x=800, y=300)  # Adjust x and y for desired position

# Run the main loop
root.mainloop()
