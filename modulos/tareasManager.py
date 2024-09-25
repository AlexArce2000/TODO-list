import json
import os
import re
import datetime
from tkinter import messagebox

TODO_FILE = "json-list/todo_list.json"

# Funciones de almacenamiento
def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Función para añadir tarea
def add_task(task_entry, task_listbox):
    task_description = task_entry.get()
    if not task_description:
        messagebox.showwarning("Advertencia", "No puedes añadir una tarea vacía.")
        return
    
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "task": task_description,
        "created_at": datetime.datetime.now().isoformat(),
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    
    task_entry.delete(0, 'end')  # Limpiar campo de texto
    update_task_list(task_listbox)

# Función para actualizar la lista de tareas
def update_task_list(task_listbox):
    task_listbox.delete(0, 'end')  # Limpiar la lista actual
    tasks = load_tasks()
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        color = "green" if task["completed"] else "red"
        date = re.compile(r'(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2})')
        date_match = date.search(task['created_at'])
        display_text = f"{task['id']}. {task['task']} [{status}] {date_match.group(1)} {date_match.group(2)}"
        task_listbox.insert('end', display_text)
        task_listbox.itemconfig('end', {'fg': color})

# Función para marcar tarea como completada
def complete_task(task_listbox):
    try:
        selected_task_index = task_listbox.curselection()[0]  # Selección en la lista
        tasks = load_tasks()
        task_id = selected_task_index + 1  # El ID es el índice + 1
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                save_tasks(tasks)
                update_task_list(task_listbox)
                return
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para marcar.")
# Función para eliminar tarea
def delete_task(task_listbox):
    try:
        selected_task_index = task_listbox.curselection()[0]  # Selección en la lista
        tasks = load_tasks()
        tasks.pop(selected_task_index)
        for index, task in enumerate(tasks):
            task["id"] = index + 1  # Actualizar ID
        save_tasks(tasks)
        update_task_list(task_listbox)
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")
