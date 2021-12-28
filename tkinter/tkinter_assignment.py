from tkinter import *


def converter():  # Ga perlu di pisah-pisah per converter ke 3 fungsi berbeda
    t1.delete("1.0", END)  # Untuk menghapus text setiap conversion
    t2.delete("1.0", END)
    t3.delete("1.0", END)

    grams = float(e1_value.get()) * 1000
    pounds = float(e1_value.get()) * 2.20462
    oz = float(e1_value.get()) * 35.274

    t1.insert(END, round(grams, 2))
    t1.insert(END, " g")  # Untuk menambah text di belakang angka

    t2.insert(END, round(pounds, 2))
    t2.insert(END, " lbs")

    t3.insert(END, round(oz, 2))
    t3.insert(END, " oz")


window = Tk()
window.title("Converter")  # Title window

windowLabel = Label(window, text="kg")  # Label di dalam window
windowLabel.grid(row=0, column=0)

e1_value = StringVar()  # Create a special stringvar object
e1 = Entry(window, textvariable=e1_value)  # Input box
e1.grid(row=0, column=1)

b1 = Button(window, text="Convert", command=converter)
b1.grid(row=0, column=2)

t1 = Text(window, height=1, width=20)
t1.grid(row=1, column=0)

t2 = Text(window, height=1, width=20)
t2.grid(row=1, column=1)

t3 = Text(window, height=1, width=20)
t3.grid(row=1, column=2)

window.mainloop()
