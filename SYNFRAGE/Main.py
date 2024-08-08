import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pymysql.cursors
from datetime import datetime

# Database connection
def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user='your_actual_username',  # Replace with your actual username
            password='your_actual_password',  # Replace with your actual password
            database='syn_flood_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connection to MySQL database was successful")
    except pymysql.MySQLError as e:
        print(f"Error: '{e}'")
    return connection

# Database functions
def fetch_logs():
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM syn_block_log")
    rows = cursor.fetchall()
    connection.close()
    return rows

def insert_log(ip, reason):
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()
    query = "INSERT INTO syn_block_log (blocked_ip, block_date, reason) VALUES (%s, %s, %s)"
    values = (ip, datetime.now(), reason)
    cursor.execute(query, values)
    connection.commit()
    connection.close()

def test_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='your_actual_username',
            password='your_actual_password',
            database='syn_flood_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection.open:
            print("Connection successful")
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Connection error: '{e}'")

test_connection()

# GUI functions
def on_block_button_click():
    ip = ip_entry.get()
    reason = reason_entry.get()
    block_ip(ip)
    insert_log(ip, reason)
    update_log_table()

def update_log_table():
    for row in tree.get_children():
        tree.delete(row)
    logs = fetch_logs()
    for log in logs:
        tree.insert('', tk.END, values=log)

def block_ip(ip_address):
    # Placeholder for blocking IP address logic
    print(f"Blocking IP: {ip_address}")

# Tkinter setup
app = tk.Tk()
app.title("SYNFRAGE")

# Create a canvas for background image
canvas = tk.Canvas(app, width=1920, height=1080)  # Set size to 1920x1080
canvas.pack(fill=tk.BOTH, expand=True)

# Load the background image
bg_image = Image.open("SYN Flood Background.png")  # Replace with your image file
bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

def update_background_image(event):
    # Resize the image to fit 1920x1080
    resized_image = bg_image.resize((1920, 1080), Image.LANCZOS)
    bg_photo_resized = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, image=bg_photo_resized, anchor=tk.NW)
    canvas.image = bg_photo_resized  # Keep a reference to avoid garbage collection

# Bind the resize event
canvas.bind("<Configure>", update_background_image)

frame = tk.Frame(canvas, bg='white')  # Added background color for visibility
frame.place(relwidth=1, relheight=1)  # Cover the entire canvas

tk.Label(frame, text="SYNFRAGE", font=("Bold Italic", 24)).place(x=750, y=50)

# Positioning widgets using place
tk.Label(frame, text="IP Address").place(x=650, y=150)
tk.Label(frame, text="Reason").place(x=650, y=200)

ip_entry = tk.Entry(frame)
ip_entry.place(x=750, y=150, width=200)

reason_entry = tk.Entry(frame)
reason_entry.place(x=750, y=200, width=200)

block_button = tk.Button(frame, text="Block IP", command=on_block_button_click)
block_button.place(x=750, y=250)

tree = ttk.Treeview(frame, columns=("id", "blocked_ip", "block_date", "reason"), show='headings')
tree.heading("id", text="ID")
tree.heading("blocked_ip", text="Blocked IP")
tree.heading("block_date", text="Block Date")
tree.heading("reason", text="Reason")
tree.place(x=400, y=400, width=800, height=250)

update_log_table()

app.mainloop()
