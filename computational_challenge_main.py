import tkinter as tk
import importlib
import sys
import os
from PIL import Image, ImageTk
from main_data import data_main as data

columns = 5
tile_width = 270
tile_height = 330
thumb_size = (180, 180)
canvas_size = 190

thumbnail_images = {}

def open_task(number):
    task_path = os.path.join(data.TASK_DIR, f"Task {number}")
    if task_path not in sys.path:
        sys.path.insert(0, task_path)

    module = importlib.import_module(data.tasks[number][1])
    module.open_window(tk.Toplevel(root))

def load_thumbnail(number):
    path = data.thumbnail_path(number)
    if path is None:
        return None

    img = Image.open(path)
    img = img.resize(thumb_size, Image.LANCZOS)

    photo = ImageTk.PhotoImage(img, master = root)
    thumbnail_images[number] = photo
    return photo

root = tk.Tk()
root.title("BPhO Computational Challenge")
root.attributes("-fullscreen", True)
root.configure(bg = "#eeeeee")

title_box = tk.Frame(root, bd = 3, relief = "solid", bg = "white")
title_box.pack(pady = 25)

tk.Label(title_box, text = "BPhO Computational Challenge", font = ("Segoe UI", 36, "bold"), bg = "white", fg = "black").pack(padx = 30, pady = 12)

main_frame = tk.Frame(root, bg = "#eeeeee")
main_frame.pack(expand = True)

for index, number in enumerate(data.tasks):
    name = data.tasks[number][0]

    tile = tk.Frame(main_frame, width = tile_width, height = tile_height, bd = 2, relief = "raised", bg = "white")
    tile.grid(row = index // columns, column = index % columns, padx = 12, pady = 12)
    tile.grid_propagate(False)

    tk.Label(tile, text = f"TASK {number}", font = ("Segoe UI", 12, "bold"), bg = "white").pack(pady = (10, 5))

    image_frame = tk.Frame(tile, width = 210, height = 210, bg = "white")
    image_frame.pack(pady = 8)
    image_frame.pack_propagate(False)

    canvas = tk.Canvas(image_frame, width = canvas_size, height = canvas_size, bg = "white", highlightthickness = 1, highlightbackground = "black")
    canvas.pack(padx = 10, pady = 10)

    photo = load_thumbnail(number)
    if photo:
        canvas.create_image(canvas_size // 2, canvas_size // 2, image = photo)
    else:
        canvas.create_text(canvas_size // 2, canvas_size // 2, text = "No preview", fill = "gray")

    tk.Label(tile, text = name, wraplength = 230, justify = "center", font = ("Segoe UI", 11), height = 2, bg = "white").pack(fill = "x", padx = 5)

    tk.Button(tile, text = "Open", command = lambda n = number: open_task(n), width = 10).pack(pady = 8)

tk.Button(root, text = "Close", command = root.destroy, font = ("Segoe UI", 10), width = 9).place(relx = 0.01, rely = 0.98, anchor = "sw")

root.mainloop()