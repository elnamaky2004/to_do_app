import json
import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# -------- Storage  --------
home = os.path.expanduser("~")
if sys.platform == "win32":
    base = os.getenv("LOCALAPPDATA") or home
elif sys.platform == "darwin":
    base = os.path.join(home, "Library", "Application Support")
else:
    base = os.path.join(home, ".local", "share")

APP_DIR = os.path.join(base, "simple_todo_app")
os.makedirs(APP_DIR, exist_ok=True)
DATA_FILE = os.path.join(APP_DIR, "todo_data.json")


def load_tasks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


# -------- GUI App --------
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("450x400")

        self.tasks = load_tasks()

        self.listbox = tk.Listbox(root, font=("Segoe UI", 11))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Task", width=12, command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Mark Done", width=12, command=self.mark_done).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remove", width=12, command=self.remove_task).grid(row=0, column=2, padx=5)

        tk.Button(root, text="Clear All", width=15, command=self.clear_tasks).pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for i, t in enumerate(self.tasks, 1):
            status = "✔" if t["done"] else "✖"
            self.listbox.insert(tk.END, f"{i}. [{status}] {t['title']}")

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Task title:")
        if title:
            self.tasks.append({
                "title": title.strip(),
                "done": False,
                "created": datetime.now().isoformat()
            })
            save_tasks(self.tasks)
            self.refresh_list()

    def mark_done(self):
        try:
            idx = self.listbox.curselection()[0]
            self.tasks[idx]["done"] = True
            save_tasks(self.tasks)
            self.refresh_list()
        except:
            messagebox.showwarning("Warning", "Select a task first")

    def remove_task(self):
        try:
            idx = self.listbox.curselection()[0]
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh_list()
        except:
            messagebox.showwarning("Warning", "Select a task first")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.refresh_list()


# -------- Run --------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
