import tkinter as tk
from tkcalendar import Calendar
import os
from tkinter.filedialog import askdirectory
from datetime import datetime, date, time
import shutil

from_path = askdirectory()
new_folder_1 = os.path.basename(from_path)
to_path = askdirectory()

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

def process_files(path_1, path_2, date):
    for root, dirs, files in os.walk(path_1):
        for file in files:
            the_source = root
            new_folder_2 = os.path.basename(the_source)
            creation_date = datetime.strptime(check_year(os.path.join(root, file)), "%Y-%m-%d")
            if date < creation_date:
                new_path = os.path.join(os.path.join(path_2, new_folder_1), new_folder_2)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                shutil.copy(os.path.join(the_source, file), new_path)

process_files(from_path, to_path, choosed_datetime)