import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from infernal_engine.utils.convert_mocap import convert_mocap

# Default values
MOD_NAME = "ReturnToTheHouseOfHope_295379f9-b5ee-119f-54c1-9f6bd887046b"
DATA_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Baldurs Gate 3/Data"
UNPACKED_DATA_PATH = "C:/Users/Shadow/bg3-modders-multitool/UnpackedData"
DIVINE_PATH = "C:/Users/Shadow/ExportTool-v1.20-b3/Packed/Tools/Divine.exe"
HANDLE = "h68aa9134g0c15g423cga4d8gd2a8f5d5a1c1"
DIALOG_FILE = "WYR_SharessCaress_Taproom_Threeway_NymphDrunkFist"

# Settings file path
SETTINGS_DIR = Path().home() / "AppData/Roaming/InfernalEngine"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"


def load_settings():
    """Load settings from file, return defaults if file doesn't exist."""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE) as f:
            return json.load(f)

    return {
        "mod_name": MOD_NAME,
        "game_data_path": DATA_PATH,
        "unpacked_data_path": UNPACKED_DATA_PATH,
        "divine_path": DIVINE_PATH,
        "handle": HANDLE,
        "dialog_file": DIALOG_FILE,
    }


def save_settings(
    mod_name: str,
    game_data_path: str,
    unpacked_data_path: str,
    divine_path: str,
    handle: str,
    dialog_file: str,
):
    """Save settings to file."""
    os.makedirs(SETTINGS_DIR, exist_ok=True)

    with open(SETTINGS_FILE, "w") as f:
        json.dump(
            {
                "mod_name": mod_name,
                "game_data_path": game_data_path,
                "unpacked_data_path": unpacked_data_path,
                "divine_path": divine_path,
                "handle": handle,
                "dialog_file": dialog_file,
            },
            f,
            indent=4,
        )


def on_submit(
    mod_name_entry: tk.Entry,
    game_data_path_entry: tk.Entry,
    unpacked_data_path_entry: tk.Entry,
    divine_path_entry: tk.Entry,
    handle_entry: tk.Entry,
    dialog_entry: tk.Entry,
    prog_var,
    root,
):
    # Save settings
    save_settings(
        mod_name_entry.get(),
        game_data_path_entry.get(),
        unpacked_data_path_entry.get(),
        divine_path_entry.get(),
        handle_entry.get(),
        dialog_entry.get(),
    )

    os.environ["MOD_NAME"] = mod_name_entry.get()
    os.environ["DATA_PATH"] = game_data_path_entry.get()
    os.environ["UNPACKED_DATA_PATH"] = unpacked_data_path_entry.get()
    os.environ["DIVINE_PATH"] = divine_path_entry.get()

    convert_mocap(handle_entry.get(), dialog_entry.get(), prog_var, root)


def on_quit(
    root,
    mod_name_entry: tk.Entry,
    game_data_path_entry: tk.Entry,
    unpacked_data_path_entry: tk.Entry,
    divine_path_entry: tk.Entry,
    handle_entry: tk.Entry,
    dialog_entry: tk.Entry,
):
    save_settings(
        mod_name_entry.get(),
        game_data_path_entry.get(),
        unpacked_data_path_entry.get(),
        divine_path_entry.get(),
        handle_entry.get(),
        dialog_entry.get(),
    )

    root.destroy()


def main():
    settings = load_settings()

    root = tk.Tk()
    root.title("Infernal Engine Mocap Converter")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Mod Name:").grid(column=0, row=0, sticky="w")
    mod_name_entry = ttk.Entry(frm, width=100)
    mod_name_entry.insert(0, settings["mod_name"])
    mod_name_entry.grid(column=0, row=1, columnspan=2, pady=5)

    ttk.Label(frm, text="Game Data Path:").grid(column=0, row=2, sticky="w")
    game_data_path_entry = ttk.Entry(frm, width=100)
    game_data_path_entry.insert(0, settings["game_data_path"])
    game_data_path_entry.grid(column=0, row=3, columnspan=2, pady=5)

    ttk.Label(frm, text="Unpacked Data Path:").grid(column=0, row=4, sticky="w")
    unpacked_data_path_entry = ttk.Entry(frm, width=100)
    unpacked_data_path_entry.insert(0, settings["unpacked_data_path"])
    unpacked_data_path_entry.grid(column=0, row=5, columnspan=2, pady=5)

    ttk.Label(frm, text="Divine Path:").grid(column=0, row=6, sticky="w")
    divine_path_entry = ttk.Entry(frm, width=100)
    divine_path_entry.insert(0, settings["divine_path"])
    divine_path_entry.grid(column=0, row=7, columnspan=2, pady=5)

    ttk.Label(frm, text="Handle:").grid(column=0, row=8, sticky="w")
    handle_entry = ttk.Entry(frm, width=100)
    handle_entry.insert(0, settings["handle"])
    handle_entry.grid(column=0, row=9, columnspan=2, pady=5)

    ttk.Label(frm, text="Dialog File:").grid(column=0, row=10, sticky="w")
    dialog_entry = ttk.Entry(frm, width=100)
    dialog_entry.insert(0, settings["dialog_file"])
    dialog_entry.grid(column=0, row=11, columnspan=2, pady=5)

    prog_var = tk.DoubleVar()
    prog_bar = ttk.Progressbar(frm, variable=prog_var)
    prog_bar.grid(column=0, row=12, columnspan=2, pady=5, sticky="ew")

    convert_btn = ttk.Button(
        frm,
        text="Convert",
        command=lambda: on_submit(
            mod_name_entry,
            game_data_path_entry,
            unpacked_data_path_entry,
            divine_path_entry,
            handle_entry,
            dialog_entry,
            prog_var,
            root,
        ),
    )
    convert_btn.grid(column=0, row=13, sticky="w")

    quit_btn = ttk.Button(
        frm,
        text="Quit",
        command=lambda: on_quit(
            root,
            mod_name_entry,
            game_data_path_entry,
            unpacked_data_path_entry,
            divine_path_entry,
            handle_entry,
            dialog_entry,
        ),
    )
    quit_btn.grid(column=1, row=13, sticky="e")

    root.protocol(
        "WM_DELETE_WINDOW",
        lambda: on_quit(
            root,
            mod_name_entry,
            game_data_path_entry,
            unpacked_data_path_entry,
            divine_path_entry,
            handle_entry,
            dialog_entry,
        ),
    )

    root.mainloop()


if __name__ == "__main__":
    main()
