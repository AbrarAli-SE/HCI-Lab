import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from tkcalendar import Calendar
import json

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        self.tasks = []

        # Set the style for the application
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TListbox', font=('Helvetica', 12))

        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.frame, height=15, width=50, font=('Helvetica', 12))
        self.task_listbox.grid(row=0, column=0, columnspan=4, pady=20)
        
        self.task_listbox.bind("<Button-1>", self.on_start_drag)
        self.task_listbox.bind("<B1-Motion>", self.on_dragging)
        self.task_listbox.bind("<ButtonRelease-1>", self.on_drop)
        
        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=10)

        self.edit_button = ttk.Button(self.frame, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=1, column=1, padx=10)

        self.delete_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=1, column=2, padx=10)

        self.complete_button = ttk.Button(self.frame, text="Mark as Completed", command=self.mark_as_completed)
        self.complete_button.grid(row=1, column=3, padx=10)

        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_tasks)
        self.file_menu.add_command(label="Load", command=self.load_tasks)
        
        # Calendar for setting deadlines
        self.calendar_label = ttk.Label(self.frame, text="Select Deadline")
        self.calendar_label.grid(row=2, column=0, pady=10)

        self.calendar = Calendar(self.frame, selectmode='day')
        self.calendar.grid(row=3, column=0, columnspan=4, pady=10)

    def on_start_drag(self, event):
        self.start_index = self.task_listbox.nearest(event.y)

    def on_dragging(self, event):
        self.dragging_index = self.task_listbox.nearest(event.y)
        if self.dragging_index != self.start_index:
            self.task_listbox.delete(self.start_index)
            task = self.tasks.pop(self.start_index)
            self.tasks.insert(self.dragging_index, task)
            self.update_task_listbox()
            self.task_listbox.select_set(self.dragging_index)
            self.start_index = self.dragging_index

    def on_drop(self, event):
        self.update_task_listbox()

    def add_task(self):
        task_title = simpledialog.askstring("Add Task", "Enter task title:")
        task_deadline = self.calendar.get_date()
        if task_title and task_deadline:
            self.tasks.append({"title": task_title, "deadline": task_deadline, "completed": False})
            self.update_task_listbox()
        
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            task = self.tasks[task_index]
            new_title = simpledialog.askstring("Edit Task", "Enter new title:", initialvalue=task["title"])
            new_deadline = self.calendar.get_date()
            if new_title and new_deadline:
                self.tasks[task_index] = {"title": new_title, "deadline": new_deadline, "completed": task["completed"]}
                self.update_task_listbox()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.update_task_listbox()

    def mark_as_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]["completed"] = True
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task["completed"] else "Pending"
            self.task_listbox.insert(tk.END, f"{task['title']} (Deadline: {task['deadline']}, Status: {status})")

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.tasks, file)

    def load_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.tasks = json.load(file)
            self.update_task_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
