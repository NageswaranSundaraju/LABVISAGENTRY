import tkinter as tk
from tkinter import Toplevel


def main():
    global root
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("400x300")
    open_button = tk.Button(root, text="Open Second Window",
                            # command=open_second_window
                            )
    open_button.pack(pady=50)

    # Run the Tkinter event loop
    root.mainloop()

# Variable to keep track of the secondary window
# second_window = None
#
# def open_second_window():
#     global second_window, root
#     if second_window is None or not tk.Toplevel.winfo_exists(second_window):
#         second_window = Toplevel(root)
#         second_window.title("Second Window")
#         second_window.geometry("300x200")
#
#         label = tk.Label(second_window, text="This is the second window")
#         label.pack(pady=20)
#
#         close_button = tk.Button(second_window, text="Close", command=close_second_window)
#         close_button.pack(pady=20)
#     else:
#         second_window.lift()
#
# def close_second_window():
#     global second_window
#     if second_window is not None:
#         second_window.destroy()
#         second_window = None
#
# # Add a button to open the second window
# if __name__ == '__main__':
#     main()
