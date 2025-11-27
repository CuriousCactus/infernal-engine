# if __name__ == "__main__":
HANDLE = "h68aa9134g0c15g423cga4d8gd2a8f5d5a1c1"  # Gal and her goldmine
# HANDLE = "had879ee5ga68fg4aa0g8f5fg0687c2df1aa4"  # Heads will roll
DIALOG_FILE = "WYR_SharessCaress_Taproom_Threeway_NymphDrunkFist"
# DIALOG_FILE = "LOW_HouseOfHope_Hope"
#     convert_mocap(HANDLE, DIALOG_FILE)


import tkinter as tk
from tkinter import ttk

from infernal_engine.utils.convert_mocap import convert_mocap


def on_submit(handle_entry: tk.Entry, dialog_entry: tk.Entry):
    """Called when the button is clicked; reads the entry and passes it on."""
    handle_value = handle_entry.get()
    dialog_value = dialog_entry.get()
    convert_mocap(handle_value, dialog_value)


def main():
    root = tk.Tk()
    root.title("Infernal Engine Mocap Converter")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Handle:").grid(column=0, row=0, sticky="w")

    handle_entry = ttk.Entry(frm, width=100)
    handle_entry.insert(0, HANDLE)
    handle_entry.grid(column=0, row=1, columnspan=2, pady=5)

    ttk.Label(frm, text="Dialog File:").grid(column=0, row=2, sticky="w")

    dialog_entry = ttk.Entry(frm, width=100)
    dialog_entry.insert(0, DIALOG_FILE)
    dialog_entry.grid(column=0, row=3, columnspan=2, pady=5)

    convert_btn = ttk.Button(
        frm, text="Convert", command=lambda: on_submit(handle_entry, dialog_entry)
    )
    convert_btn.grid(column=0, row=4, sticky="w")

    quit_btn = ttk.Button(frm, text="Quit", command=root.destroy)
    quit_btn.grid(column=1, row=4, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    main()
