import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import trimesh

def choose_files(entry_widget):
    paths = filedialog.askopenfilenames(filetypes=[("STL files", "*.stl")])
    if paths:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ";".join(paths))

def choose_output_folder(entry_widget):
    path = filedialog.askdirectory()
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)

def compress_stl(input_paths, output_path, target_triangles, progress_bar, progress_label):
    files = input_paths.split(";")

    total_files = len(files)
    for i, file_path in enumerate(files):
        progress = int((i + 1) / total_files * 100)
        progress_bar["value"] = progress
        progress_label["text"] = f"Progress: {i+1}/{total_files} ({progress}%)"
        window.update_idletasks()

        mesh = trimesh.load_mesh(file_path)
        simplified_mesh = mesh.simplify_quadric_decimation(target_triangles)
        output_file_path = os.path.join(output_path, os.path.basename(file_path))
        simplified_mesh.export(output_file_path)

def compress():
    input_paths = input_entry.get()
    output_path = output_entry.get()
    target_triangles = int(slider.get())

    progress_bar["value"] = 0
    progress_label["text"] = "Progress: 0/0 (0%)"
    compress_stl(input_paths, output_path, target_triangles, progress_bar, progress_label)
    progress_bar["value"] = 100
    progress_label["text"] = "Progress: Complete"

window = tk.Tk()
window.title("STL Compresser | Made by github@fan-ziqi")

input_label = tk.Label(window, text="Select Input File(s):")
input_label.pack()
input_frame = tk.Frame(window)
input_frame.pack()

input_entry = tk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT)

choose_button = tk.Button(input_frame, text="Browse", command=lambda: choose_files(input_entry))
choose_button.pack(side=tk.LEFT)

output_label = tk.Label(window, text="Select Output Folder:")
output_label.pack()
output_frame = tk.Frame(window)
output_frame.pack()

output_entry = tk.Entry(output_frame, width=50)
output_entry.pack(side=tk.LEFT)

output_button = tk.Button(output_frame, text="Browse", command=lambda: choose_output_folder(output_entry))
output_button.pack(side=tk.LEFT)

slider_label = tk.Label(window, text="Select Target Triangles (100-10000):")
slider_label.pack()

slider = tk.Scale(window, from_=100, to=10000, orient=tk.HORIZONTAL, length=300)
slider.set(1000)
slider.pack()

progress_frame = tk.Frame(window)
progress_frame.pack()

progress_label = tk.Label(progress_frame, text="Progress: 0/0 (0%)")
progress_label.pack()

progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
progress_bar.pack()

compress_button = tk.Button(window, text="Compress", command=compress)
compress_button.pack()

window.geometry("450x250")

window.mainloop()
