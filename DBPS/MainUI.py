from tkinter import *
# import tkinter as tk

from tkinter import Toplevel


def main():
    global root
    root = Tk()
    root.title("LVE ADMIN")
    root.geometry("955x500")

    HeaderTitle = Label(root, text='Lab Visage Entry Admin', font=("Arial", 40, "bold"))
    HeaderTitle.pack()

    detailFrame = Frame(root, bg='White', height=310, width=430)
    detailFrame.pack(side = LEFT, padx = 50)


    nameLabel = Label(detailFrame, text='Name')
    nameLabel.pack()

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    main()