"""
Ini adalah frontend dari:
Book Storage database

Powered by SQLITE3

Book identity:
Name, Author, Year, ISBN

Users can:
Search entry
Entry entry
Read record
Update entry
Delete entry
Close app
"""

from tkinter import *
import backend

# Tiap backend function harus disatukan dengan fungsi lagi di frontend


def get_selected_row(event):
    try:
        global selected_tuple  # Global enables a variable to be called outside of a function
        index = list1.curselection()[0]  # Karena return tuple dengan 1 value
        selected_tuple = list1.get(index)
        # Ga perlu return selected_tuple karena dah bisa dicall di luar function
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[2])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
    except:
        pass


def view_command():  # Untuk memasukan data ke list box
    list1.delete(0, END)
    for row in backend.view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in backend.search(
        titleText_value.get(),
        authorText_value.get(),
        yearText_value.get(),
        isbnText_value.get(),
    ):
        list1.insert(END, row)


def add_command():
    list1.delete(0, END)
    backend.insert(
        titleText_value.get(),
        authorText_value.get(),
        yearText_value.get(),
        isbnText_value.get(),
    )
    list1.insert(END, "Entry success.")
    list1.insert(
        END,
        (
            titleText_value.get(),
            authorText_value.get(),
            yearText_value.get(),
            isbnText_value.get(),
        ),
    )


def delete_command():
    backend.delete(selected_tuple[0])  # Jadi gaperlu masukin fungsi, masukin global var


def update_command():
    backend.update(
        selected_tuple[0],
        titleText_value.get(),
        authorText_value.get(),
        yearText_value.get(),
        isbnText_value.get(),
    )
    print(
        selected_tuple[0],
        titleText_value.get(),
        authorText_value.get(),
        yearText_value.get(),
        isbnText_value.get(),
    )


window = Tk()
window.title("Book Storage Database")

l1 = Label(window, text="Title")
l1.grid(row=0, column=0)

l2 = Label(window, text="Year")
l2.grid(row=1, column=0)

l3 = Label(window, text="Author")
l3.grid(row=0, column=2)

l4 = Label(window, text="ISBN")
l4.grid(row=1, column=2)

titleText_value = StringVar()
e1 = Entry(window, textvariable=titleText_value)
e1.grid(row=0, column=1)

yearText_value = StringVar()
e2 = Entry(window, textvariable=yearText_value)
e2.grid(row=1, column=1)

authorText_value = StringVar()
e3 = Entry(window, textvariable=authorText_value)
e3.grid(row=0, column=3)

isbnText_value = StringVar()
e4 = Entry(window, textvariable=isbnText_value)
e4.grid(row=1, column=3)

list1 = Listbox(window, height=8, width=40)
list1.grid(row=2, column=0, rowspan=8, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=8)

list1.bind("<<ListboxSelect>>", get_selected_row)

b1 = Button(window, text="View all", width=15, command=view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Search entry", width=15, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add entry", width=15, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update", width=15, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete", width=15, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=15, command=window.destroy)
b6.grid(row=7, column=3)

window.mainloop()
