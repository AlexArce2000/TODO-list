import json
import datetime
import os

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
def add_task(task_description):
    if not task_description:
        return False  # No se puede añadir una tarea vacía
    
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "task": task_description,
        "created_at": datetime.datetime.now().isoformat(),
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return True  # Tarea añadida con éxito

# Función para marcar tarea como completada
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return True
    return False  # Tarea no encontrada

# Función para eliminar tarea
def delete_task(task_id):
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            # Actualizar los IDs de las tareas restantes
            for idx, t in enumerate(tasks):
                t["id"] = idx + 1  # Actualizar ID
            save_tasks(tasks)
            return True  # Tarea eliminada con éxito
    return False  # Tarea no encontrada
