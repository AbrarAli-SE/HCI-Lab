import tkinter as tk
from tkinter import messagebox, simpledialog

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        # List to store tasks
        self.tasks = []
        
        # Create the main window
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for the task list
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(pady=10)
        
        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.task_frame, width=50, height=10)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Attach scrollbar to listbox
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)
        
        # Frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        # Buttons for adding, editing, and deleting tasks
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=0, column=1, padx=5)
        
        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=5)
        
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_tasks)
        self.file_menu.add_command(label="Load", command=self.load_tasks)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
    def add_task(self):
        # Dialog to get task details
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if title:
            deadline = simpledialog.askstring("Add Task", "Enter task deadline:")
            if deadline:
                task = f"{title} - {deadline}"
                self.tasks.append(task)
                self.task_listbox.insert(tk.END, task)
        
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            selected_task = self.tasks[selected_task_index]
            
            # Dialog to edit task details
            new_title = simpledialog.askstring("Edit Task", "Edit task title:", initialvalue=selected_task.split(" - ")[0])
            if new_title:
                new_deadline = simpledialog.askstring("Edit Task", "Edit task deadline:", initialvalue=selected_task.split(" - ")[1])
                if new_deadline:
                    updated_task = f"{new_title} - {new_deadline}"
                    self.tasks[selected_task_index] = updated_task
                    self.task_listbox.delete(selected_task_index)
                    self.task_listbox.insert(selected_task_index, updated_task)
        
    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            self.task_listbox.delete(selected_task_index)
            del self.tasks[selected_task_index]
        
    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")
        messagebox.showinfo("Save", "Tasks saved successfully!")
        
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = [line.strip() for line in file.readlines()]
                self.task_listbox.delete(0, tk.END)
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, task)
            messagebox.showinfo("Load", "Tasks loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Load", "No saved tasks found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()