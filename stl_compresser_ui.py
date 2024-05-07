import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import trimesh
import threading

def choose_files(entry_widget):
    # Function to choose input files
    paths = filedialog.askopenfilenames(filetypes=[("STL files", "*.stl")])
    if paths:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ";".join(paths))

def choose_output_folder(entry_widget):
    # Function to choose output folder
    path = filedialog.askdirectory()
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)

def compress_stl(input_paths, output_path, target_triangles, progress_bar, progress_label, on_complete):
    # Function to compress STL files
    files = input_paths.split(";")

    total_files = len(files)
    progress_per_file = 100 / total_files

    for i, file_path in enumerate(files):
        mesh = trimesh.load_mesh(file_path)
        simplified_mesh = mesh.simplify_quadric_decimation(target_triangles)
        output_file_path = os.path.join(output_path, os.path.basename(file_path))
        simplified_mesh.export(output_file_path)

        # Update progress bar
        progress = int((i + 1) * progress_per_file)
        progress_label["text"] = f"Progress: {i + 1}/{total_files} ({progress}%)"

        # Update progress bar and interface after processing each file
        progress_bar["value"] = progress
        window.update_idletasks()

    # Call the callback function after compression is complete
    on_complete()

def compress():
    input_paths = input_entry.get()
    output_path = output_entry.get()

    # Check if input and output paths are empty
    if not input_paths or not output_path:
        # Show a message to the user indicating missing input/output
        tk.messagebox.showinfo("Error", "Please select input file(s) and output folder.")
        return

    # Disable buttons, entry, and slider
    compress_button.config(state=tk.DISABLED)
    choose_button.config(state=tk.DISABLED)
    output_button.config(state=tk.DISABLED)
    slider.config(state=tk.DISABLED)
    input_entry.config(state=tk.DISABLED)
    output_entry.config(state=tk.DISABLED)

    target_triangles = int(slider.get())

    progress_bar["value"] = 0
    progress_label["text"] = "Progress: 0/0 (0%)"

    # Define callback function after compression thread finishes
    def on_compress_finished():
        # Enable buttons, entry, and slider
        compress_button.config(state=tk.NORMAL)
        choose_button.config(state=tk.NORMAL)
        output_button.config(state=tk.NORMAL)
        slider.config(state=tk.NORMAL)
        input_entry.config(state=tk.NORMAL)
        output_entry.config(state=tk.NORMAL)

    # Create a thread to perform compression operation
    compress_thread = threading.Thread(target=compress_stl,
                                       args=(input_paths, output_path, target_triangles, progress_bar, progress_label,
                                             on_compress_finished))

    # Start the thread
    compress_thread.start()

root = tk.Tk()
root.title("STL Compressor")
root.resizable(False, False)  # Disable resizing

window = tk.Frame(root)

# Input selection
input_label = tk.Label(window, text="Select Input File(s):")
input_label.pack()
input_frame = tk.Frame(window)
input_frame.pack()

input_entry = tk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT)

choose_button = tk.Button(input_frame, text="Browse", command=lambda: choose_files(input_entry))
choose_button.pack(side=tk.LEFT)

# Output selection
output_label = tk.Label(window, text="Select Output Folder:")
output_label.pack()
output_frame = tk.Frame(window)
output_frame.pack()

output_entry = tk.Entry(output_frame, width=50)
output_entry.pack(side=tk.LEFT)

output_button = tk.Button(output_frame, text="Browse", command=lambda: choose_output_folder(output_entry))
output_button.pack(side=tk.LEFT)

# Slider for selecting target triangles
slider_label = tk.Label(window, text="Select Target Triangles (100-10000):")
slider_label.pack()

slider = tk.Scale(window, from_=100, to=10000, orient=tk.HORIZONTAL, length=300)
slider.set(1000)
slider.pack()

# Progress bar and label
progress_frame = tk.Frame(window)
progress_frame.pack()

progress_label = tk.Label(progress_frame, text="Progress: 0/0 (0%)")
progress_label.pack()

progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
progress_bar.pack()

# Compression button
compress_button = tk.Button(window, text="Compress", command=compress)
compress_button.pack()

separator = ttk.Separator(window, orient='horizontal')
separator.pack(fill='x')

bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

version_label = tk.Label(bottom_frame, text="STL Compressor v1.2")
version_label.pack(side=tk.LEFT)

licence_label = tk.Label(bottom_frame, text="Made by github@fan-ziqi")
licence_label.pack(side=tk.RIGHT)

window.grid(row=0, column=0)

window.mainloop()
