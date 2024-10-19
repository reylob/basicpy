import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('members.db')
c = conn.cursor()

# Create members table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL UNIQUE
    )
''')
conn.commit()

# Functions
def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good Morning!"
    elif 12 <= current_hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

def is_valid_philippine_number(contact):
    return contact.startswith("63") and len(contact) == 12 and contact.isdigit()

def add_member():
    name = entry_name.get()
    contact = entry_contact.get()

    if name and is_valid_philippine_number(contact):  # Validate Philippine number
        try:
            c.execute("INSERT INTO members (name, contact) VALUES (?, ?)", (name, contact))
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            entry_name.delete(0, tk.END)
            entry_contact.delete(0, tk.END)
            view_members()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicate Error", "This contact already exists. Please enter a unique contact.")
    else:
        messagebox.showwarning("Input Error", "Please fill in both name and a valid 12-digit Philippine contact number (e.g., 639XXXXXXXXX).")

def view_members():
    listbox_members.delete(0, tk.END)
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    if members:
        for row in members:
            listbox_members.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Contact: {row[2]}")
    else:
        messagebox.showinfo("Info", "No members found.")

def delete_member():
    selected = listbox_members.curselection()
    if selected:
        member_data = listbox_members.get(selected[0])
        member_id = int(member_data.split(',')[0].split(': ')[1])
        c.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
        messagebox.showinfo("Success", "Member deleted successfully!")
        view_members()
    else:
        messagebox.showwarning("Selection Error", "Please select a member to delete.")

def search_member():
    search_name = entry_search.get()
    listbox_members.delete(0, tk.END)
    c.execute("SELECT * FROM members WHERE name LIKE ?", ('%' + search_name + '%',))
    results = c.fetchall()
    if results:
        for row in results:
            listbox_members.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Contact: {row[2]}")
    else:
        messagebox.showinfo("No Results", "No members found with that name.")

# Navigation functions
def show_frame(frame):
    frame.tkraise()

# Input validation: Ensure only digits in contact entry
def validate_contact(char):
    return char.isdigit()

# GUI setup
root = tk.Tk()
root.title("Member Management System")

# Main window layout
root.geometry("700x600")

# Define frames for different views
home_frame = tk.Frame(root)
add_frame = tk.Frame(root)
view_frame = tk.Frame(root)
search_frame = tk.Frame(root)

for frame in (home_frame, add_frame, view_frame, search_frame):
    frame.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

# Responsive grid configuration
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)

# Home frame content
greeting_label = tk.Label(home_frame, text=get_greeting(), font=("Arial", 18), fg="blue")
greeting_label.grid(row=0, column=0, columnspan=3, pady=20)

welcome_label = tk.Label(home_frame, text="Welcome to the Member Management System", font=("Arial", 14))
welcome_label.grid(row=1, column=0, columnspan=3, pady=10)

# Add member frame content
tk.Label(add_frame, text="Add New Member", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)
tk.Label(add_frame, text="Name", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")
entry_name = tk.Entry(add_frame, font=("Arial", 12), width=30)
entry_name.grid(row=1, column=1, pady=5, columnspan=2, sticky="w")

tk.Label(add_frame, text="Contact (Philippine, 12 digits)", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="e")
vcmd = (root.register(validate_contact), '%S')
entry_contact = tk.Entry(add_frame, font=("Arial", 12), width=30, validate='key', validatecommand=vcmd)
entry_contact.grid(row=2, column=1, pady=5, columnspan=2, sticky="w")

btn_add_member = tk.Button(add_frame, text="Add Member", command=add_member, bg="green", fg="white", font=("Arial", 12))
btn_add_member.grid(row=3, column=1, pady=10)

# View members frame content
tk.Label(view_frame, text="Member List", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

listbox_members = tk.Listbox(view_frame, font=("Arial", 12), width=50, height=10)
listbox_members.grid(row=1, column=0, columnspan=3, pady=10)

btn_view_refresh = tk.Button(view_frame, text="Refresh List", command=view_members, bg="blue", fg="white", font=("Arial", 12))
btn_view_refresh.grid(row=2, column=1, pady=5)

btn_delete_member = tk.Button(view_frame, text="Delete Selected Member", command=delete_member, bg="red", fg="white", font=("Arial", 12))
btn_delete_member.grid(row=3, column=1, pady=10)

# Search members frame content
tk.Label(search_frame, text="Search Members", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)
tk.Label(search_frame, text="Enter Name", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")
entry_search = tk.Entry(search_frame, font=("Arial", 12), width=30)
entry_search.grid(row=1, column=1, pady=5, columnspan=2, sticky="w")

btn_search_member = tk.Button(search_frame, text="Search", command=search_member, bg="orange", fg="white", font=("Arial", 12))
btn_search_member.grid(row=2, column=1, pady=10)

listbox_members_search = tk.Listbox(search_frame, font=("Arial", 12), width=50, height=10)
listbox_members_search.grid(row=3, column=0, columnspan=3, pady=10)

# Inline navigation bar (top)
nav_frame = tk.Frame(root, bg="lightgray")
nav_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

btn_home = tk.Button(nav_frame, text="Home", command=lambda: show_frame_mem(home_frame), font=("Arial", 12), bg="lightblue")
btn_home.pack(side="left", padx=5, pady=5)

btn_add = tk.Button(nav_frame, text="Add Member", command=lambda: show_frame_mem(add_frame), font=("Arial", 12), bg="lightgreen")
btn_add.pack(side="left", padx=5, pady=5)

# Navigation functions
def show_frame_mem(frame_view):
    frame_view.tkraise()

# Modify this part in your navigation bar to show members when "View Members" is clicked
btn_view = tk.Button(nav_frame, text="View Members",
                     command=lambda: [show_frame_mem(view_frame), view_members()],  # Trigger view_members when clicked
                     font=("Arial", 12), bg="lightyellow")
btn_view.pack(side="left", padx=5, pady=5)


btn_search = tk.Button(nav_frame, text="Search Members", command=lambda: show_frame_mem(search_frame), font=("Arial", 12), bg="orange")
btn_search.pack(side="left", padx=5, pady=5)

btn_exit = tk.Button(nav_frame, text="Exit", command=root.quit, font=("Arial", 12), bg="red", fg="white")
btn_exit.pack(side="right", padx=5, pady=5)

# Show home frame at startup
show_frame_mem(home_frame)

# Start the GUI main loop
root.mainloop()

# Close the connection when done
conn.close()
