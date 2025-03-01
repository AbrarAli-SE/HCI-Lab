import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.tasks = []

        self.task_listbox = tk.Listbox(root, height=15, width=50)
        self.task_listbox.pack(pady=20)

        self.task_listbox.bind("<Button-1>", self.on_start_drag)
        self.task_listbox.bind("<B1-Motion>", self.on_dragging)
        self.task_listbox.bind("<ButtonRelease-1>", self.on_drop)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_tasks)
        self.file_menu.add_command(label="Load", command=self.load_tasks)

    def on_start_drag(self, event):
        self.start_index = self.task_listbox.nearest(event.y)

    def on_dragging(self, event):
        self.dragging_index = self.task_listbox.nearest(event.y)
        if self.dragging_index != self.start_index:
            self.task_listbox.delete(self.start_index)
            self.task_listbox.insert(self.dragging_index, self.tasks[self.start_index]['title'])
            self.task_listbox.select_set(self.dragging_index)
            self.start_index = self.dragging_index

    def on_drop(self, event):
        self.tasks = [self.tasks[self.task_listbox.index(i)] for i in range(self.task_listbox.size())]

    def add_task(self):
        task_title = simpledialog.askstring("Add Task", "Enter task title:")
        task_deadline = simpledialog.askstring("Add Task", "Enter task deadline:")
        if task_title and task_deadline:
            self.tasks.append({"title": task_title, "deadline": task_deadline})
            self.update_task_listbox()

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            task = self.tasks[task_index]
            new_title = simpledialog.askstring("Edit Task", "Enter new title:", initialvalue=task["title"])
            new_deadline = simpledialog.askstring("Edit Task", "Enter new deadline:", initialvalue=task["deadline"])
            if new_title and new_deadline:
                self.tasks[task_index] = {"title": new_title, "deadline": new_deadline}
                self.update_task_listbox()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['title']} (Deadline: {task['deadline']})")

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
