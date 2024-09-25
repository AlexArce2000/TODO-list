import tkinter as tk
import re
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

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
def add_task():
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
    
    task_entry.delete(0, tk.END)  # Limpiar campo de texto
    update_task_list()

# Función para actualizar la lista de tareas
def update_task_list():
    task_listbox.delete(0, tk.END)  # Limpiar la lista actual
    tasks = load_tasks()
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        color = "green" if task["completed"] else "red"
        date = re.compile(r'(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2})')
        match = date.search(task['created_at'])
        display_text = f"{task['id']}. {task['task']} [{status}] {match.group(1)} {match.group(2)}"
        task_listbox.insert(tk.END, display_text)
        
        # Cambiar el color según el estado
        task_listbox.itemconfig(tk.END, {'fg': color})

# Función para marcar tarea como completada
def complete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]  # Selección en la lista
        tasks = load_tasks()
        task_id = selected_task_index + 1  # El ID es el índice + 1
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                save_tasks(tasks)
                update_task_list()
                return
    except IndexError:
        pass  # No mostrar advertencia aquí

# Función para eliminar tarea
def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]  # Selección en la lista
        tasks = load_tasks()
        # El ID es el índice de la lista de tareas
        task_id = selected_task_index + 1  # El ID es el índice + 1
        # Eliminar la tarea seleccionada
        tasks.pop(selected_task_index)
        # Actualizar los IDs de las tareas restantes
        for index, task in enumerate(tasks):
            task["id"] = index + 1  # Actualizar ID
        save_tasks(tasks)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")

# Función para exportar tareas a PDF
# Función para exportar tareas a PDF
def export_to_pdf():
    tasks = load_tasks()
    if not tasks:
        messagebox.showwarning("Advertencia", "No hay tareas para exportar.")
        return

    pdf_file_path = "json-list/todo_list.pdf"  
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Establecer fuentes para los encabezados
    c.setFont("Helvetica-Bold", 14)  # Negrita para encabezados
    c.drawString(100, height - 50, "Lista de Tareas")
    c.drawString(100, height - 70, "ID")
    c.drawString(150, height - 70, "Tarea")
    c.drawString(300, height - 70, "Estado")

    # Dibuja línea horizontal para encabezados
    c.line(100, height - 75, 500, height - 75)

    # Regresar a la fuente normal para el contenido
    c.setFont("Times-Roman", 12)  # Fuente normal para las tareas

    y = height - 100
    for task in tasks:
        status = "Completada" if task["completed"] else "Pendiente"
        
        # Dibuja cuadro para cada tarea
        if task["completed"]:
            c.setFillColor(colors.green)
        else:
            c.setFillColor(colors.red)

        c.rect(95, y - 12, 410, 25, stroke=1, fill=1)  # Rectángulo alrededor de la tarea

        # Cambiar color del texto según el estado
        c.setFillColor(colors.white)  # Texto en blanco
        c.drawString(100, y, str(task['id']))  # ID
        c.drawString(150, y, task['task'])     # Tarea
        c.drawString(300, y, status)           # Estado
        
        y -= 30  # Espacio entre líneas (ajustado para el alto del cuadro)

    c.save()
    messagebox.showinfo("Éxito", f"Lista de tareas exportada a {pdf_file_path}")
    
# Variable para controlar si el clic fue en el botón
clicked_button = False

# Función para deseleccionar la tarea al hacer clic fuera del Listbox
def deselect_task(event):
    global clicked_button
    if not clicked_button and task_listbox.winfo_containing(event.x_root, event.y_root) != task_listbox:
        if not (event.widget == delete_button or event.widget == complete_button):
            task_listbox.selection_clear(0, tk.END)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestor de Tareas")
root.geometry("400x400")
root.resizable(False, False)  # Evitar que la ventana cambie de tamaño
root.configure(bg="lightblue")

# Cargar el ícono (en formato PNG)
icon_path = "image/icon-app.png"  # Reemplaza con la ruta del ícono
icon_img = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_img)

# Cargar la imagen de fondo
bg_image_path = "image/fondo.jpg"  # Reemplaza con la ruta de tu imagen
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((400, 400))  # Ajustar el tamaño de la imagen
bg_photo = ImageTk.PhotoImage(bg_image)

# Crear un Label con la imagen de fondo
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Colocar el Label en toda la ventana

# Asignar el ícono a la ventana principal
root.iconphoto(False, icon_photo)

# Cargar iconos
icon_add_path = "image/add.png"
icon_delete_path = "image/delete.png"
icon_complete_path = "image/complete.png"
icon_pdf_path = "image/pdf.png"  # Reemplaza con la ruta de tu ícono de PDF

# Crear objetos PhotoImage
img_add = Image.open(icon_add_path).resize((20, 20))
icon_add = ImageTk.PhotoImage(img_add)

img_delete = Image.open(icon_delete_path).resize((20, 20))
icon_delete = ImageTk.PhotoImage(img_delete)

img_complete = Image.open(icon_complete_path).resize((20, 20))
icon_complete = ImageTk.PhotoImage(img_complete)

img_pdf = Image.open(icon_pdf_path).resize((20, 20))
icon_pdf = ImageTk.PhotoImage(img_pdf)

# Campo de entrada para añadir tareas
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# Asocia el evento de la tecla Enter con la función add_task
task_entry.bind("<Return>", lambda event: add_task())

# Botón con ícono para añadir tarea
add_button = tk.Button(root, text="Añadir tarea", command=add_task, image=icon_add, compound=tk.LEFT)
add_button.pack(pady=5)

    # Listbox para mostrar las tareas
task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(pady=10)

# Botón para marcar como completada
complete_button = tk.Button(root, text="Marcar como completada", command=complete_task, image=icon_complete, compound=tk.LEFT)
complete_button.pack(pady=5)

# Botón para eliminar tarea
delete_button = tk.Button(root, text="Eliminar tarea", command=delete_task, image=icon_delete, compound=tk.LEFT)
delete_button.pack(pady=5)

# Botón para exportar tareas a PDF con ícono
export_button = tk.Button(root, text="Exportar a PDF", command=export_to_pdf, image=icon_pdf, compound=tk.LEFT)
export_button.pack(pady=5)

# Actualizar la lista de tareas al inicio
update_task_list()

# Función para manejar el clic en el botón "Marcar como completada"
def on_complete_click():
    global clicked_button
    clicked_button = True
    complete_task()
    clicked_button = False

# Asociar el evento de clic a la función deselect_task
root.bind("<Button-1>", deselect_task)

# Asignar el evento de clic en el botón "Marcar como completada"
complete_button.bind("<Button-1>", lambda event: on_complete_click())

# Ejecutar la aplicación
root.mainloop()
