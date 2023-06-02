import tkinter as tk
from tkcalendar import Calendar
import os
from tkinter.filedialog import askdirectory
from datetime import datetime, date, time
import shutil
import pathlib

from_path = askdirectory()
start = os.path.dirname(from_path)
to_path = askdirectory()
extensions = ['.mp3', '.wav', '.flac']

def choose_year():
    root = tk.Tk()
    def get_selected_date():
        nonlocal selected_date
        selected_date = calendar.selection_get()
        root.destroy()
    selected_date = None
    calendar = Calendar(root, selectmode='day', year=2023, month=5, day=13)
    calendar.pack()
    button = tk.Button(root, text="OK", command=get_selected_date)
    button.pack()
    root.mainloop()
    return selected_date if selected_date is not None else None

choosed_date = datetime.strptime(str(choose_year()), "%Y-%m-%d")
choosed_datetime = datetime.combine(choosed_date, time.min)

def check_year(item):
    creation_time = os.path.getctime(item)
    creation_date = datetime.fromtimestamp(creation_time).date()
    creation_date = datetime.combine(creation_date, datetime.min.time())
    formatted_date = creation_date.strftime('%Y-%m-%d')
    return formatted_date

def process_files(path, path1, date):
    count = 0
    tree = os.walk(path)
    for root in tree:
        files = os.listdir(root[0])
        for file in files:
            ext = pathlib.Path(file).suffix
            if ext not in extensions:
                continue
            if os.path.isfile(os.path.join(root[0],file)):
                creation_date = datetime.strptime(check_year(os.path.join(root[0], file)), "%Y-%m-%d")
                if date < creation_date:
                    path2 = os.path.relpath(root[0],start)
                    destination = os.path.join(path1, path2)
                    if not os.path.exists(destination):
                        os.makedirs(destination)
                    shutil.copy(os.path.join(root[0], file), destination)
                    count += 1
    return count

result = process_files(from_path, to_path, choosed_datetime)
print(f'Copied {result} files.')