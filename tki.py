#tkinter based interface for Maria

import tkinter as tk

#init root window
root = tk.Tk()
root.title("Maria")
root.geometry("1920x1080")
root.configure(bg='lightgrey')


#frame for displaying problems
prob_frame = tk.Frame(root, bg="grey", bd=2, relief="sunken")
prob_frame.pack(fill='both',  side=tk.LEFT, expand=True, padx=10, pady=10)
prob_label = tk.Label(prob_frame, text="" )
prob_label.pack(padx=5, pady=5)

def on_click_prob():
    prob_label.config(text="do something with your life!")

new_prob_but = tk.Button(prob_frame, text="New problemo", command=on_click_prob)
new_prob_but.pack(padx=5, pady=5, side=tk.LEFT)

#Frame for topic selection
topics_frame = tk.Frame(root, bg="grey", bd=2, relief="sunken")
topics_frame.pack(fill='both', side=tk.RIGHT, expand=False, padx=10, pady=10)
topics_header = tk.Label(topics_frame, text='Topics')
topics_header.pack(padx=5,  pady=5)

#run Maria
root.mainloop()

