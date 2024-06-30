import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import logging

logging.basicConfig(filename="admin.log", level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data():
    try:
        connection = mysql.connector.connect(
            user='NAGES',
            password='ROOT',
            host='192.168.0.254',
            database='lvedb'
        )
        cursor = connection.cursor()
        select_query = "SELECT name, noic, notel FROM lect"
        cursor.execute(select_query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        return data

    except mysql.connector.Error as err:
        logging.error(f"{err} - Error in show lect module")
        print(f"Error: {err}")
        return []

def delete_data(selected_item):
    try:
        connection = mysql.connector.connect(
            user='NAGES',
            password='ROOT',
            host='192.168.0.254',
            database='lvedb'
        )
        cursor = connection.cursor()
        delete_query = "DELETE FROM lect WHERE noic = %s"
        cursor.execute(delete_query, (selected_item[1],))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except mysql.connector.Error as err:
        logging.error(f"{err} - Error in delete lect module")
        print(f"Error: {err}")
        return False

def update_data(selected_item, updated_values):
    try:
        connection = mysql.connector.connect(
            user='NAGES',
            password='ROOT',
            host='192.168.0.254',
            database='lvedb'
        )
        cursor = connection.cursor()
        update_query = "UPDATE lect SET name = %s, notel = %s WHERE noic = %s"
        cursor.execute(update_query, (updated_values[0], updated_values[2], selected_item[1]))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except mysql.connector.Error as err:
        logging.error(f"{err} - Error in update lect module")
        print(f"Error: {err}")
        return False

def on_delete():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No item selected")
        return
    item = tree.item(selected_item)
    values = item['values']

    if messagebox.askyesno("Delete", f"Are you sure you want to delete {values[0]}?"):
        if delete_data(values):
            tree.delete(selected_item)
            messagebox.showinfo("Success", "Item deleted successfully")
        else:
            messagebox.showerror("Error", "Failed to delete item. Check log for details.")

def on_update():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No item selected")
        return
    item = tree.item(selected_item)
    values = item['values']

    def save_updates():
        updated_values = (name_entry.get(), noic_entry.get(), notel_entry.get())
        if update_data(values, updated_values):
            tree.item(selected_item, values=updated_values)
            messagebox.showinfo("Success", "Item updated successfully")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to update item. Check log for details.")

    update_window = tk.Toplevel(root)
    update_window.title("Update Item")
    update_window.geometry("300x200")

    tk.Label(update_window, text="Name").pack(pady=5)
    name_entry = tk.Entry(update_window)
    name_entry.pack(pady=5)
    name_entry.insert(0, values[0])

    tk.Label(update_window, text="IC Number").pack(pady=5)
    noic_entry = tk.Entry(update_window)
    noic_entry.pack(pady=5)
    noic_entry.insert(0, values[1])

    tk.Label(update_window, text="Telephone Number").pack(pady=5)
    notel_entry = tk.Entry(update_window)
    notel_entry.pack(pady=5)
    notel_entry.insert(0, values[2])

    tk.Button(update_window, text="Save", command=save_updates).pack(pady=10)

def create_gui():
    global root, tree
    root = tk.Tk()
    root.title("List of Names")
    root.geometry("600x400")

    label = tk.Label(root, text="Names, IC Numbers, and Telephone Numbers in Database", font=("Arial", 16))
    label.pack(pady=10)

    # Create Treeview widget with scrollbars
    frame = tk.Frame(root)
    frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Name", "NOIC", "NOTEL"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("NOIC", text="IC Number")
    tree.heading("NOTEL", text="Telephone Number")

    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

    # Insert data into the Treeview
    data = fetch_data()
    if data:
        for row in data:
            tree.insert("", tk.END, values=row)
    else:
        error_label = tk.Label(root, text="Error fetching data from the database. Check the log for details.", fg="red")
        error_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    delete_button = tk.Button(button_frame, text="Delete", command=on_delete)
    delete_button.pack(side=tk.LEFT, padx=10)

    update_button = tk.Button(button_frame, text="Update", command=on_update)
    update_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
