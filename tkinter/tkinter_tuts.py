from tkinter import *


def km_to_miles():
    miles = float(e1_value.get()) * 1.6  # .get untuk mendapatkan stringnya
    t1.insert(END, miles)  # END untuk meletakan di END?


window = Tk()

b1 = Button(window, text="Execute", command=km_to_miles)
b1.grid(row=0, column=0)

e1_value = StringVar()  # Storage untuk data hasil input
e1 = Entry(window, textvariable=e1_value)
e1.grid(row=0, column=1)

t1 = Text(window, height=1, width=20)
t1.grid(row=0, column=2)

window.mainloop()  # Widgets ada di antara windows dan mainloop
