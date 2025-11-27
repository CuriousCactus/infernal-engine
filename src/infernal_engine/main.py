import os
import tkinter as tk
from tkinter import ttk

from infernal_engine.utils.convert_mocap import convert_mocap

MOD_NAME = "ReturnToTheHouseOfHope_295379f9-b5ee-119f-54c1-9f6bd887046b"
DATA_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Baldurs Gate 3/Data"
UNPACKED_DATA_PATH = "C:/Users/Shadow/bg3-modders-multitool/UnpackedData"
HANDLE = "h68aa9134g0c15g423cga4d8gd2a8f5d5a1c1"  # Gal and her goldmine
# HANDLE = "had879ee5ga68fg4aa0g8f5fg0687c2df1aa4"  # Heads will roll
DIALOG_FILE = "WYR_SharessCaress_Taproom_Threeway_NymphDrunkFist"
# DIALOG_FILE = "LOW_HouseOfHope_Hope"


def on_submit(
    mod_name_entry: tk.Entry,
    game_data_path_entry: tk.Entry,
    unpacked_data_path_entry: tk.Entry,
    handle_entry: tk.Entry,
    dialog_entry: tk.Entry,
):
    mod_name_value = mod_name_entry.get()
    game_data_path_value = game_data_path_entry.get()
    unpacked_data_path_value = unpacked_data_path_entry.get()

    os.environ["MOD_NAME"] = mod_name_value
    os.environ["DATA_PATH"] = game_data_path_value
    os.environ["UNPACKED_DATA_PATH"] = unpacked_data_path_value

    handle_value = handle_entry.get()
    dialog_value = dialog_entry.get()

    convert_mocap(handle_value, dialog_value)


def main():
    root = tk.Tk()
    root.title("Infernal Engine Mocap Converter")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Mod Name:").grid(column=0, row=0, sticky="w")
    mod_name_entry = ttk.Entry(frm, width=100)
    mod_name_entry.insert(0, MOD_NAME)
    mod_name_entry.grid(column=0, row=1, columnspan=2, pady=5)

    ttk.Label(frm, text="Game Data Path:").grid(column=0, row=2, sticky="w")
    game_data_path_entry = ttk.Entry(frm, width=100)
    game_data_path_entry.insert(0, DATA_PATH)
    game_data_path_entry.grid(column=0, row=3, columnspan=2, pady=5)

    ttk.Label(frm, text="Unpacked Data Path:").grid(column=0, row=4, sticky="w")
    unpacked_data_path_entry = ttk.Entry(frm, width=100)
    unpacked_data_path_entry.insert(0, UNPACKED_DATA_PATH)
    unpacked_data_path_entry.grid(column=0, row=5, columnspan=2, pady=5)

    ttk.Label(frm, text="Handle:").grid(column=0, row=6, sticky="w")
    handle_entry = ttk.Entry(frm, width=100)
    handle_entry.insert(0, HANDLE)
    handle_entry.grid(column=0, row=7, columnspan=2, pady=5)

    ttk.Label(frm, text="Dialog File:").grid(column=0, row=8, sticky="w")
    dialog_entry = ttk.Entry(frm, width=100)
    dialog_entry.insert(0, DIALOG_FILE)
    dialog_entry.grid(column=0, row=9, columnspan=2, pady=5)

    convert_btn = ttk.Button(
        frm,
        text="Convert",
        command=lambda: on_submit(
            mod_name_entry,
            game_data_path_entry,
            unpacked_data_path_entry,
            handle_entry,
            dialog_entry,
        ),
    )
    convert_btn.grid(column=0, row=10, sticky="w")

    quit_btn = ttk.Button(frm, text="Quit", command=root.destroy)
    quit_btn.grid(column=1, row=10, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    main()
