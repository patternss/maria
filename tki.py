#Maria - the number one virtual teacher

import tkinter as tk

#init root window
root = tk.Tk()
root.title("Maria")
root.geometry("1920x1080")
root.configure(bg='lightgrey')

prob_label = tk.Label(root, text="")
prob_label.pack()

def on_click_prob():
    prob_label.config(text="do something with your life!")

new_prob_but = tk.Button(root, text="New problemo", command=on_click_prob)
new_prob_but.pack()

#run Maria
root.mainloop()

