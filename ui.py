#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

import random_lock
import vault_ctl


def main():
    vault_ctl.read_credentials()

    # create tkinter window
    root = tk.Tk()
    root.title("PiVault")

    # title frame
    title_frame = ttk.Frame(root)
    title_label = ttk.Label(title_frame, text="PiVault Control", font=("Helvetica", 16))
    title_label.pack()
    title_frame.pack()
    ttk.Separator(root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)

    # Add a choice selector for the random lock style
    random_frame = ttk.Frame(root)
    style_label = ttk.Label(random_frame, text="Random Lock", font=("Helvetica", 12))
    style_label.pack(side=tk.TOP)
    style_var = tk.StringVar()
    style_var.set('uniform')
    style_selector = ttk.OptionMenu(random_frame, style_var, 'uniform', *['uniform', 'moody', 'low', 'middle', 'high'])
    style_selector.pack(side=tk.LEFT)
    random_button = ttk.Button(random_frame, text="Random Lock",
                               command=lambda: lock_with_random(total_time(hour_textbox, minute_textbox),
                                                                style_var.get()))
    random_button.pack(side=tk.LEFT)
    random_frame.pack()
    ttk.Separator(root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)

    # timed lframeock frame
    lock_frame = ttk.Frame(root)
    # create an hour text box and a label
    hour_textbox = ttk.Entry(lock_frame, width=10)
    hour_label = ttk.Label(lock_frame, text="Hours")
    # default 0 hours
    hour_textbox.insert(0, "0")

    # create a minute text box and a label
    minute_textbox = ttk.Entry(lock_frame, width=10)
    minute_label = ttk.Label(lock_frame, text="Minutes")
    # default 5 minutes
    minute_textbox.insert(0, "5")
    minute_textbox.focus()

    minute_textbox.bind("<Return>", lambda event: add_minutes(int(minute_textbox.get())))
    # put hours and minutes next to each other horizontally
    hour_label.pack(side=tk.LEFT)
    hour_textbox.pack(side=tk.LEFT)
    minute_label.pack(side=tk.LEFT)
    minute_textbox.pack(side=tk.LEFT)

    lock_frame.pack()

    # create buttons in their own frame
    button_frame = ttk.Frame(root, padding=(10, 10))
    unlock_button = ttk.Button(button_frame, text="Unlock", command=unlock)
    lock_button = ttk.Button(button_frame, text="Lock",
                             command=lambda: add_minutes(total_time(hour_textbox, minute_textbox)))
    unlock_button.pack(side=tk.LEFT)
    lock_button.pack(side=tk.LEFT)

    # pack the frames vertically
    button_frame.pack()
    lock_frame.pack()

    # start the GUI
    root.mainloop()


def total_time(hour_textbox, minute_textbox):
    return int(hour_textbox.get()) * 60 + int(minute_textbox.get())


def unlock():
    res = vault_ctl.unlock()
    vault_ctl.print_response(res)


def add_minutes(minutes):
    print(f"adding {minutes} minutes")
    dt = vault_ctl.add_minutes_to_now(minutes)
    res = vault_ctl.set_unlock_time(dt)
    vault_ctl.print_response(res)


def lock_with_random(max_minutes, style):
    random_lock.lock_up_to(max_minutes, style)


if __name__ == '__main__':
    main()
