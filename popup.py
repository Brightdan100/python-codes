import tkinter as tk
from tkinter import ttk
NORM_FONT = ("Helvetica", 15)
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("State of DB")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

popupmsg("The DB is innconsistent\nCheck out below for more details")
