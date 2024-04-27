import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
import os
import subprocess
import json

keyword_entries = []  # Declare globally

def browse_folder():  # input in abc.py
    folder_path = filedialog.askdirectory(
        initialdir="/",
        title="Select a Folder"
    )
    file_path_var.set(folder_path)

    # Filter and display PDF and DOCX files
    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1].lower() in ('.pdf', '.docx'):
            print(filename)  # Display the filename in the terminal

def generate_textboxes():
    global keyword_entries

    category_data = []

    # Collect data from dropdowns
    for category_frame in category_frames:
        category_name = category_var[category_frame].get()
        num_keywords = int(keyword_vars[category_frame].get())
        category_data.append((category_name, num_keywords))

    # Clear old textboxes
    clear_existing_textboxes()

    # Generate new textboxes and save their references
    keyword_entries.clear()  # Clear before generating new entries
    for i, (category_name, num_keywords) in enumerate(category_data):
        label = tk.Label(root, text=f"{category_name}:")
        label.pack()
        for _ in range(num_keywords):
            entry = tk.Entry(root)
            entry.pack()
            keyword_entries.append(entry)

    # Place save button below textboxes
    save_button = tk.Button(root, text="Categorize", command=save_to_backup)
    save_button.pack()


def save_to_backup(): # connect to 
    global keyword_entries

    category_data = {}

    # Collect data from dropdowns and textboxes
    keyword_start_index = 0
    for i, category_frame in enumerate(category_frames):
        category_name = category_var[category_frame].get()
        num_keywords = int(keyword_vars[category_frame].get())

        keywords = keyword_entries[keyword_start_index:keyword_start_index + num_keywords]
        category_data[category_name] = [entry.get() for entry in keywords]

        keyword_start_index += num_keywords

    #print(category_data)
    subprocess.run(["python3", "augmentA.py", json.dumps(category_data)])


def clear_existing_textboxes():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
            widget.destroy()


def update_category_dropdowns():
    # Destroy old category frames
    for frame in category_frames:
        frame.destroy()
    category_frames.clear()

    # Create new frames
    num_categories = num_categories_var.get()
    for i in range(num_categories):
        frame = tk.Frame(root)
        frame.pack()
        category_frames.append(frame)

        tk.Label(frame, text="Category Name:").pack()
        category_var[frame] = tk.StringVar(frame)
        tk.Entry(frame, textvariable=category_var[frame]).pack()

        tk.Label(frame, text="Number of Keywords:").pack()
        keyword_vars[frame] = tk.IntVar(frame)
        keyword_options = [1, 2, 3, 4, 5]
        ttk.Combobox(frame, textvariable=keyword_vars[frame],
                     values=keyword_options).pack()





# --- Main Program ---
root = tk.Tk()
root.title("BuzzMatchTester")

# UI Elements for File Input
file_frame = tk.Frame(root)  # Frame to hold file path and button
file_frame.pack()

file_path_label = tk.Label(file_frame, text="File Path:")
file_path_label.pack(side='left')

file_path_var = tk.StringVar(root)
file_path_entry = tk.Entry(file_frame, textvariable=file_path_var)
file_path_entry.pack(side='left')

browse_button = tk.Button(file_frame, text="Browse Folder", command=browse_folder)  # Change browse_file to browse_folder
browse_button.pack(side='left')

# Dropdown for Number of Categories
num_categories_label = tk.Label(root, text="Number of Categories:")
num_categories_label.pack()

num_categories_options = [0,1, 2, 3, 4, 5]
num_categories_var = tk.IntVar(root)
num_categories_var.set(num_categories_options[0])
num_categories_dropdown = ttk.Combobox(root, textvariable=num_categories_var,
                                       values=num_categories_options)
num_categories_dropdown.pack()

category_frames = []  
category_var = {}  
keyword_vars = {} 

update_category_dropdowns()  # Initial setup


# Generate Button
generate_button = tk.Button(root, text="Generate Textboxes", command=generate_textboxes)
generate_button.pack()

num_categories_dropdown.bind("<<ComboboxSelected>>", lambda _: update_category_dropdowns())  # After updating dropdowns

root.mainloop()
