import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.font import Font

# Function to convert numbers to Roman numerals
def to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Task Manager")
        self.root.geometry("1200x800")
        self.root.minsize(1200, 800)
        
        # Apply a modern theme
        self.style = ttk.Style(theme="cosmo")
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.button_font = Font(family="Helvetica", size=12)
        self.text_font = Font(family="Courier New", size=12)
        
        # List to store tasks
        self.tasks = []
        
        # Create the main window
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = ttk.Label(self.main_container, text="Task Manager", font=self.title_font)
        self.title_label.pack(pady=10)
        
        # Task list frame
        self.task_frame = ttk.LabelFrame(self.main_container, text="Tasks", padding=10)
        self.task_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.task_frame, width=80, height=15, font=self.text_font, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for the listbox
        self.scrollbar = ttk.Scrollbar(self.task_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Attach scrollbar to listbox
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        
        # Enable drag-and-drop for the listbox
        self.task_listbox.bind("<ButtonPress-1>", self.on_drag_start)
        self.task_listbox.bind("<B1-Motion>", self.on_drag_motion)
        self.task_listbox.bind("<ButtonRelease-1>", self.on_drag_release)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_container)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons for adding, editing, and deleting tasks
        self.add_button = ttk.Button(self.button_frame, text="Add Task", command=self.add_task, bootstyle=SUCCESS, width=15)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(self.button_frame, text="Edit Task", command=self.edit_task, bootstyle=INFO, width=15)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bootstyle=DANGER, width=15)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Filter buttons
        self.filter_frame = ttk.LabelFrame(self.main_container, text="Filter Tasks", padding=10)
        self.filter_frame.pack(fill=tk.X, pady=10)
        
        self.filter_all_button = ttk.Button(self.filter_frame, text="All Tasks", command=self.filter_all_tasks, bootstyle=SECONDARY, width=15)
        self.filter_all_button.pack(side=tk.LEFT, padx=5)
        
        self.filter_high_button = ttk.Button(self.filter_frame, text="High Priority", command=lambda: self.filter_tasks_by_priority("High"), bootstyle=DANGER, width=15)
        self.filter_high_button.pack(side=tk.LEFT, padx=5)
        
        self.filter_medium_button = ttk.Button(self.filter_frame, text="Medium Priority", command=lambda: self.filter_tasks_by_priority("Medium"), bootstyle=WARNING, width=15)
        self.filter_medium_button.pack(side=tk.LEFT, padx=5)
        
        self.filter_low_button = ttk.Button(self.filter_frame, text="Low Priority", command=lambda: self.filter_tasks_by_priority("Low"), bootstyle=SUCCESS, width=15)
        self.filter_low_button.pack(side=tk.LEFT, padx=5)
        
        # Data input frame
        self.data_frame = ttk.LabelFrame(self.main_container, text="Data Input", padding=10)
        self.data_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text widget for multi-line input with Roman numerals
        self.data_text = scrolledtext.ScrolledText(self.data_frame, wrap=tk.WORD, width=80, height=10, font=self.text_font)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Button to convert numbers to Roman numerals
        self.roman_button = ttk.Button(self.data_frame, text="Convert to Roman", command=self.convert_to_roman, bootstyle=WARNING, width=20)
        self.roman_button.pack(pady=10)
        
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
            priority = simpledialog.askstring("Add Task", "Enter priority (High/Medium/Low):")
            if priority:
                deadline = simpledialog.askstring("Add Task", "Enter task deadline (YYYY-MM-DD):")
                if deadline:
                    # Assign a sequential number to the task
                    task_number = len(self.tasks) + 1
                    task = f"{task_number}. {title} - {priority} - {deadline}"
                    self.tasks.append(task)
                    self.task_listbox.insert(tk.END, task)
        
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            selected_task = self.tasks[selected_task_index]
            
            # Extract the task number from the selected task
            task_number = selected_task.split(".")[0]
            
            # Dialog to edit task details
            new_title = simpledialog.askstring("Edit Task", "Edit task title:", initialvalue=selected_task.split(" - ")[0].split(". ")[1])
            if new_title:
                new_priority = simpledialog.askstring("Edit Task", "Edit priority (High/Medium/Low):", initialvalue=selected_task.split(" - ")[1])
                if new_priority:
                    new_deadline = simpledialog.askstring("Edit Task", "Edit task deadline (YYYY-MM-DD):", initialvalue=selected_task.split(" - ")[2])
                    if new_deadline:
                        updated_task = f"{task_number}. {new_title} - {new_priority} - {new_deadline}"
                        self.tasks[selected_task_index] = updated_task
                        self.task_listbox.delete(selected_task_index)
                        self.task_listbox.insert(selected_task_index, updated_task)
        
    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            self.task_listbox.delete(selected_task_index)
            del self.tasks[selected_task_index]
            
            # Reassign task numbers after deletion
            self.reassign_task_numbers()
        
    def reassign_task_numbers(self):
        # Clear the listbox
        self.task_listbox.delete(0, tk.END)
        
        # Reassign numbers to tasks
        for i, task in enumerate(self.tasks):
            task_parts = task.split(". ", 1)
            if len(task_parts) > 1:
                new_task = f"{i + 1}. {task_parts[1]}"
                self.tasks[i] = new_task
                self.task_listbox.insert(tk.END, new_task)
        
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
    
    def convert_to_roman(self):
        # Get the text from the data box
        text = self.data_text.get("1.0", tk.END).strip()
        lines = text.split("\n")
        
        # Convert numbers to Roman numerals
        roman_text = ""
        for line in lines:
            try:
                num = int(line)
                roman_text += to_roman(num) + "\n"
            except ValueError:
                roman_text += line + "\n"
        
        # Update the data box with Roman numerals
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert(tk.END, roman_text)
    
    def filter_all_tasks(self):
        # Show all tasks
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)
    
    def filter_tasks_by_priority(self, priority):
        # Filter tasks by priority
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if f" - {priority} - " in task:
                self.task_listbox.insert(tk.END, task)
    
    def on_drag_start(self, event):
        # Get the index of the selected task
        self.drag_index = self.task_listbox.nearest(event.y)
    
    def on_drag_motion(self, event):
        # Move the task to the new position
        new_index = self.task_listbox.nearest(event.y)
        if new_index != self.drag_index:
            task = self.tasks.pop(self.drag_index)
            self.tasks.insert(new_index, task)
            self.task_listbox.delete(self.drag_index)
            self.task_listbox.insert(new_index, task)
            self.drag_index = new_index
    
    def on_drag_release(self, event):
        # Reassign task numbers after drag-and-drop
        self.reassign_task_numbers()

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = TaskManagerApp(root)
    root.mainloop()