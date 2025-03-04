import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from tkcalendar import Calendar
import json
from ttkthemes import ThemedStyle

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        self.tasks = []
        
        # Set the style for the application
        style = ThemedStyle(root)
        style.set_theme("clam")
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TListbox', font=('Helvetica', 12))

        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(self.frame, width=200, relief=tk.SUNKEN)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        self.main_area = ttk.Frame(self.frame)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # Task Listbox
        self.task_listbox = tk.Listbox(self.main_area, height=15, width=50, font=('Helvetica', 12))
        self.task_listbox.grid(row=0, column=0, columnspan=4, pady=20)
        
        # Buttons
        self.add_button = ttk.Button(self.main_area, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=10)
        
        self.edit_button = ttk.Button(self.main_area, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=1, column=1, padx=10)
        
        self.delete_button = ttk.Button(self.main_area, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=1, column=2, padx=10)
        
        self.complete_button = ttk.Button(self.main_area, text="Mark as Completed", command=self.mark_as_completed)
        self.complete_button.grid(row=1, column=3, padx=10)
        
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_tasks)
        self.file_menu.add_command(label="Load", command=self.load_tasks)
        
        # Priority selection
        self.priority_label = ttk.Label(self.sidebar, text="Select Priority")
        self.priority_label.grid(row=0, column=0, pady=10)
        
        self.priority_combobox = ttk.Combobox(self.sidebar, values=["Low", "Medium", "High"])
        self.priority_combobox.grid(row=1, column=0, pady=10)
        
        # Calendar for deadlines
        self.calendar_label = ttk.Label(self.sidebar, text="Select Deadline")
        self.calendar_label.grid(row=2, column=0, pady=10)
        
        self.calendar = Calendar(self.sidebar, selectmode='day')
        self.calendar.grid(row=3, column=0, pady=10)

    def add_task(self):
        task_title = simpledialog.askstring("Add Task", "Enter task title:")
        task_priority = self.priority_combobox.get()
        task_deadline = self.calendar.get_date()
        if task_title and task_deadline:
            self.tasks.append({"title": task_title, "deadline": task_deadline, "priority": task_priority, "completed": False})
            self.update_task_listbox()
        
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            task = self.tasks[task_index]
            new_title = simpledialog.askstring("Edit Task", "Enter new title:", initialvalue=task["title"])
            new_priority = simpledialog.askstring("Edit Task", "Enter new priority (Low, Medium, High):", initialvalue=task["priority"])
            new_deadline = self.calendar.get_date()
            if new_title and new_deadline:
                self.tasks[task_index] = {"title": new_title, "deadline": new_deadline, "priority": new_priority, "completed": task["completed"]}
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
            self.task_listbox.insert(tk.END, f"{task['title']} (Deadline: {task['deadline']}, Priority: {task['priority']}, Status: {status})")
            
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
    
