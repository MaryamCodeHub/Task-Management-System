import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

tasks = []
task_id = 1

def add_task():
    global task_id
    description = simpledialog.askstring("Add Task", "Enter task description:")
    if description:
        tasks.append({'id': task_id, 'description': description, 'status': 'pending'})
        update_task_view()
        task_id += 1

def update_task_view():
    task_tree.delete(*task_tree.get_children())  # Clear existing rows in Treeview
    for task in tasks:
        task_tree.insert('', tk.END, iid=task['id'], values=(task['id'], task['description'], task['status']))

def remove_task(task_id):
    global tasks
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        tasks.remove(task)
        update_task_view()
        messagebox.showinfo("Info", f"Task '{task['description']}' removed.")
    else:
        messagebox.showerror("Error", "Task not found.")

def mark_task_completed(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['status'] = 'completed'
        update_task_view()
        messagebox.showinfo("Info", f"Task '{task['description']}' marked as completed.")
    else:
        messagebox.showerror("Error", "Task not found.")

def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        new_description = simpledialog.askstring("Edit Task", f"Enter new description for task '{task['description']}':")
        if new_description:
            task['description'] = new_description
            update_task_view()
            messagebox.showinfo("Info", f"Task ID {task['id']} updated.")
        else:
            messagebox.showwarning("Warning", "No description entered. Task not updated.")
    else:
        messagebox.showerror("Error", "Task not found.")

def on_task_right_click(event):
    selected_item = task_tree.selection()
    if selected_item:
        task_id = int(selected_item[0])
        task_menu = tk.Menu(root, tearoff=0)
        task_menu.add_command(label="Mark as Completed", command=lambda: mark_task_completed(task_id))
        task_menu.add_command(label="Edit Task", command=lambda: edit_task(task_id))
        task_menu.add_command(label="Remove Task", command=lambda: remove_task(task_id))
        task_menu.post(event.x_root, event.y_root)

def clear_all_tasks():
    confirmation = messagebox.askyesno("Clear All Tasks", "Are you sure you want to clear all tasks?")
    if confirmation:
        tasks.clear()
        update_task_view()
        messagebox.showinfo("Info", "All tasks cleared.")

# Initialize the main window
root = tk.Tk()
root.title("Task Management System")

# Treeview for displaying tasks
columns = ('ID', 'Description', 'Status')
task_tree = ttk.Treeview(root, columns=columns, show='headings')
task_tree.heading('ID', text='ID')
task_tree.heading('Description', text='Description')
task_tree.heading('Status', text='Status')
task_tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Bind right-click (context menu) for task management
task_tree.bind("<Button-3>", on_task_right_click)  # Right-click event for Windows/Linux
task_tree.bind("<Control-1>", on_task_right_click)  # Right-click event for macOS (Command-click)

# Add and Clear buttons
tk.Button(root, text="Add Task", command=add_task).pack(pady=5)
tk.Button(root, text="Clear All Tasks", command=clear_all_tasks).pack(pady=5)

# Initialize task view
update_task_view()
root.mainloop()
